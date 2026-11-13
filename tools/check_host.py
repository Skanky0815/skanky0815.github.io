"""Check the shared-host configuration before preparing its deployment."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCOPES = {"skanky0815.github.io/pixels-world", "skanky0815.github.io/pixels-world/*"}


class AgeMeta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name", "").lower() == "age-meta-label":
            self.values.append(attrs.get("content"))


def check_files():
    expected = {"age-de.xml", "age.xml", "index.html", ".nojekyll"}
    actual = {path.name for path in (ROOT / "public").iterdir()}
    if actual != expected:
        raise ValueError(f"Unerwartete Host-Dateien: {actual ^ expected}")
    for name in ("age-de.xml", "age.xml"):
        root = ET.parse(ROOT / "public" / name).getroot()
        if root.tag != "age-declaration":
            raise ValueError("Falsches XML-Wurzelelement")
        mode = root.find("ageblock-labeltype")
        expected_modes = {"htmlmeta": "true", "default-age": "18", "httpheader": "false",
                          "phraselabel": "false", "agesubmit": "false", "label-z": "false", "xmlfile": "false"}
        if mode is None or {node.tag: node.text for node in mode} != expected_modes:
            raise ValueError("Unerwartete Auswertung oder Fallback")
        scopes = [node.text for node in root.findall("./ageblock-labeltype-definition/labeltype-htmlmeta-definition/label/scope")]
        if len(scopes) != 2 or set(scopes) != SCOPES:
            raise ValueError("Scope muss auf beide Pixel’s-World-Einstiege begrenzt bleiben")
        country = root.find("ageblock-country")
        if country is None or country.findtext("country-default") != name:
            raise ValueError("Falsche Standard-Länderdatei")
        codes = {node.get("class"): node.findtext("country-code") for node in country.findall("country")}
        expected_codes = {"age-de.xml": "de"} if name == "age-de.xml" else {"age-de.xml": "de", "age.xml": "all"}
        if codes != expected_codes:
            raise ValueError("Falsche Länderzuordnung")
    print("XML, Scope, Fallback und Veröffentlichungsumfang geprüft.")


def check_live():
    for page in ("", "play.html", "impressum.html", "datenschutz.html"):
        url = "https://skanky0815.github.io/pixels-world/" + page
        with urlopen(url, timeout=20) as response:
            if response.status != 200 or response.url != url:
                raise ValueError(f"Unerwartete Antwort für {url}")
            if response.headers.get_content_type() != "text/html":
                raise ValueError(f"Kein HTML für {url}")
            html = response.read(2_000_000).decode("utf-8")
        parser = AgeMeta()
        parser.feed(html)
        if parser.values != ["age=6"]:
            raise ValueError(f"Alters-Metadaten fehlen oder sind uneindeutig: {url}")
        print(f"Live-Metadaten geprüft: {url}")


if __name__ == "__main__":
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--live", action="store_true")
    args = arguments.parse_args()
    try:
        check_files()
        if args.live:
            check_live()
    except Exception as error:
        raise SystemExit(f"Host-Prüfung fehlgeschlagen: {error}") from error

# Host-Konfiguration für skanky0815.github.io

Dieses Repository bereitet die Altersdateien am Host-Wurzelpfad für
[Pixel’s World](https://skanky0815.github.io/pixels-world/) vor. Die Spieladresse
und der getrennte Spiel-Release bleiben erhalten. Bezug:
[pixels-world#252](https://github.com/Skanky0815/pixels-world/issues/252),
[Spiel-PR #286](https://github.com/Skanky0815/pixels-world/pull/286).

## Konfiguration und Grenze

`public/age-de.xml` und `public/age.xml` erlauben die HTML-Meta-Auswertung für
`skanky0815.github.io/pixels-world` und `skanky0815.github.io/pixels-world/*`.
Die vier Spielseiten müssen `age-meta-label` mit `age=6` ausliefern. Andere
Projekte erhalten dadurch keine pauschale Einstufung „ab 6“.

Der Sicherheits-Fallback **18** greift bei fehlenden/unerkannten Angaben. Seine
mögliche Wirkung auf andere Pfade des gemeinsamen Hosts muss vor der
Veröffentlichung berücksichtigt werden: Die Pfadbegrenzung ist keine Zusage,
dass jedes Filterprogramm alle anderen Projekte unverändert behandelt.
Eine spätere Erweiterung benötigt die jeweilige Inhaltsbewertung.

Die Dateien folgen der [Dokumentation zur Einzelseiten-Einstufung](https://age-label.com/how-to/single-page-rating)
und den [JusProg-Hinweisen](https://www.jugendschutzprogramm.de/webseite-labeln/).
Die strukturelle XML-Prüfung ist keine Bestätigung der tatsächlichen Filterwirkung
und beantwortet keine organisatorische Rechtsfrage nach § 7 JMStV.

## Prüfen und nach Review veröffentlichen

1. `python3 tools/check_host.py` prüft Dateien, Scope und Fallback lokal und im PR.
2. Zuerst Spiel-PR #286 reviewen, mergen und regulär als Spielversion veröffentlichen.
3. `python3 tools/check_host.py --live` prüft anschließend alle vier öffentlichen
   Spielseiten auf ihre Alters-Metadaten. Fehlende Angaben stoppen die Bereitstellung.
4. Nach Review dieses Host-PRs unter **Pages** die vorbereitete Quelle
   **GitHub Actions** kontrollieren. Danach den Workflow **Host veröffentlichen**
   manuell auf `main` starten. Er prüft lokal und live, bevor er ausschließlich
   `public/` als Pages-Artefakt veröffentlicht. PRs und Pushes veröffentlichen nichts.
5. Danach HTTP-Status und XML-Inhalt von `/age-de.xml` und `/age.xml`, beide
   Spieleinstiege sowie echte Erkennung/Altersgrenzen in einem geeigneten
   Jugendschutzprogramm prüfen. Zusätzlich die Wirkung auf andere Projektpfade prüfen.

Die Altersdateien liegen bis zur separaten Freigabe nur im Review-Branch. GitHub
aktiviert User-Pages beim Anlegen des entsprechend benannten Repositorys automatisch;
die Quelle wurde deshalb von der automatischen Branch-Veröffentlichung auf
[GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
umgestellt. Der vorbereitete Veröffentlichungsworkflow wird erst nach Review manuell
gestartet. Es werden keine Domain-, Redirect- oder hostweiten robots.txt-Einstellungen angelegt.

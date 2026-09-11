# W55-R6: Externes Eingangsarchiv

Auftrag: neue Originaldatei-Kopien plus Pfad/Hash/Klartext anstelle großer
Base64-JSON-Blöcke ermöglichen; historische Archive erhalten.

Der installierte Helfer umfasste 83 Zeilen und war nicht im öffentlichen Paket.
Sein CLI-/Ledger-/Base64-Verhalten wurde übernommen. Die beiden kleinen
Lese-/Hashfunktionen liegen im neuen Helfer, weil das öffentliche
`handoff_common.py` nur den schon verwendeten atomaren Publisher enthält.
Keine Installation und keine Änderung dieser gemeinsamen Datei.

Neu: optional `snapshot --archive-dir`, JSON-Version 2 mit relativem
`archive_path`, unveränderte hashbenannte Originalkopien und Klartext. Legacy-
Version 1 bleibt Standard ohne Option und wird weiter geprüft. Vorhandene
Snapshots werden abgelehnt; gleiche Archivbytes werden wiederverwendet,
abweichende vorhandene Archive nicht ersetzt. Mehrdateien-Publikation ist keine
Gesamttransaktion: bei Fehlern können schon gesicherte Originalkopien verbleiben.

TDD: vier anfängliche CLI-Tests; drei externe Fälle wegen unbekannter Option rot,
Legacyfall grün. Nach Umsetzung sieben Tests grün, darunter echte RTF-Extraktion,
Byte-/Klartextkorruption, fehlende Archive, Unveränderlichkeit vorhandener Dateien,
gemeinsames Verschieben von Snapshot/Archiv sowie Ledger beider Formate.
Befehl: `python3 -m unittest discover -s tests -p test_handoff_inputs.py`.
Die Tests fanden zusätzlich die macOS-Pfadalias-Falle `/var` versus `/private/var`;
relative Archivpfade werden daher aus dem aufgelösten Snapshot-Verzeichnis gebildet.

Kein altes Archiv, keine Nutzerquelle und keine installierte Skilldatei verändert.
Keine Swift-Builds. Speicherformat vermeidet Base64-Diffs; reale Token-/Quoten-
Einsparung wurde nicht gemessen.

# Warm-Handoff-Projektvereinbarung

Übernimm nur Regeln, die das Projekt annimmt. Ersetze Platzhalter in eckigen Klammern. Diese Vorlage erteilt selbst keine Rechte.

<!-- rule:AG-01 -->
## Start und Fortsetzung

- Lies bei Sitzungsstart und vor dem Handoff `[Pfad der Handoff-Vereinbarung]` und das jüngste benannte Handoff.
- Behandle das gespeicherte Handoff und spätere Nutzernachrichten als geordneten Eingangsstrom.
- Lies `[Feedbackpfad]` an natürlichen Kontrollpunkten und direkt vor Abschluss vollständig.
- Erhalte Nutzeroriginale wörtlich; schreibe Agentenantworten und Deutungen in getrennte Abschnitte.

- Erzeuge jedes RTF-Handoff mit `scripts/handoff-rtf.sh` aus dem Skill-Verzeichnis gemäß [RTF-Sicherheit](../references/rtf-macos.de.md); ersetze dies nie durch direkte Erzeugung mit `textutil`.

Beim Wellenstart die Zwischenrufe-Datei als `.md` im Projektstamm anlegen und in einem Editor öffnen, in den der Nutzer schreiben kann (macOS: `open -a TextEdit "<voller Pfad>"`, nie in einem reinen Lese-Viewer wie dem cmux-Markdown-Tab), nie als RTF-Eingang; sie ist bis zum nächsten Handoff der einzige Eingang. Nur gespeicherte Ergänzungen lesen; Antworten in dieselbe Markdown-Datei anhängen, mit `Neue Zwischenrufe gelesen: ja/nein`, `ZWISCHENRUFE BIS HIER BEARBEITET — <Uhrzeit>` und `AB HIER NEUE ZWISCHENRUFE` plus leerer `>>>`-Zeile. Bei ungespeichertem oder unbekanntem Editorstand das Anhängen zurückstellen; nie selbst speichern oder schließen. Nach HF-07.

<!-- rule:AG-02 -->
## Umfang und Besitz

- Arbeite nur innerhalb der Nutzerautorisierung und zugewiesenen Pfade.
- Jede beschreibbare Datei gehört genau einem Agenten. Stoppe und melde, bevor du einen fremden Pfad berührst.
- Leite keine Erlaubnis zu Installation, Veröffentlichung, Push, UI-Steuerung, Kontaktaufnahme oder destruktiver Arbeit ab.
- Serialisiere Kommandos mit gemeinsamem `[Build-Lock oder veränderlicher Ressource]`.

Arbeiteraufträge erhalten die geltenden Nutzerregeln; ein Chef darf sie nicht still außer Kraft setzen. Konflikte mit Hostrechten benennen. Wellennummern folgen einer gemeinsamen Folge je Projekt über alle Hosts; die nächste freie Nummer im gespeicherten Plan reservieren (WV-01).

<!-- rule:AG-03 -->
## Optionaler Wächtermodus

- Wächtermodus: `[aktiv / inaktiv]`.
- Wenn aktiv, laufen substanzielle Recherche, Analyse, Umsetzung, QA, Sichtprüfung, Berichte und Handoff-Erstellung über Wächter und Arbeiter.
- Die Hauptsession übernimmt knappe Koordination, notwendige Entscheidungen und gebündelte Abnahme ohne doppelte Detailarbeit.
- Nutze kurze eigenständige Briefe, automatische Fertigmeldung und keine Statusfrage vor 25 Minuten außer bei Blockade.
- Beachte tatsächliche Hostplätze; stelle Arbeit an oder verkleinere sie bei fehlender Kapazität.

<!-- rule:AG-04 -->
## Belege und Abschluss

- Prüfe Repository-Stand, geänderte Pfade, Tests und gespeicherte Berichte vor einer Erledigt-Meldung.
- Trenne API-Fakten, Client- oder Hostgrenzen und Messwerte der aktuellen Sitzung.
- Schreibe den geforderten dauerhaften Bericht nach `[Berichtspfad]`.
- Nenne erledigte, offene, laufende und blockierte Arbeit sowie den nächsten Einstieg.

Hostspezifische Ergänzungen gehören in den aktiven Adapter: [Codex](../references/codex.de.md) oder [Claude Code](../references/claude-code.de.md).

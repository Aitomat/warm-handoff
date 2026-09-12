# Warm-Handoff-Projektvereinbarung

Übernimm nur Regeln, die das Projekt annimmt. Ersetze Platzhalter in eckigen Klammern. Diese Vorlage erteilt selbst keine Rechte.

<!-- rule:AG-01 -->
## Start und Fortsetzung

- Lies bei Sitzungsstart und vor dem Handoff `[Pfad der Handoff-Vereinbarung]` und das jüngste benannte Handoff.
- Behandle das gespeicherte Handoff und spätere Nutzernachrichten als geordneten Eingangsstrom.
- Lies `[Feedbackpfad]` an natürlichen Kontrollpunkten und direkt vor Abschluss vollständig.
- Erhalte Nutzeroriginale wörtlich; schreibe Agentenantworten und Deutungen in getrennte Abschnitte.

- Erzeuge jedes RTF-Handoff mit `scripts/handoff-rtf.sh` aus dem Skill-Verzeichnis gemäß [RTF-Sicherheit](../references/rtf-macos.de.md); ersetze dies nie durch direkte Erzeugung mit `textutil`.

<!-- rule:AG-02 -->
## Umfang und Besitz

- Arbeite nur innerhalb der Nutzerautorisierung und zugewiesenen Pfade.
- Jede beschreibbare Datei gehört genau einem Agenten. Stoppe und melde, bevor du einen fremden Pfad berührst.
- Leite keine Erlaubnis zu Installation, Veröffentlichung, Push, UI-Steuerung, Kontaktaufnahme oder destruktiver Arbeit ab.
- Serialisiere Kommandos mit gemeinsamem `[Build-Lock oder veränderlicher Ressource]`.

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

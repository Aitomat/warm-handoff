---
name: warm-handoff-full-de
description: Führt den vollständigen Warm-Handoff-Ablauf für verlustfreie Fortsetzungen, editierbare Übergabedokumente, belegorientiertes Modellrouting und autorisierte Multi-Agenten-Wellen aus.
---

# Warm Handoff — vollständiger Ablauf

Nutze diese Variante zur Einführung oder Prüfung des Ablaufs. Für Routinerunden ist der kurze Skill `warm-handoff-de` vorgesehen. Die stabilen Regel-IDs entsprechen der kurzen englischen und deutschen Fassung. Referenzlinks sind relativ zur Paketwurzel: Installiere diese Datei als `SKILL.md` zusammen mit den für `full-de` in `docs/language-matrix.json` deklarierten Ressourcen.

<!-- rule:WH-01 -->
## 1. Umfang feststellen

1. Lies vor dem Handoff die Anweisungsdateien des Repositorys.
2. Bestimme das jüngste Handoff, die darin benannte Feedback- oder Zwischenrufe-Datei und spätere Nutzernachrichten.
3. Halte Ziel, erlaubte und verbotene Aktionen, eigene Pfade, erwartete Artefakte, Prüfkommandos und Liefergrenze fest.
4. Prüfe aktuellen Branch, Arbeitsbaum und relevante Dateien, bevor du Erledigt-Aussagen glaubst.

Behandle die Quellen als geordneten Strom. Spätere Anweisungen können frühere präzisieren, ohne erhaltenen Nutzertext zu löschen. Ein Handoff überträgt Kontext und Entscheidungen; es erweitert keine Rechte. Frage nur, wenn erforderliche Information nicht ableitbar ist oder unabhängige Arbeit nicht mehr weitergehen kann.

Wähle für diesen Lauf genau einen Provider-Adapter: [Codex](references/codex.de.md) oder [Claude Code](references/claude-code.de.md). Vermische keine hostspezifischen Befehle mit dem Kernablauf.

<!-- rule:WH-02 -->
## 2. Verlustfrei fortsetzen

Lies jede gespeicherte Quelle vollständig. Importiere RTF unter macOS vollständig mit `textutil`; Ausschnitte oder Terminalvorschauen reichen nicht. Erhalte Nutzerblöcke bytegleich, wenn ein Bytearchiv gefordert ist, und wörtlich im lesbaren Handoff. Schreibe Deutung, Entscheidungen und Antworten in getrennte, benannte Abschnitte.

Vor dem Handeln:

- gleiche Duplikate und späte Ergänzungen ab;
- trenne ausdrückliche Entscheidungen von Vorschlägen und Agentenschlüssen;
- prüfe referenzierte Commits, Dateien, Testergebnisse und laufende Arbeit;
- kennzeichne veralteten, unbekannten oder ungeprüften Stand ehrlich;
- halte Geheimnisse und irrelevanten Gesprächsverlauf aus dem nächsten Handoff heraus.

Erzeuge ein neues datiertes Handoff, statt eine beantwortete Quelle zu bearbeiten. Die Kopierzeile oben soll den absoluten Pfad des neuen Handoffs nennen. Nimm erhaltene Nutzersammlung, aktuelles Ziel und Grenzen, belegte Lieferungen, offene oder laufende Arbeit, offene Entscheidungen, Testanweisungen, knappe Erinnerung und den Sammelbereich für die nächste Sitzung auf. Siehe [Handoff-Format](references/handoff-format.de.md). **Pflicht (14.09.2026):** Lies `references/handoff-format.de.md` vollständig, bevor du schreibst, und lies das vorherige Handoff ungefiltert — nie Zeilen abschneiden, nie nur nach `>>>Userantwort:` greppen. Die verbindliche 17-teilige Abschnittsfolge steht in der Referenz (HF-06). Am Wellenende nicht auf Agentenmeldungen warten, sondern abschließen.

<!-- rule:WH-03 -->
## 3. Innerhalb der Autorisierung arbeiten

Arbeite weiter, bis das autorisierte Ergebnis vollständig ist. Ein brauchbares Arbeitspaket hat ein konkretes Ziel, exklusive Dateien, Abhängigkeiten, Akzeptanzkriterien, verbotene Aktionen und einen geforderten Bericht. Teile Arbeit nur bei unabhängigen Paketen. Beachte die tatsächlichen Agentenplätze des Hosts und Ressourcengrenzen der Maschine; Bezeichnungen oder Pläne schaffen keine Kapazität.

Nutze direkte Arbeiter für unabhängige Umsetzung. Setze einen Wächter nur ein, wenn mehrere Arbeiter interne Koordination oder Integration brauchen. Serialisiere gemeinsame Builds, veränderliche Umgebungen, Veröffentlichungen und andere umkämpfte Ressourcen. Lasse nie mehrere Agenten dieselbe Datei bearbeiten. Lies die Feedbackquelle vor der Endintegration erneut, weil der Nutzer eine weitere vollständige Revision gespeichert haben kann.

Wähle Modelle nach Aufgabenform und belegter Verfügbarkeit, nicht nach Hörensagen. Trenne veröffentlichte API-Spezifikation, wirksame Client- oder Hostgrenzen und Messwerte der aktuellen Sitzung. Aktuelle Plattformhinweise und Prüfdaten stehen in [Modellrouting](references/model-routing.de.md) und [Beleggrenzen](references/evidence-scope.de.md). Den vollständigen Paket- und Integrationsvertrag beschreibt [Wellen-Ausführung](references/wave-execution.de.md).

<!-- rule:WH-04 -->
## 4. Dokumentsicherheit erhalten

Markdown ist die vom Agenten geschriebene Quelle. Ein RTF-Zwilling kann unter macOS das editierbare Antwortdokument des Nutzers sein. Überschreibe nie eine bestehende Antwortdatei und folge keinem Ausgabe-Symlink. Rendere in eine temporäre Datei, prüfe Textroundtrip und Hyperlinkfelder und veröffentliche dann exklusiv.

Goldene Antwortabsätze beginnen mit `>>>`. Ein leerer Absatz direkt nach einem Antwortmarker muss ebenfalls den goldenen 18-Punkt-Stil tragen, damit dort eingegebener und mit Return fortgesetzter Text den Antwortstil behält. Der nächste vom Agenten geschriebene Absatz muss auf normalen Hintergrund zurücksetzen.

Trenne drei Aussagen:

1. Rendererprüfungen belegen erzeugten Text und RTF-Linkfelder;
2. ein AppKit-/TextEdit-Fortsetzungstest belegt Formatierung nach Eingabe, Return, Speichern und Neuladen;
3. das Einfügen in eine andere Anwendung braucht eigene manuelle oder anwendungsnahe Belege.

TextEdit zu öffnen oder Tabgruppen zu verändern ist eine UI-Aktion und braucht die Autorisierung des Auftrags. Siehe [RTF unter macOS](references/rtf-macos.de.md).

<!-- rule:WH-05 -->
## 5. Optionale Hilfen bewusst einsetzen

[Context Mode](references/context-mode.de.md) ist optional. Er kann große Dateien oder Befehlsausgaben verarbeiten und ein gezieltes Ergebnis zurückgeben. Prüfe drei Zustände unabhängig: ob das Paket installiert ist, ob seine MCP-Werkzeuge in dieser Sitzung aufrufbar sind und ob seine Hooks wirken. Ein erfolgreicher MCP-Aufruf belegt keine Hooks; ein vorhandenes Paket belegt keines von beidem. Installiere oder aktualisiere es nie ohne Erlaubnis.

<!-- rule:WH-06 -->
## 6. Mit Belegen abschließen

Am letzten sicheren Kontrollpunkt:

1. lies die benannte gespeicherte Feedbackquelle erneut;
2. prüfe Git und bestätige, dass nur eigene Pfade geändert wurden;
3. führe die geforderten zielgerichteten Prüfungen aus und halte genaue Ergebnisse fest;
4. prüfe jede Erledigt-Aussage anhand eines Artefakts oder Kommandos;
5. schreibe den dauerhaften Bericht an den geforderten Pfad;
6. nenne erledigte, offene, laufende und blockierte Arbeit sowie den nächsten Einstieg.

Gib Arbeit nicht als erledigt aus, nur weil ein Prozess gestartet wurde, eine Datei existiert oder ein anderer Agent einen Erfolg meldete. Wenn eine manuelle Prüfung nicht stattfand, lasse sie ausdrücklich offen.

Die spanische Übersetzung ist zurückgestellt. Audio, Video und Website-Material bleiben Zukunftsvorschläge und gehören nicht zu diesem Paket.

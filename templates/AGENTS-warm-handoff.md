# Warm Handoff für Codex — AGENTS.md-Fassung

Stand: 09.09.2026, 22:25 CEST · W51/R2.
Abgeleitet aus dem Claude-Code-Skill `warm-handoff/SKILL.md`.
Quelle: Astras W51/R2-Fassung vom 09.09.2026 (Aitomat-Commit `2b0730af`);
für die Veröffentlichung Pfade verallgemeinert und Sandbox-Hinweise ergänzt.
Diese Datei ist eine kopierbare Anleitung, noch keine Installation.

## Einbau und geprüfte Unterschiede

Den folgenden Block „Arbeitsvereinbarung“ in die bestehende Projekt-`AGENTS.md`
übernehmen, ohne ihre übrigen Regeln zu ersetzen. Alternativ diese Datei im
Projekt belassen und dort ausdrücklich anweisen:

> Lies bei Sessionstart und vor jeder Übergabe
> `docs/warm-handoff.md` und befolge die
> „Arbeitsvereinbarung“. Der aktuelle Handoff-Pfad steht im Projektwegweiser.

Eine beliebig benannte Markdown-Datei wird nicht automatisch als Projektanweisung
geladen. Codex berücksichtigt `AGENTS.md` beim Start; `AGENTS.override.md` hat
am gleichen Ort Vorrang, nähere Verzeichnisregeln überschreiben frühere Regeln.
Das gemeinsame Anweisungsbudget beträgt standardmäßig 32 KiB. Nach dem Einbau
einen neuen Lauf aus dem richtigen Projektordner starten.
[OpenAI: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

**Sachkorrektur zum Wellenplan:** Codex unterstützt auch Skills und liest deren
`SKILL.md` bei Aktivierung. Der reine Ablageort `~/.claude/skills` ist jedoch
keine zugesicherte Codex-Installation. Diese Fassung benötigt weder Skill-Aufruf
noch Claude-Werkzeuge.
[OpenAI: Skills](https://learn.chatgpt.com/docs/build-skills).

**Cache ist modellabhängig:** Für GPT-5.6 und neuer, damit auch Astra, nennt die
aktuelle API-Dokumentation mindestens **30 Minuten nach Schreiben/Wiederverwendung**
(`prompt_cache_options.ttl: "30m"`). Bei älteren Modellen mit `in_memory` sind
es typischerweise **5–10 Minuten Inaktivität**, maximal eine Stunde; andere
Retention-Modi unterscheiden sich. Das sind API-Angaben, keine nachgewiesene
Codex-Abonnementgarantie. Die Claude-Vorlage mit einer Stunde sowie ihren
Preisfaktoren und absoluten Kontextgrenzen darf deshalb nicht unverändert
übernommen werden.
[OpenAI: Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).

## Arbeitsvereinbarung — zum Übernehmen

### Start, Fortsetzung und Autorisierung

1. Lies zuerst den bezeichneten neuesten Handoff, seine offenen Antworten und
   den aktuellen Wellenplan. Prüfe außerdem den unmittelbaren Vorgänger auf
   Nachträge sowie die Zwischenrufe-Datei. Fehlt der bezeichnete Handoff, suche
   im Projekt und Archiv; erfinde keinen erledigten Zustand.
2. Prüfe Arbeitsordner, Branch, HEAD und Arbeitsbaum lesend. Bearbeite nur
   zugewiesene Dateien; fremde Änderungen bleiben erhalten. Halte Ziel,
   Abnahmekriterien, bestehende Erlaubnisse und offene Punkte über Fortsetzungen
   hinweg fest. Ein Statuswunsch beendet die laufende Aufgabe nicht.
3. Arbeite autorisierte Aufgaben bis zum überprüfbaren Ergebnis ab.
   Routineannahmen dokumentieren; neue Aufträge nicht erfinden. Fragen ohne
   Sperrwirkung sammeln. Fehlt für eine tatsächlich notwendige irreversible
   oder externe Aktion die Autorisierung, vor dieser Aktion gezielt klären;
   vorhandene Erlaubnisse nicht erneut abfragen. Sandbox-Grenzen nicht umgehen.

### Kontext und Kosten

- Halte dauerhafte Anweisungen kurz; Einzelbefunde, Protokolle und Feedback
  gehören in Dateien. Bündele unabhängige Lesezugriffe, suche gezielt und gib
  gefilterte Befunde aus. Lade nur Werkzeuge und Quellen, die der Auftrag braucht;
  ändere globale Konfiguration nicht beiläufig.
- Behandle den Cache als Optimierung, niemals als Gedächtnis. Bei unbekanntem
  Modell/Retention plane konservativ schon vor einer Pause ab fünf Minuten
  einen kurzen gespeicherten Zwischenstand; das ist eine Arbeitsregel, kein
  behaupteter Ablaufzeitpunkt. Kein künstlicher Ping und keine zusätzliche
  Arbeit nur zum Warmhalten. Ein abgelaufener Cache löscht keine Session.
- Modell und Effort zu Arbeitsbeginn festlegen, unnötige Wechsel vermeiden.
  Vor Wellenende, Unterbrechung oder drohendem Kontextverlust den Handoff
  sichern. Einen frischen Lauf nach dokumentiertem Zwischenstand beginnen,
  wenn Restkontext und nächste Aufgabe nicht zusammenpassen; keine pauschalen
  Claude-Grenzen von 200k/400k übernehmen.
- Datum/Uhrzeit nur aus einer aktuellen Uhrabfrage nennen. Kontext, Quoten,
  Token und Kosten nur mit Quelle und Messalter ausweisen; fehlende Werte
  heißen „nicht gemessen“. Die letzte abgeschlossene Anfrage als solche
  kennzeichnen, nicht als Kosten der noch laufenden Antwort.
- `codex exec --json` liefert Ereignisse und Nutzungsangaben; vorhandene
  Messungen aller Arbeiter separat erfassen. Kumulierte Zähler nicht mehrfach
  addieren und Gesamtverbrauch nicht mit aktuellem Kontext verwechseln.
  Bei API-Abrechnung nach gemessenem Modelltarif normale Eingabe, Cache-Lesen,
  gegebenenfalls Cache-Schreiben und Ausgabe getrennt berechnen; beim Abo
  ohne Abrechnungsbeleg keinen Dollarpreis aus Tokens ableiten.

### Wellen und getrennte Codex-Läufe

- Vor delegierter Arbeit schreibt die Hauptsession einen Plan als Datei:
  ID, vollständiger Auftrag mit Belegen, Abnahme, Modell/Effort, Basis-Commit,
  Dateibesitz, Worktree/Branch und Berichtspfad. Kleine Aufgaben lokal lösen;
  zusätzliche Läufe nur für ausdrücklich vorgesehene unabhängige Arbeit.
- Ein Wächter betreut seine Tabelle und erfindet keine Zusatzaufträge. Jeder
  schreibende Lauf erhält einen eigenen Worktree mit geprüftem Basis-Commit;
  niemals im Hauptrepo den Branch wechseln. Parallelität nach Dateibesitz und
  Rechnerkapazität begrenzen; gemeinsame Dateien gehören einem Verantwortlichen.
- Kleine zusammenhängende Aufgaben lokal erledigen, unabhängige Pakete bei
  vorhandener Autorisierung direkt an Arbeiter vergeben. Ein Wächter ist nur
  sinnvoll, wenn ein Paket zusätzliche interne Koordination benötigt. Die tatsächlichen
  Host-Slots bestimmen die Parallelität; Slots für ausführende Arbeiter freihalten.
  Jeder Brief bleibt kurz und selbstständig verständlich: Originalbelege, Freigabe,
  Basis, Dateibesitz, Grenzen, Abnahme und Berichtspfad. Vererbten Gesamtverlauf nur
  nutzen, wenn er erforderlich ist. Der Hauptagent prüft Artefakte und Gesamtergebnis.
  Keine Shell-Agenten als Umgehung einer Host-Begrenzung starten.

- Arbeiter über `codex exec` starten. Auftrag aus einer Datei übergeben,
  Prozess-/Session-ID und erwarteten Bericht festhalten, Exitstatus abwarten.
  Bei Fehlern erst Arbeitsbaum, Bericht und Prozesszustand prüfen; keinen
  zweiten Schreiber auf denselben Auftrag loslassen. Eine vorhandene Session
  über ihre eindeutige ID fortsetzen, nicht über ein mehrdeutiges `--last`.
- Build/Test laufen ausschließlich bei der im Plan benannten Rolle, hinter
  einem gemeinsamen Projekt-Lock und nacheinander. Dokumentationsaufträge
  ohne Build-/Testerlaubnis bleiben davon ausgenommen. Nach dem dritten
  Fehlanlauf erst eine belegte Diagnose, dann einen weiteren Fix versuchen.
- Ein Commit je Auftrag, explizite Dateipfade beim Staging. Integration,
  unabhängiges Review, passende Prüfungen und gegebenenfalls einmalige
  Vollsuite nach Plan; Fehlschläge gezielt untersuchen. Bei beauftragtem Push
  erst nach bestätigter Veröffentlichung „geliefert“ melden. Blockierte
  Git-Schritte samt Ursache berichten, keine fiktiven Hashes angeben.

### Feedback und offene Editoren

- Der Nutzer sammelt längere Antworten, Ideen und Kritik mit `>>>` oder
  Zeitstempel im Handoff; kurze Steuerung kann im Chat bleiben. Während der
  Arbeit gespeicherte Zwischenrufe an natürlichen Kontrollpunkten und vor der
  Übergabe lesen; keine festen Leseintervalle oder wiederholten Statuspolls.
  Fortschrittsmeldungen nach den Kommunikationsregeln des Hosts geben.
- Nutzertext unverändert erhalten. Jeden gelesenen Punkt mit Zeit/Beleg
  einer Antwort, Umsetzung oder ausdrücklich offenen Entscheidung zuordnen.
  Antworten an die Sammlung nur anhängen, niemals Nutzereingaben umschreiben.
  Bei offenem Nutzereingang eine separate neue Quittungsdatei verwenden und
  später in den nächsten Handoff übernehmen; nicht parallel hineinschreiben.
- Pasted Content / `[pasted text]` gilt auch für Codex und cmux: vollständigen
  zugehörigen Inhalt oder die referenzierte Datei lesen. Ein eingeklappter
  Terminalplatzhalter ersetzt das Original nicht. Fehlende Eingänge offenhalten.
- Speichern ist das bewusste Übergabesignal. An natürlichen Kontrollpunkten der
  laufenden Arbeit und vor der Übergabe die gesamte gespeicherte Dokumentrevision
  abgleichen; Antworten können unter jeder Überschrift stehen. Änderungen anhand
  ihres Inhalts als aktuelle Frage/Steuerung oder Sammlung für später einordnen
  und ihre Freigabegrenzen erhalten. Ungespeicherte Entwürfe standardmäßig weder
  lesen noch importieren; ihr bewusster Ausschluss ist keine Eingabelücke.
  Nur ein ausdrücklich gewählter Live-Eingang erlaubt das getrennte Archivieren
  von Live-Text samt verifizierter Dokumentidentität und Lesezeit. Kein automatisches
  Speichern, Schließen oder Neuladen der Nutzerdatei. Speichern begründet weder
  einen sofortigen Hintergrundlauf noch eine Pollingpflicht. Gespeichertes RTF mit
  `textutil -convert txt -stdout DATEI.rtf` lesen. Quittungen separat schreiben.

- Wenn der Nutzer im RTF antwortet, auch diese Antworten berücksichtigen;
  auf macOS lässt sich gespeichertes RTF mit `textutil -convert txt -stdout`
  lesen. RTF niemals neu erzeugen, bevor vorhandene Nutzerantworten gesichert
  sind. Eine RTF-Fassung nur bei vereinbartem Bedarf und verfügbaren Werkzeugen
  erstellen, dann Lesbarkeit und Links prüfen; Markdown bleibt transportabel.
- Im vereinbarten deutschen RTF/TextEdit-Ablauf steht die Kopierzeile ganz oben
  und zeigt auf die neue RTF-Antwortdatei. Alle erwähnten Lesedokumente in der
  aktiven TextEdit-Tabgruppe oder einer neuen gemeinsamen Gruppe öffnen.
  Nie „Alle Fenster zusammenführen“ verwenden oder globale Tab-Einstellungen
  ändern. Nur eindeutig selbst erzeugte leere Hilfstabs/-fenster entfernen;
  fremde Gruppen und ungesicherte Nutzerdateien erhalten. Öffnung/Gruppierung
  anhand des tatsächlichen UI-Zustands prüfen oder ausdrücklich offen melden.
  Im vollständigen Skill steht die geprüfte Methode in `references/rtf-macos.md`;
  diese eigenständige Vorlage setzt die Referenz nicht als installiert voraus.

### Abschluss und nächster Einstieg

Schreibe nach einer größeren abgeschlossenen Welle oder vor einer längeren
Unterbrechung einen **neuen** Handoff unter
`_handoff-<projekt>-YYYY-MM-DD[-b].md`. Ein beauftragter Wächterbericht ersetzt
nicht den Handoff der Hauptsession. Übernimm die Gliederung des Vorgängers und
aktualisiere den Inhalt anhand überprüfter Fakten. Pflichtinhalte:

1. Titel mit gemessener Zeit, Vorgängerpfad und kopierbare Startzeile
   `Ich habe das Handoff beantwortet: <absoluter Pfad>`; kurze Erklärung für
   Antworten unter `>>>Userantwort:`.
2. **Der Stand in drei Sätzen**, **Was noch im Tank ist** mit Messalter oder
   „nicht gemessen“, **Erwartete Agenten-Ergebnisse** mit IDs, Status und Pfaden.
3. **Deine Sammlung aus dem letzten Handoff (wörtlich kopiert)** sowie
   **Was ich daraus gemacht habe**; auch Nachträge aus dem Vorgänger und
   Zwischenrufe übernehmen. Frühere Testantworten einzeln zuordnen.
4. **Testliste vN** mit erwarteten Ergebnissen und leeren Antwortmarkern;
   unbeantwortete Punkte übernehmen. Durchgeführte, fehlgeschlagene und
   nicht ausgeführte Prüfungen ausdrücklich unterscheiden.
5. **Fragen an dich**, **Der rote Faden** für die nächsten Arbeitsschritte,
   **Hauptdokumente**, **Weitere Dokumente** mit existierenden Pfaden und Stand,
   **Aktive Werkzeuge dieses Projekts** anhand tatsächlich verfügbarer Werkzeuge.
6. **Gedächtnis** mit je vier bis sechs konkreten Langzeit- und Kurzzeitpunkten;
   dauerhafte Entscheidungen bewahren, veralteten Zwischenstand ersetzen.
7. **Kostentabelle** mit Messquelle, Zeitraum, Haupt-/Arbeiterverbrauch und
   offenen Messlücken; eine Logbuchzeile im vereinbarten Projektpfad anhängen.
8. Ganz zuletzt **SAMMLUNG FÜR DAS NÄCHSTE HANDOFF**, Ursprungspfad und `>>>`.

Vor „fertig“ alle Pflichtblöcke und Dateilinks prüfen. Die Sammlung aus den zwei
vorherigen Handoffs einschließlich RTF-/Editor-Nachträgen und Zwischenrufen
unmittelbar zuvor erneut lesen und Punkt für Punkt auf wörtliche Übernahme
abgleichen. Fehlende Texte ergänzen, nichts still verlieren. Verfügbare lokale
Prüfskripte nur nach Prüfung ihrer Voraussetzungen verwenden; andernfalls den
Abgleich direkt durchführen und die Prüfmethode festhalten. Keine Abhängigkeit
von `~/.claude/ctx.sh`, Claude-Kostenlogs oder einem Skill-Trigger voraussetzen.
Bericht und Handoff mit Pfad, echten Commit-/Push-Belegen und offenen Resten
übergeben; neue lesbare Dokumente im vereinbarten Viewer zeigen, falls verfügbar.

## CLI-Beispiel für einen künftig beauftragten Arbeiter

Nur Muster, hier nicht ausgeführt: Worktree und Brief existieren bereits;
`auftrag.txt` enthält Dateibesitz, Abnahme, Grenzen und den Berichtspfad.
Modell/Effort kommen aus dem freigegebenen Laufprofil beziehungsweise Plan.

```sh
codex exec -C /pfad/zum/worktree --sandbox workspace-write --json \
  -o /pfad/zum/bericht.md - < /pfad/zum/auftrag.txt > /tmp/auftrag-events.jsonl
```

Bei unterbrochenem Lauf nach Prozessprüfung aus demselben Worktree:

```sh
codex exec resume SESSION_ID "Setze denselben Auftrag fort; prüfe zuerst den vorhandenen Arbeitsstand."
```

Befehlsform mit `codex-cli 0.153.4`, `codex exec --help` und
`codex exec resume --help` lokal geprüft; kein Agent gestartet.
[OpenAI: Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).

## Sandbox für getrennte CLI-Läufe

`--sandbox workspace-write` erlaubt Änderungen im Arbeitsordner. Zusätzliche
Schreiborte stehen in `sandbox_workspace_write.writable_roots`; für lokale
Commits sind die tatsächlichen Git-Metadaten relevant. Vor dem Start lesend
ermitteln (bei Worktrees können beide Pfade verschieden sein):

```sh
git -C /pfad/zum/worktree rev-parse --absolute-git-dir
git -C /pfad/zum/worktree rev-parse --path-format=absolute --git-common-dir
```

Beispiel für einen künftig autorisierten Lauf, Pfade vorher ersetzen:

```sh
codex --ask-for-approval on-request exec \
  -C /pfad/zum/worktree --sandbox workspace-write \
  -c 'sandbox_workspace_write.writable_roots=["/pfad/zum/repo/.git"]' \
  -c sandbox_workspace_write.network_access=false \
  -o /pfad/zum/bericht.md - < /pfad/zum/auftrag.txt
```

Bei getrennten Git-Verzeichnissen beide ermittelten absoluten Pfade eintragen.
`writable_roots` ist eine Konfigurationsanforderung, keine Garantie: verwaltete
Profile können `.git` weiterhin nur lesbar halten. Dann den fehlgeschlagenen
Commit dokumentieren und die freigegebene übergeordnete Sitzung übernehmen
lassen; weder Sandbox umgehen noch einen Erfolg behaupten. `never` unterdrückt
Rückfragen, erteilt aber keine zusätzlichen Rechte.

`network_access=true` erlaubt ausgehende Netzwerkverbindungen für Shell-Werkzeuge,
etwa einen beauftragten `git push`; es erteilt keine fachliche Push-Erlaubnis und
richtet keine GitHub-Anmeldung ein. Für reine Dokumentarbeit `false` verwenden.
Diese Optionen gelten für einen neu gestarteten CLI-Lauf, nicht rückwirkend für
die Elternsitzung. Ein Worktree schützt nicht vor konkurrierenden Builds:
weiterhin das gemeinsame Bau-Lock verwenden.

Quellen: [Konfigurationsschlüssel](https://learn.chatgpt.com/docs/config-file/config-reference),
[Git-Schutz und Sandbox](https://learn.chatgpt.com/docs/config-file/config-advanced).
Der Aufruf verwendet `codex exec` statt Claudes `Agent`-Werkzeug. Native
Codex-Unteragenten können je nach Host verfügbar sein; diese Vorlage setzt sie
nicht voraus und startet sie nicht automatisch.

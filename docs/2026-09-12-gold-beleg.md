# Gold-Beleg — W56 F3, 12.09.2026

## Ursache und Korrektur

Ausgangsstand: `0ea4424`, Branch `w56-f3`. `scripts/handoff-rtf.sh` delegiert an `scripts/render_rtf.py`. Die alte Bedingung färbte neben `>>>` nur eine unmittelbar folgende Leerzeile. Nichtleere Fortsetzungen verloren Gold und beendeten den Fortsetzungszustand.

Jetzt bleibt der Zustand über nichtleere Fortsetzungszeilen erhalten. Annahme zur Quellsyntax: Eine Leerzeile beendet die Antwort und bleibt selbst golden als Eingabefeld; Überschrift, Codeblockgrenze oder `<!-- answer:end -->` beenden sie vor fremdem Text. Ohne solche Grenze kann der Renderer die Autorenschaft freien Texts nicht erkennen. Mehrere Nutzerabsätze mit Leerzeilen oder wörtlichem Markdown gehören in einen `user-original`-Block. Jede Zeile darin war bereits golden und bleibt es.

Die Codex-Adapter und AGENTS-Vorlagen enthielten keinen direkten `textutil`-Erzeugungsaufruf, aber auch keine verbindliche Wrapper-Anweisung. Diese Lücke ist in EN und DE geschlossen: RTF immer über `scripts/handoff-rtf.sh`; direktes `textutil` dient nur dem Lesen/Prüfen. Die RTF-Referenzen beschreiben die Antwortgrenzen synchron.

## Quelle

Persistierte Testquelle: `tests/fixtures/f3-gold.md`, wortwörtlich:

````text
>>>Answer: First answer line
Second answer line
Third answer line

Agent after blank
>>>Answer: Before heading
# Agent heading
Agent after heading
>>>Answer: Before explicit end
<!-- answer:end -->
Agent after explicit end
>>>Answer: Before code
```
Agent code
```
<!-- user-original:start -->
Old user message

# Old literal heading
Old user wish
<!-- user-original:end -->
Agent after original
````

## Kommandos und Ausgaben

Arbeitsverzeichnis: `/private/tmp/warm-handoff-w55-r7`.

```console
$ python3 scripts/render_rtf.py tests/fixtures/f3-gold.md /tmp/f3-gold.rtf
/tmp/f3-gold.rtf — text roundtrip and 0 hyperlink fields verified; viewer QA pending
$ grep -c 'cbpat1' /tmp/f3-gold.rtf
11
```

Beide Kommandos: Exitcode 0. `tests/test_rtf_gold_lines.py` ruft den Wrapper auf und führt `grep -c cbpat1` einzeln für jede der neun erwarteten nichtleeren Nutzerzeilen aus (> 0). Zwei zusätzliche goldene Leerabsätze ergeben zusammen elf. Alle Agentenzeilen müssen ohne `cbpat1` bleiben. Der bestehende Cocoa-Test prüft weiterhin den Goldhintergrund alter Originaltexte nach Speichern/Neuladen. Sein Agentenabsatz nutzt jetzt die ausdrückliche Antwortgrenze.

Testweg laut README: `python3 -m unittest discover -s tests -v`; ausgeführt mit derselben Discovery ohne ausführliche Einzelnamen. Erster Lauf: 47 Tests, ein Fehler im vorhandenen Swift-AppKit-Probetest wegen nicht beschreibbarem `/Users/pro16/.cache/clang/ModuleCache`; zusätzlich meldete Swift einen SDK/Compiler-Folgefehler. Deshalb Wiederholung mit Cache-Verzeichnissen unter `/tmp`. Es wurden weder `swift build` noch `swift test` ausgeführt. Keine Nutzerdatei oder installierter Skill wurde geändert, keine Editorfenster wurden geöffnet. Eine manuelle TextEdit-Sichtprüfung wird nicht behauptet.

Vollständige Ausgabe des erfolgreichen Wiederholungslaufs (Exitcode 0):

```console
$ CLANG_MODULE_CACHE_PATH=/tmp/f3-clang-cache SWIFT_MODULECACHE_PATH=/tmp/f3-swift-cache python3 -m unittest discover -s tests
...............................................
----------------------------------------------------------------------
Ran 47 tests in 73.931s

OK
```

`git diff --check` lieferte keine Ausgabe (Exitcode 0). Veröffentlichung erfolgt durch den Wächter; dieser Auftrag endet mit lokalem Commit ohne Push.

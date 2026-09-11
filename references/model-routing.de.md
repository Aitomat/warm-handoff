# Modellrouting

<!-- rule:MR-01 -->
## Nach Aufgabe und Beleg routen

Wähle ein Modell nach benötigter Denktiefe, Latenz, Werkzeugnutzung und belegter Verfügbarkeit. Nutze für begrenzte Umformungen ein günstigeres oder schnelleres Modell und für mehrdeutige Integration oder Review ein stärkeres Modell nur, wenn der Host es anbietet. Schreibe keine persönliche Modellaufstellung als allgemeine Regel fest.

<!-- rule:MR-02 -->
## Drei Bereiche trennen

1. **API-Spezifikation:** veröffentlichtes Modell-Kontextfenster, Funktionen und API-Preise.
2. **Client- oder Hostgrenze:** Modelle, Reasoning-Einstellungen, Kontext, Kontingente, Caching und Werkzeuge des aktuellen Produkts.
3. **Sitzungsmessung:** Anfragen, Token, Cacheverhalten, Laufzeit oder Kosten dieses Laufs.

Übertrage keinen Bereich ohne direkten Beleg auf einen anderen. Unbekannte wirksame Grenzen bleiben unbekannt.

<!-- rule:MR-03 -->
## Aktuell geprüfte Hinweise

Am 11.09.2026 ausschließlich anhand offizieller Primärdokumentation geprüft:

- OpenAI-API-Seiten nennen für GPT-6 Astra und GPT-5.6 Sol Kontextfenster von 1.050.000 Token. Das bestimmt keine Codex-Hostgrenze.
- OpenAI dokumentiert beim API-Prompt-Caching für GPT-5.6 und neuer mindestens beziehungsweise standardmäßig 30 Minuten Aufbewahrung und automatisches Caching geeigneter Präfixe ab 1.024 sichtbaren Eingabetoken. Das bestimmt weder Cacheverhalten noch Abrechnung eines Codex-Abonnements.
- Anthropic dokumentiert modellabhängige Claude-Kontextfenster bis zu 1 Mio. Token und getrennte Claude-Code-Cache-Standards für Hauptgespräche im Abonnement und andere Interaktionen. Das belegt weder Cache noch Kontingent der laufenden Sitzung.

Quellen: [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [OpenAI-Prompt-Caching](https://developers.openai.com/api/docs/guides/prompt-caching), [Claude-Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows), [Claude-Code-Prompt-Caching](https://code.claude.com/docs/en/prompt-caching).

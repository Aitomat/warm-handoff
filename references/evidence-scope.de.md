# Beleggrenzen

<!-- rule:EV-01 -->
## Belegklassen

- **Quellenfakt:** genauer Nutzertext, Repository-Inhalt oder offizielle Dokumentation.
- **Beobachteter Stand:** aktuelles Kommando-, Werkzeug-, UI- oder Testergebnis mit Datum und Umgebung.
- **Schluss:** aus Quellenfakten oder Beobachtungen abgeleitete Aussage.
- **Unbekannt:** ein Wert, den die vorhandenen Belege nicht bestimmen.

Kennzeichne Schlüsse ausdrücklich. Nutze für veränderliche Plattformaussagen bevorzugt Primärdokumentation.

<!-- rule:EV-02 -->
## Zeit- und Produktgrenzen

Nenne bei Aussagen zu Modellen, Caching, Preisen, Kontingenten und Produktfunktionen ein Prüfdatum. Benenne die Oberfläche: API, Desktop-Client, CLI, Abonnement oder aktuelle Host-Sitzung. Ein Fakt aus einer Oberfläche gilt nicht automatisch für eine andere.

<!-- rule:EV-03 -->
## Abschlussbelege

Passe Prüfung und Aussage aneinander an. Ein Renderertest belegt erzeugte RTF-Struktur; ein AppKit-Fortsetzungstest belegt Stil nach Speichern/Neuladen; ein manueller Test in der Zielanwendung belegt Einfügeverhalten. Eine vorhandene Datei beweist keinen Inhalt, und ein Arbeiterbericht ersetzt keine Integrationsprüfung.

Ist ein Beleg unvollständig, nenne die genaue offene Prüfung, statt die Aussage mit vager Sicherheit abzuschwächen.

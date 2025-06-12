
# 📊 Grundbuchanalyse – Zeitreihenvergleich von Eigentumsdaten

Dieses Projekt führt eine zeitbasierte Analyse von Grundbuchdaten ab 2013, basierend auf Eigentümertypen und Wirtschaftszweigen. Es verarbeitet historische Daten aus einem SQL Server Data Warehouse und erzeugt automatisch:
- Diagramme mit Trends und Alarmmarkierungen
- Eine Excel-Datei mit farblich markierten Auffälligkeiten

---

## ⚙️ Voraussetzungen

- **Python 3.10+**
- **Zugang zu SQL Server**
- **uv** (virtuelle Umgebung via [uv](https://github.com/astral-sh/uv))

---

## 📦 Installation

### 1. Virtuelle Umgebung initialisieren

Führe das mitgelieferte Batch-Skript aus:

```bash
install_uv.bat
```

Dies lädt und installiert automatisch alle Abhängigkeiten mit `uv`.

### 2. Umgebungsvariablen einrichten

Kopiere die Datei `.env.example` und benenne sie um in `.env`. Fülle sie mit deinen echten Verbindungsdaten

---

## ▶️ Ausführen

Führe das Analyse-Skript über die vorbereitete Batch-Datei aus:

```bash
run_code.bat
```

Dieses Skript startet `gb_historie.py` direkt innerhalb der virtuellen Umgebung.

---

## 📁 Ausgabe

Nach erfolgreicher Ausführung befinden sich alle Ergebnisse im Ordner `Daten`:
- **GB_prozentuale.xlsx** – Excel-Datei mit Veränderungswerten, rot markiert bei > ±5 %
- **plots/** – Diagramme pro Kategorie und Sektor mit Trend- und Alarmdarstellung

---

## 🧼 Struktur

```
├── gb_historie.py             # Hauptskript zur Analyse
├── .env.example               # Vorlage für Umgebungsvariablen
├── install_uv.bat            # Erst-Setup mit uv
├── run_code.bat              # Start-Skript
├── .python-version
├── project.toml
├── README.md 
├── Daten/plots
```

---


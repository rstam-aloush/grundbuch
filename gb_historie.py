import pandas as pd
import matplotlib.pyplot as plt
import os
import pyodbc
from dotenv import load_dotenv

# ---------------- Konfiguration ----------------
load_dotenv()
server = os.getenv("SERVER")
database = os.getenv("DATABASE")
query_2020 = os.getenv("QUERY_2020")
query_1999 = os.getenv("QUERY_1999")

# ---------------- Datenbankverbindung ----------------
conn = pyodbc.connect(
    "Driver={SQL Server};"
    f"Server={server};"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.execute(f"USE {database}")

query_2020 = f"""
SELECT *
  FROM {query_2020}
"""
query_1999 = f"""
SELECT *
  FROM {query_1999}
"""

# --------------- Daten laden und verarbeiten ---------------
# Excel-Dateien laden
df1 = pd.read_sql_query(query_1999, conn)
df2 = pd.read_sql_query(query_2020, conn)

df1 = df1.loc[:, ~df1.columns.str.startswith("Leer")]
df1 = df1.loc[:, ~df1.columns.str.startswith("Unbekannt")]
df2 = df2.loc[:, ~df2.columns.str.startswith("Leer")]
df2 = df2.loc[:, ~df2.columns.str.startswith("Unbekannt")]
# Verbindung schließen (optional)
conn.close()

# Zeilen von df1 mit Jahr zwischen 2013 und 2019 filtern
df1_filtered = df1[(df1['Jahr'] >= 2013) & (df1['Jahr'] <= 2019)]

# Gefilterte Zeilen an df2 anhängen
df_merged = pd.concat([df2, df1_filtered], ignore_index=True)



# Kategorien definieren anhand der Rechtsform
def kategorisiere_rechtsform(rf):
    if str(rf).startswith("01"):
        return "Natürliche Person"
    elif str(rf).startswith(("09", "10", "11")):
        return "Gemeinschaften"
    elif str(rf).startswith("12"):
        return "Gemischt"
    else:
        return "Juristische Person"
    
df_merged["Kategorie"] = df_merged["Rechtsform"].apply(kategorisiere_rechtsform)

# Wirtschaftssektoren-Spalten extrahieren
wirtschaftsspalten = [col for col in df_merged.columns if col not in ["Jahr", "Rechtsform", "Kategorie"]]

# Aggregieren
df_aggregiert = df_merged.groupby(["Jahr", "Kategorie"])[wirtschaftsspalten].sum().reset_index()

# Spalte "Total" pro Zeile (Summe über Wirtschaftssektoren)
df_aggregiert["Total"] = df_aggregiert[wirtschaftsspalten].sum(axis=1)

df_aggregiert = df_aggregiert.sort_values(by=["Jahr", "Kategorie"])

wertspalten = [col for col in df_aggregiert.columns if col not in ["Jahr", "Kategorie"]]

# ---------------- Berechnungen ----------------
total_df = df_aggregiert[["Jahr", "Kategorie"]].copy()

for spalte in wertspalten:
    total_df[f"{spalte}"] = df_aggregiert.groupby("Kategorie")[spalte].pct_change() * 100

# ---------------- Plotting mit Alarmmarkierung ----------------
output_dir = "Data\plots"
os.makedirs(output_dir, exist_ok=True)

for spalte in wertspalten:

    pct_col = f"{spalte}"
    spaltenname = spalte.replace("/", "_").replace("-", "_").replace("&", "_").replace(", ", "_").replace(" ", "_")
    plt.figure(figsize=(14, 6))

    for kategorie in df_aggregiert["Kategorie"].unique():
        jahre = df_aggregiert[df_aggregiert["Kategorie"] == kategorie]["Jahr"]
        werte = total_df[total_df["Kategorie"] == kategorie][pct_col]
        

        # Linien plotten
        plt.plot(jahre, werte, marker='o', label=f"{kategorie} - %")

        # Alarm-Marker einzeichnen
        for x, y in zip(jahre, werte):
            if pd.notna(y) and abs(y) > 19:
                plt.scatter(x, y, color='black', s=50, zorder=5)

    plt.title(f"{spalte}")
    plt.xlabel("Jahr")
    plt.ylabel("Veränderung in %")
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, f"{spaltenname}.png"))
    plt.close()

with pd.ExcelWriter("Data\GB_prozentuale.xlsx", engine="xlsxwriter") as writer:
    total_df.to_excel(writer, index=False, sheet_name="Prozentwerte") 

    workbook = writer.book
    worksheet = writer.sheets["Prozentwerte"]

    #Formate definieren
    red_bold = workbook.add_format({'font_color': 'red', 'bold': True})

    for row_inderx, row in total_df.iterrows():
        for col_index, value in enumerate(row[2:], start=2):
            if pd.notna(value) and abs(value) > 19:
                worksheet.write(row_inderx + 1, col_index, value, red_bold)


print("✅ Die Daten wurden erfolgreich verarbeitet und gespeichert.")
print("📁 Sie befinden sich im Ordner 'Daten'.")


import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

url = "https://companies-market-cap-copy.vercel.app/index.html"
html_raw = requests.get(url)
html_text = html_raw.text

html_parseado = BeautifulSoup(html_text, "html.parser")
tabla = html_parseado.find("table") 
tr = tabla.find_all("tr")

datos = []
for fila in tr[1:]:
    td = fila.find_all("td")
    fecha = td[0].text.strip()
    ingresos = td[1].text.strip()
    datos.append([fecha, ingresos])

for dato in datos:
    if "$" in dato[1]:
        dato[1] = dato[1].replace("$", "")
     
    if "B" in dato[1]:
        dato[1] = dato[1].replace("B", "")

    if " " in dato[1]:
        dato[1] = dato[1].replace(" ", "")

    dato[1] = float(dato[1])


dataframe = pd.DataFrame(datos, columns=["Fecha", "Ingresos"])
dataframe = dataframe.sort_values("Fecha")

conn = sqlite3.connect("beneficios_Tesla.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingresos (
    fecha TEXT,
    ingresos REAL
)
""")


for i,j in dataframe.iterrows():
    cursor.execute("INSERT INTO ingresos (fecha, ingresos) VALUES (?, ?)", (j["Fecha"], j["Ingresos"]))

conn.commit()
conn.close()


plt.figure(figsize=(10, 6))
plt.plot(dataframe["Fecha"], dataframe["Ingresos"], label="Ingresos", marker="o",linestyle=':', color='green')
plt.title("Tesla")
plt.xlabel("Fecha")
plt.ylabel("Ingresos (billones USD)")
plt.legend()


plt.show()

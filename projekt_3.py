"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jan Staněk
email: rubadub@seznam.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def validate_arguments(args): 
    # Validuje argumenty zadané v příkazové řádku
    if len(args) != 3:
        print("Chyba: Zadejte přesně 2 argumenty - název obce a jméno výstupního souboru.")
        sys.exit(1)

    obec = args[1]
    output_file = args[2]

    if not output_file.endswith(".csv"):
        print("Chyba: Druhý argument musí být jméno souboru s příponou .csv.")
        sys.exit(1)

    return obec, output_file

def get_obec_url(base_url, obec):
    # Najde URL pro  zadanou obec
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Chyba: Nepodařilo se připojit na URL {base_url} (status code {response.status_code}).")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0 and obec.lower() in cells[1].text.lower():
            link = cells[3].find("a")
            if link:
                return_value="https://www.volby.cz/pls/ps2017nss/" + link["href"]
                return return_value

    print(f"Chyba: Obec {obec} nebyla nalezena.")
    sys.exit(1)

def scrape_okrsky(base_url):
    # Scrapuje linky na všechny okrsky ze zadání základní URL
    # print(base_url)
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Chyba: Nepodařilo se připojit na URL {base_url} (status code {response.status_code}).")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    # print(f"DEBUG: Počet nalezených tabulek: {len(tables)}")

    okrsky = []

    for table in tables:
        rows = table.find_all("tr")
        # print(f"DEBUG: Počet nalezených řádků v tabulce: {len(rows)}")

        for i, row in enumerate(rows):
        # print(f"DEBUG: Obsah řádku {i}: {row}")
            link = row.find("a")
            if link and "xjazyk" in link["href"]:
                okrsky.append("https://www.volby.cz/pls/ps2017nss/" + link["href"])
    if not okrsky:
        print("Chyba: Žádné odkazy na okrsky nebyly nalezeny.")
        sys.exit(1)

    return okrsky


def find_between(s, start, end):
    return s.split(start)[1].split(end)[0]
    # Doplňková funkce pro získání čísla obce do prvního sloupce výsledků v CSV
    
def scrape_results(okrsek_url):
    """Scrapes election results for a single okrsek."""
    # print(okrsek_url)
    response = requests.get(okrsek_url)
    # print(okrsek_url)
    if response.status_code != 200:
        print(f"Chyba: Nepodařilo se připojit na URL {okrsek_url} (status code {response.status_code}).")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    # Získání základních údajů o okrsku
    header_table = soup.find_all("table")[0]
        # print(header_table)
    header_rows = header_table.find_all("tr")
        # print(header_table)
        # print(soup)
        # print(header_rows[0].find_all("td"))
    cislo_okrsku = find_between(okrsek_url,"&xobec=","&") # Vystřihuji z URL odkazu kód obce
        # print(soup)
        # print (soup.find_all("h3"))
    nazev_okrsku_find = soup.find_all("h3")
    for h3ky in nazev_okrsku_find:
        if h3ky.text.strip()[0:4]=="Obec": nazev_okrsku=h3ky.text.strip()[6:] # Ošetřuje, když se liší počet nadpisů na stránce, z které získáván název obce (např. Praha)
    # print(nazev_okrsku)
    # print(nazev_okrsku)
    # print(soup)
    # Získání výsledků hlasování
    results_table = soup.find_all("table")[0]
    # rows = results_table.find_all("tr")[1:]
    # print(results_table)
    volici = results_table.find_all("td")[3].text.strip()
    # print(volici)
    obalky = results_table.find_all("td")[6].text.strip()
    # print(obalky)
    platne_hlasy = results_table.find_all("td")[7].text.strip()
    # print(platne_hlasy)
    kandidati = soup.find_all("tr")[5:]
    strany = {}
    for kandidat in kandidati:
        cols = kandidat.find_all("td")
        if len(cols)>0 and cols[1].text.strip()!='-': # Kontrola, aby neprobíhalo pro prázdný řádek tabulky výsledků (tj. když je stran méně než třicet)
            strany[cols[1].text.strip()] = cols[2].text.strip()
        # print(strany)
    return {
        "code": cislo_okrsku,
        "location": nazev_okrsku,
        "registered": volici,
        "envelopes": obalky,
        "valid": platne_hlasy,
        **strany
    }

def save_to_csv(data, output_file):
    # Uloží data to CSV souboru
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Výsledky byly uloženy do souboru {output_file}.")

if __name__ == "__main__":
    base_url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

    # Validace argumentů
    obec, output_file = validate_arguments(sys.argv)

    # Získání URL pro obec
    obec_url = get_obec_url(base_url, obec)

    # Scraping okrsků
    okrsky_urls = scrape_okrsky(obec_url)

    # Scraping výsledků
    results = []
    for okrsek_url in okrsky_urls:
        results.append(scrape_results(okrsek_url))

    # Uložení do CSV
    save_to_csv(results, output_file)
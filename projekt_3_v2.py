"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jan Staněk
email: rubadub@seznam.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Tuple

def validate_arguments(args: List[str]) -> Tuple[str, str]:
    """
    Ověří správnost argumentů zadaných v příkazovém řádku.
    
    :param args: Seznam argumentů z příkazové řádky.
    :return: Název obce a jméno výstupního souboru.
    """
    if len(args) != 3:
        print("Chyba: Zadejte přesně 2 argumenty - název obce a jméno výstupního souboru.")
        sys.exit(1)

    obec, output_file = args[1], args[2]

    if not output_file.endswith(".csv"):
        print("Chyba: Druhý argument musí být jméno souboru s příponou .csv.")
        sys.exit(1)

    return obec, output_file

def get_soup(session: requests.Session, url: str) -> BeautifulSoup:
    """
    Stáhne obsah stránky a vrátí jej jako objekt BeautifulSoup.

    :param session: HTTP session pro efektivní opakované požadavky.
    :param url: URL adresa stránky ke stažení.
    :return: Objekt BeautifulSoup obsahující HTML stránky.
    """
    response = session.get(url)
    if response.status_code != 200:
        print(f"Chyba: Nepodařilo se připojit na URL {url} (status code {response.status_code}).")
        sys.exit(1)
    return BeautifulSoup(response.content, "html.parser")

def get_obec_url(session: requests.Session, base_url: str, obec: str) -> str:
    """
    Najde URL stránky s výsledky pro zadanou obec.

    :param session: HTTP session.
    :param base_url: Základní URL volební stránky.
    :param obec: Název obce.
    :return: URL stránky s výsledky pro obec.
    """
    soup = get_soup(session, base_url)
    rows = soup.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0 and obec.lower() in cells[1].text.lower():
            link = cells[3].find("a")
            if link:
                return "https://www.volby.cz/pls/ps2017nss/" + link["href"]

    print(f"Chyba: Obec {obec} nebyla nalezena.")
    sys.exit(1)

def scrape_okrsky(session: requests.Session, obec_url: str) -> List[str]:
    """
    Najde a vrátí seznam URL pro jednotlivé volební okrsky.

    :param session: HTTP session.
    :param obec_url: URL stránky obce.
    :return: Seznam URL adres okrsků.
    """
    soup = get_soup(session, obec_url)
    tables = soup.find_all("table")

    okrsky = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            link = row.find("a")
            if link and "xjazyk" in link["href"]:
                okrsky.append("https://www.volby.cz/pls/ps2017nss/" + link["href"])

    if not okrsky:
        print("Chyba: Žádné odkazy na okrsky nebyly nalezeny.")
        sys.exit(1)

    return okrsky

def extract_code(url: str) -> str:
    """
    Extrahuje kód obce z URL.

    :param url: URL volebního okrsku.
    :return: Číselný kód obce.
    """
    return url.split("&xobec=")[1].split("&")[0]

def extract_location(soup: BeautifulSoup) -> str:
    """
    Extrahuje název obce z HTML.

    :param soup: Objekt BeautifulSoup obsahující HTML stránky.
    :return: Název obce.
    """
    for h3 in soup.find_all("h3"):
        if h3.text.strip().startswith("Obec"):
            return h3.text.strip()[6:]
    return ""

def extract_basic_stats(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extrahuje základní volební statistiky (registrovaní voliči, vydané obálky, platné hlasy).

    :param soup: Objekt BeautifulSoup obsahující HTML stránky.
    :return: Slovník se základními statistikami.
    """
    table = soup.find_all("table")[0]
    tds = table.find_all("td")
    return {
        "registered": tds[3].text.strip(),
        "envelopes": tds[6].text.strip(),
        "valid": tds[7].text.strip()
    }

def extract_parties(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extrahuje výsledky jednotlivých stran v okrsku.

    :param soup: Objekt BeautifulSoup obsahující HTML stránky.
    :return: Slovník s názvy stran a počty hlasů.
    """
    rows = soup.find_all("tr")[5:]
    parties = {}
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 2 and cols[1].text.strip() != '-':
            party = cols[1].text.strip()
            votes = cols[2].text.strip()
            parties[party] = votes
    return parties

def scrape_results(session: requests.Session, okrsek_url: str) -> Dict[str, str]:
    """
    Stáhne a zpracuje výsledky voleb pro konkrétní okrsek.

    :param session: HTTP session.
    :param okrsek_url: URL stránky s výsledky pro daný okrsek.
    :return: Slovník s výsledky voleb v okrsku.
    """
    soup = get_soup(session, okrsek_url)
    return {
        "code": extract_code(okrsek_url),
        "location": extract_location(soup),
        **extract_basic_stats(soup),
        **extract_parties(soup)
    }

def save_to_csv(data: List[Dict[str, str]], output_file: str) -> None:
    """
    Uloží volební výsledky do CSV souboru.

    :param data: Seznam slovníků obsahujících volební výsledky.
    :param output_file: Název souboru pro uložení dat.
    """
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Výsledky byly uloženy do souboru {output_file}.")

def main() -> Tuple[List[Dict[str, str]], str]:
    """
    Hlavní funkce, která spouští celý proces scraping a zpracování volebních dat.

    :return: Seznam výsledků a název výstupního souboru.
    """
    base_url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    obec, output_file = validate_arguments(sys.argv)

    with requests.Session() as session:
        obec_url = get_obec_url(session, base_url, obec)
        okrsky_urls = scrape_okrsky(session, obec_url)
        results = [scrape_results(session, url) for url in okrsky_urls]

    return results, output_file

if __name__ == "__main__":
    results, output_file = main()
    save_to_csv(results, output_file)

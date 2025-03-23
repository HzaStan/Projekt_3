# 🗳️ Projekt 3: Scraping volebních výsledků  
**Kurz Datový analytik s Pythonem**

Tento Python skript slouží ke stažení a zpracování volebních výsledků z webu [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro zvolenou obec. Na základě zadaného názvu obce skript najde příslušné volební okrsky, získá výsledky hlasování a uloží je do CSV souboru.

---

## 👤 Autor  
**Jan Staněk**  
📧 Email: [rubadub@seznam.cz](mailto:rubadub@seznam.cz)

---

## 🛠️ Instalace

1. Ujistěte se, že máte nainstalovaný **Python 3.x**
2. Nainstalujte potřebné knihovny:
```bash
pip install requests beautifulsoup4 pandas
```

---

## ▶️ Spuštění

Skript spouštějte z příkazové řádky se dvěma argumenty:

```
python projekt_3_v2.py <název_obce> <výstupní_soubor.csv>
```

- `<název_obce>` — např. `Prostějov`
- `<výstupní_soubor.csv>` — např. `vysledky_prostejov.csv`

**Příklad:**
```bash
python projekt_3_v2.py Prostějov vysledky_prostejov.csv
```

---

## 🧩 Hlavní funkce skriptu

| Funkce | Popis |
|--------|-------|
| `validate_arguments(args)` | Ověří správnost vstupních argumentů. |
| `get_obec_url(base_url, obec)` | Najde odkaz pro konkrétní obec na webu volby.cz. |
| `scrape_okrsky(obec_url)` | Získá seznam odkazů na volební okrsky pro obec. |
| `scrape_results(okrsek_url)` | Hlavní orchestrátor pro zisk dat z okrsku (rozděleno do více funkcí). |
| `extract_basic_info(soup, okrsek_url)` | Získá kód a název obce. |
| `extract_voting_stats(soup)` | Získá počty voličů, obálek a platných hlasů. |
| `extract_party_votes(soup)` | Získá hlasy pro jednotlivé strany. |
| `save_to_csv(data, output_file)` | Uloží výsledky do CSV souboru. |

---

## 📦 Požadavky

- Python 3.x  
- Knihovny:  
  - `requests`  
  - `beautifulsoup4`  
  - `pandas`

---

## 📊 Příklad výstupu

Níže je ukázka struktury CSV výstupu (hlavička a dva řádky):

| code   | location  | registered | envelopes | valid | Občanská demokratická strana | Česká pirátská strana | ANO 2011 | ... |
|--------|-----------|------------|-----------|--------|-------------------------------|------------------------|----------|-----|
| 500054 | Praha 1   | 21 556     | 14 145    | 14 036 | 2 770                         | 2 332                  | 2 617    | ... |
| 500224 | Praha 10  | 79 964     | 52 238    | 51 895 | 8 137                         | 9 355                  | 2 998    | ... |

> 🔎 Sloupce s názvy politických stran se mohou lišit dle obce a dostupných kandidujících subjektů.

---
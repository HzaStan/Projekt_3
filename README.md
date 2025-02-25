# Projekt 3: Scraping volebních výsledků pro kurz Datový analytik s Pythonem
Tento Python skript slouží k získání volebních výsledků z webu [volby.cz]
(https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro konkrétní obec. 
Skript vyhledá volební okrsky pro danou obec, stáhne výsledky hlasování a uloží je do CSV souboru.

# Autor
Jan Staněk 
Email: rubadub@seznam.cz

# Instalace
1. Ujistěte se, že máte nainstalovaný Python 3.x.
2. Nainstalujte potřebné knihovny pomocí pip: pip install requests beautifulsoup4 pandas

# Spuštění
Skript se spouští z příkazové řádky s dvěma argumenty:
1. Název obce: Název obce, pro kterou chcete získat volební výsledky (např. "Praha").
2. Výstupní soubor: Jméno výstupního souboru s příponou .csv (např. vysledky_Praha.csv).

Příklad spuštění skriptu: python projekt_3.py Praha vysledky_Praha.csv
Tento příkaz stáhne volební výsledky pro obec "Praha" a uloží je do souboru vysledky.csv.

# Funkce
1. validate_arguments(args)
Validuje argumenty zadání skriptu. 
Očekává dva argumenty: název obce a jméno výstupního souboru s příponou .csv.

2. get_obec_url(base_url, obec)
Vyhledá URL pro konkrétní obec na webu volby.cz.

3. scrape_okrsky(base_url)
Získá všechny odkazy na volební okrsky pro zadanou obec.

4. scrape_results(okrsek_url)
Stáhne a zpracuje výsledky voleb pro jeden volební okrsek.

5. save_to_csv(data, output_file)
Uloží získaná data do CSV souboru.

# Požadavky
Python 3.x
Knihovny: requests, beautifulsoup4, pandas

# Příklad výstupu
Například záhlaví a první dva řádky CSV souboru pro obec Praha má vypadat takto:
code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Volte Pr.Blok www.cibulka.net,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Společ.proti výst.v Prok.údolí,Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,OBČANÉ 2011-SPRAVEDL. PRO LIDI,Unie H.A.V.E.L.,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
500054,Praha 1,21 556,14 145,14 036,2 770,9,13,657,12,1,774,392,514,41,6,241,14,44,2 332,5,0,12,2 783,1 654,1,7,954,3,133,11,2,617,34
500224,Praha 10,79 964,52 238,51 895,8 137,40,34,3 175,50,17,2 334,2 485,1 212,230,15,1 050,35,67,9 355,9,8,30,6 497,10 856,37,53,2 398,12,477,69,53,2 998,162

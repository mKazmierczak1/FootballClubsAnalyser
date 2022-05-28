import pandas as pd 
import requests
import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

leagues_url = 'https://www.worldfootball.net/schedule/$-20#-20*-spieltag/%/'
salaries_url = 'https://www.capology.com/$/payrolls/20#-20*/'
transfers_url = 'https://www.capology.com/$/transfer-recap/20#-20*/'

leagues = [('eng-premier-league', '38', 'uk/premier-league')]#, ('bundesliga', '34', 'de/1-bundesliga'), ('esp-primera-division', '38', 'es/la-liga'), 
#('ita-serie-a', '38', 'it/serie-a'), ('fra-ligue-1', '38', 'fr/ligue-1')]

leagues_urls = []
salaries_urls = []
transfers_urls = []

clubs = {}

map_clubs = {
    'Bayern Munich': 'Bayern München',
    'Inter Milan': 'Inter',
    'PSG': 'Paris Saint-Germain',
    'Hetha': 'Hertha BSC',
    'Brunszwik': 'Eintracht Braunschweig',
    'Athletic': 'Athletic Bilbao',
    'Saint-Etienne': 'AS Saint-Étienne',
    'QPR': 'Queens Park Rangers',
    'GFC Ajaccio': 'GFC Ajaccio',
    'Parma': 'Parma Calcio 1913'
}

def getClubKey(club_name: str):
    global clubs

    for key in clubs.keys():

        key_in_ASCII = unidecode.unidecode(key)
        if club_name in key_in_ASCII:
            return key
        elif club_name in map_clubs.keys():
            return map_clubs[club_name]

    return "No key found!"

def mapToEuro(money: str) -> int:
   exchange_rate = 1.18 if '£' in money else 1
   map_to_number = int(money.replace('£', "").replace('€', "").replace(',', "").strip())
   return int(map_to_number * 1000 * exchange_rate)

def create_seasons_dic(year_from, year_to):
    seasons_dic = {}

    if year_from < year_to:
        for i in range(year_from, year_to):
            seasons_dic[str(year_from) + '/' + str(year_from + 1)] = '-'
    
    return seasons_dic

def extract_data_by_season(data):
    seasons = create_seasons_dic(13, 22)

    for d in data:
        seasons[d[0]] = d[1]

    return seasons.values()

def getSum(payrolls, balances):
    sum = []

    for i in range(0, len(payrolls)):
        if payrolls[i] != '-' and balances[i] != '-':
            sum.append(payrolls[i] + balances[i])
    
    return sum

def extract_row(data):
    row = [data[0]]
    positions = data[1][0]
    payrolls = data[1][1]
    balances = data[1][2]

    row.extend(extract_data_by_season(payrolls))
    row.extend(extract_data_by_season(balances))
    row.extend(getSum(payrolls, balances))
    row.extend(extract_data_by_season(positions))

    return row
    
def exctact_rows_from_clubs_data():
    data = []
    for k in clubs.keys():
        data.append(extract_row(a[k]))

    return data

for i in range (13, 21):
   for league in leagues:
      leagues_urls.append((str(i)+'/'+str(i+1), leagues_url.replace('$', league[0]).replace('#', str(i)).replace('*', str(i+1)).replace('%', league[1])))
      salaries_urls.append((str(i)+'/'+str(i+1), salaries_url.replace('$', league[2]).replace('#', str(i)).replace('*', str(i+1))))
      transfers_urls.append((str(i)+'/'+str(i+1), transfers_url.replace('$', league[2]).replace('#', str(i)).replace('*', str(i+1)), ('20'+str(i)+'-20'+str(i+1))))

# load teams and their final league position in seasons from 2013/14 to 2021/22
for url in leagues_urls:
   resp = requests.get(url[1]) 
   if resp.status_code == 200:
      soup = BeautifulSoup(resp.content,'html.parser')
      tabs = soup.find_all('table', {'class': 'standard_tabelle'})
      df = pd.read_html(str(tabs))[1]
      
      positions = df['#'].tolist()
      teams = df["Team.1"].tolist()

      teams_positions = []

      for i in range(0, len(teams)):
         teams_positions.append((teams[i], positions[i]))

      for team in teams_positions:
         if not team[0] in clubs.keys():
            clubs[team[0]] = ([(url[0], team[1])], [], [])
         else:
            clubs[team[0]][0].append((url[0], team[1]))

# load clubs salaries from website
for url in salaries_urls:
   timeout = 10
   browser = webdriver.Chrome(ChromeDriverManager().install())
   browser.get(url[1])

   try:
      element_present = EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
      WebDriverWait(browser, timeout).until(element_present)
   except TimeoutException:
      print("Timed out waiting for page to load")

   soup = BeautifulSoup(browser.page_source,'html5lib')
   table = soup.find('table', id="table")
   df = pd.read_html(str(table))

   payroll_column = 'Annual Gross(' + ("IN GBP, 000's" if 'premier-league' in url[1] else "IN EUR, 000's") + ')'

   clubs_from_table = df[0]['Unnamed: 0_level_0']['Club'].tolist()
   salaries_from_table = df[0]['Combined Payroll'][payroll_column].tolist()

   for i in range(0, len(clubs_from_table)):
      club_key = getClubKey(clubs_from_table[i])
      if club_key != "No key found!":
         clubs[club_key][1].append((url[0], mapToEuro(salaries_from_table[i])))


# load clubs transfers balances from website
for url in transfers_urls:
   timeout = 10
   browser = webdriver.Chrome(ChromeDriverManager().install())
   browser.get(url[1])

   try:
      element_present = EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
      WebDriverWait(browser, timeout).until(element_present)
   except TimeoutException:
      print("Timed out waiting for page to load")

   soup = BeautifulSoup(browser.page_source,'html5lib')
   table = soup.find('table', id="table")
   df = pd.read_html(str(table))

   balance_column = 'Balance(' + ("IN GBP, 000's" if 'premier-league' in url[1] else "IN EUR, 000's") + ')'

   print(df[0].columns)
   clubs_from_table = df[0]['Unnamed: 0_level_0']['Club'].tolist()
   balance_from_table = df[0][url[2] + ' Transfer Operations'][balance_column].tolist()

   for i in range(0, len(clubs_from_table)):
      club_key = getClubKey(clubs_from_table[i])
      if club_key != "No key found!":
         clubs[club_key][2].append((url[0], mapToEuro(balance_from_table[i])))

print(clubs)      
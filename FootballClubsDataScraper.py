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

leagues = [('eng-premier-league', '38', 'uk/premier-league'), ('bundesliga', '34', 'de/1-bundesliga'), ('esp-primera-division', '38', 'es/la-liga'), 
('ita-serie-a', '38', 'it/serie-a'), ('fra-ligue-1', '38', 'fr/ligue-1')]

leagues_urls = []
salaries_urls = []
transfers_urls = []

clubs = {}

# Irregular names which can be mapped in normal way
map_clubs = {
    'Bayern Munich': 'Bayern München',
    'Inter Milan': 'Inter',
    'PSG': 'Paris Saint-Germain',
    'Hertha Berlin': 'Hertha BSC',
    'Braunschweiger': 'Eintracht Braunschweig',
    'Athletic Club': 'Athletic Bilbao',
    'St-Etienne': 'AS Saint-Étienne',
    'QPR': 'Queens Park Rangers',
    'Gazelec Ajaccio': 'GFC Ajaccio',
    'Parma': 'Parma FC'
}

# Dta is scraped from 2 websites and because of that the same club can be named diffrently between websites
# Adjusting name form one website to work with diffrent one
def get_club_key(club_name: str):
    global clubs

    for key in clubs.keys():

        key_in_ASCII = unidecode.unidecode(key)
        if club_name in key_in_ASCII:
            return key
        elif club_name in map_clubs.keys():
            return map_clubs[club_name]

    return "No key found!"

# Clubs form english Premier League have data about money expressed in pounds
# To standardize data, they must be mapped to euros
# Multiplication by 1000 results from the fact that the data is stored in this way (divided by 1000)
def map_to_euro(money: str) -> int:
   exchange_rate = 1.18 if '£' in money else 1
   map_to_number = int(money.replace('£', "").replace('€', "").replace(',', "").strip())
   return int(map_to_number * 1000 * exchange_rate)

# Creating urls which will be futher used to scrap data from those websites
def create_urls(year_from, year_to):
    for i in range (year_from, year_to):
        for league in leagues:
            if i == 16 and league[0] == 'esp-primera-division':         # Unfortunately, one URL is different and must be handled manually
                leagues_urls.append((str(i)+'/'+str(i+1), 'https://www.worldfootball.net/schedule/esp-primera-division-2016-2017-spieltag_2/38/')) 
            else:
                leagues_urls.append((str(i)+'/'+str(i+1), leagues_url.replace('$', league[0]).replace('#', str(i)).replace('*', str(i+1)).replace('%', league[1])))

            salaries_urls.append((str(i)+'/'+str(i+1), salaries_url.replace('$', league[2]).replace('#', str(i)).replace('*', str(i+1))))
            transfers_urls.append((str(i)+'/'+str(i+1), transfers_url.replace('$', league[2]).replace('#', str(i)).replace('*', str(i+1)), ('20'+str(i)+'-20'+str(i+1))))

# Load teams and their final league position in seasons from 2013/14 to 2021/22
def load_teams_positions():
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
                if teams[i] != 'Parma Calcio 1913':                         # Parma changed it's name from Parma FC to Parma Calcio 1913
                    teams_positions.append((teams[i], positions[i]))        # At one site there are 2 names: old and new one
                else:                                                       # But on second site name Parma refers to both names
                    teams_positions.append(('Parma FC', positions[i]))      

            for team in teams_positions:
                if not team[0] in clubs.keys():
                    clubs[team[0]] = ([(url[0], team[1])], [], [])
                else:
                    clubs[team[0]][0].append((url[0], team[1]))

# Load clubs salaries from website
def load_cubs_salaries():
    for url in salaries_urls:
        timeout = 20
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
            club_key = get_club_key(clubs_from_table[i])
            if club_key != "No key found!":
                clubs[club_key][1].append((url[0], map_to_euro(salaries_from_table[i])))


# Load clubs transfers balances from website
def load_clubs_transfer_balances():
    for url in transfers_urls:
        timeout = 20
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
        clubs_from_table = df[0]['Unnamed: 0_level_0']['Club'].tolist()
        balance_from_table = df[0][url[2] + ' Transfer Operations'][balance_column].tolist()

        for i in range(0, len(clubs_from_table)):
            club_key = get_club_key(clubs_from_table[i])
            if club_key != "No key found!":
                clubs[club_key][2].append((url[0], map_to_euro(balance_from_table[i])))

def create_seasons_dic(year_from, year_to):
    seasons_dic = {}

    if year_from < year_to:
        for i in range(year_from, year_to):
            seasons_dic[str(i) + '/' + str(i + 1)] = '-'
    
    return seasons_dic

# If data about season isn't present return '-'
def extract_data_by_season(data, year_from, year_to):
    seasons = create_seasons_dic(year_from, year_to)

    for d in data:
        seasons[d[0]] = d[1]

    return list(seasons.values())

# Sum club's payroll and transfers balance
def sum_expenses(payrolls, balances):
    sum = []

    for i in range(0, len(payrolls)):
        if payrolls[i] != '-' and balances[i] != '-':
            sum.append(payrolls[i] - balances[i])
        elif payrolls[i] == '-' and balances[i] != '-':
            sum.append(-balances[i])
        else:
            sum.append('-')
    
    return sum

# Create single table row which contains data about single club
def extract_row(data, year_from, year_to):
    row = [data[0]]
    positions = extract_data_by_season(data[1][0], year_from, year_to)
    payrolls = extract_data_by_season(data[1][1], year_from, year_to)
    balances = extract_data_by_season(data[1][2], year_from, year_to)

    row.extend(payrolls)
    row.extend(balances)
    row.extend(sum_expenses(payrolls, balances))
    row.extend(positions)

    return row

# Extract the downloaded club data for storing in a data frame 
def extract_rows_from_clubs_data(year_from, year_to):
    data = []
    for k in clubs.keys():
        data.append(extract_row((k, clubs[k]), year_from, year_to))

    return data

def create_dataframe_from_clubs_data(year_from, year_to):
    seasons = []
    columns_names = ['Payrolls', 'Balances', 'Expenses', 'League positions']

    for i in range (year_from, year_to):
        seasons.append(str(i)+'/'+str(i+1))
    

    def create_tuples(name):
        l = []
        for season in seasons:
            l.append((name, season))
        
        return l
        
    columns = [('', 'Club')]

    for name in columns_names:
        columns.extend(create_tuples(name)) 


    df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(columns), data=extract_rows_from_clubs_data(year_from, year_to))

    return df

def store_data(df: pd.DataFrame):
    df.to_csv("clubs_data.csv")
    df.to_excel("clubs_data.xlsx")

# load every data form web and store it as .csv and .xlsx files
def load_and_store_data_about_clubs_form_web(year_from, year_to):
    create_urls(year_from, year_to)
    load_teams_positions()
    load_cubs_salaries()
    load_clubs_transfer_balances()

    df = create_dataframe_from_clubs_data(year_from, year_to)
    store_data(df)
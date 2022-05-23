import pandas as pd 
import requests
from bs4 import BeautifulSoup   # ważna alternatywa: Selenium

clubs = {}

premier_league_table_url = 'https://www.worldfootball.net/schedule/eng-premier-league-20##-20**-spieltag/38/'
premier_league_tables_urls = []

salaries_url = 'https://www.capology.com/uk/premier-league/payrolls/20##-20**/'
premier_league_salaries_urls = []


for i in range (13, 21):
   # year1 = str(i) if i >= 10 else '0' + str(i)
   # year2 = str(i+1) if i >= 9 else '0' + str(i+1)

   premier_league_tables_urls.append(('20' + str(i) + '/' + str(i+1), premier_league_table_url.replace('##', str(i)).replace('**', str(i+1))))
   premier_league_salaries_urls.append(('20' + str(i) + '/' + str(i+1), salaries_url.replace('##', str(i)).replace('**', str(i+1))))

# resp = requests.get(seson08_09) 
# if resp.status_code == 200:    # czy stronę udało się otworzyć?
#     soup = BeautifulSoup(resp.content,'html.parser')  # utowrzenie drzewa wyszukiwań
#     links = soup.find_all('a')   # ekstrakcja tabel z drzewa wyszukiwań

# teams = []

# for link in links:
#    link_text = link.text.strip()
   
#    if 'href' in link.attrs.keys():
#       if '/wiki/2008%E2%80%9309' in link['href']:
#           teams.append(link['href'])


# for table in premier_league_tables:
#    resp = requests.get(table[1]) 
#    if resp.status_code == 200:    # czy stronę udało się otworzyć?
#       soup = BeautifulSoup(resp.content,'html.parser')  # utowrzenie drzewa wyszukiwań
#       tabs = soup.find_all('table',{'class':"wikitable"})   # ekstrakcja tabel z drzewa wyszukiwań
#       df = pd.read_html(str(tabs))#[3]        # konwersja pierwszej znalezionej tabeli do ramki danych
      
#       print(table[0])
#       for f in df:
#          if 'Qualification or relegation' in f.keys():
#             print(f.get("Team"))
#             print(f)



# for table in premier_league_tables2:
#    resp = requests.get(table[1]) 
#    if resp.status_code == 200:    # czy stronę udało się otworzyć?
#       soup = BeautifulSoup(resp.content,'html.parser')  # utowrzenie drzewa wyszukiwań
#       tabs = soup.find_all('table', {'class': 'standard_tabelle'})   # ekstrakcja tabel z drzewa wyszukiwań
#       df = pd.read_html(str(tabs))[0]#[3]        # konwersja pierwszej znalezionej tabeli do ramki danych
      
#       print(table[0])
#       #print(df)

#       for team in df.get(1):
#          clubs[team] = ([], [])

for table in premier_league_tables_urls:
   resp = requests.get(table[1]) 
   if resp.status_code == 200:    # czy stronę udało się otworzyć?
      soup = BeautifulSoup(resp.content,'html.parser')  # utowrzenie drzewa wyszukiwań
      tabs = soup.find_all('table', {'class': 'standard_tabelle'})   # ekstrakcja tabel z drzewa wyszukiwań
      df = pd.read_html(str(tabs))[1]#[3]        # konwersja pierwszej znalezionej tabeli do ramki danych
      
      positions = df['#'].tolist()
      teams = df["Team.1"].tolist()

      teams_position = []

      for i in range(0, len(teams)):
         teams_position.append((teams[i], positions[i]))

      for team in teams_position:
         if not team[0] in clubs.keys():
            clubs[team[0]] = ([team[1]], [])
         else:
            clubs[team[0]][0].append(team[1])


print(pd.read_html("./salaries/PL/pl_21_22.html")["Annual Gross(IN GBP, 000's)"].tolist())

# for salary in premier_league_salaries_urls:
#    resp = requests.get(salary[1]) 
#    if resp.status_code == 200:
#       soup = BeautifulSoup(resp.content,'html.parser')
      
#       print(salary[0])
#       print(tabs)
  

print(clubs)      
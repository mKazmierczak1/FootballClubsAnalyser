import unidecode

clubs = {'Bayern München': 1,
'Inter': 2,
'Bor. Mönchengladbach': 3,
'Paris Saint-Germain': 4,
'Hertha BSC': 5,
'1. FC Nürnberg ':6,
'Eintracht Braunschweig': 7,
'Atlético Madrid':8
'1. FC Nürnberg': 9 }

map_clubs = {
    'Bayern Munich': 'Bayern München',
    'Inter Milan': 'Inter',
    'PSG': 'Paris Saint-Germain'
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

print(getClubKey('Bayern Munich'))
print(getClubKey('Inter Milan'))
print(getClubKey('Monchengladbach'))
print(getClubKey("Hertha"))
print(getClubKey('PSG'))
print(getClubKey('Atletico'))
print(getClubKey('1. FC Nürnberg'))

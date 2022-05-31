import pandas as pd
import statistics
from os.path import exists
import football_clubs_data_scraper as scraper

file_path = 'data/clubs_data.csv'

# if file doesn't exist load from web
if not exists(file_path):
    scraper.load_and_store_data_about_clubs_form_web(13, 22)

df = pd.read_csv(file_path)

# create list of all expenses from every club's season
expenses = df['Expenses'].to_list()[1:]
for i in range(1, 9):
    expenses.extend(df['Expenses.' + str(i)].to_list()[1:])

# create list of all every club's season positions
positions = df['League positions'].to_list()[1:]
for i in range(1, 9):
    positions.extend(df['League positions.' + str(i)].to_list()[1:])

# remove invalid data
i = len(expenses) - 1
while i >= 0:
    if expenses[i] == '-' or positions[i] == '-':
        positions.pop(i)
        expenses.pop(i)
    i -= 1

# convert string values to int
expenses = [int(i) for i in expenses]

# create dictionary with every possible position in league (1-20)
positions_dic = {}
for i in range(1, 21):
    positions_dic[str(i)] = []

# add every expense to proper position
for i in range(0, len(positions)):
    positions_dic[positions[i]].append(int(expenses[i]))

# calculate average expenses and median for every position
average_expenses = []
median_expenses = []
for k in positions_dic.keys():
    average_expenses.append(statistics.mean(positions_dic[k]))
    median_expenses.append(statistics.median(positions_dic[k]))


def getClubsPositions():
    return positions

def getClubsExpenses():
    return expenses

def getAverageExpensesPerPosition():
    return average_expenses

def getMedianExpensesPerPosition():
    return median_expenses

def getEveryPossiblePosition():
    return list(positions_dic.keys())
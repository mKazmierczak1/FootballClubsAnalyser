import numpy as np
import pandas as pd
import statistics
#import FootballClubsDataScraper as scraper

#scraper.load_and_store_data_about_clubs_form_web(13, 22)
df = pd.read_csv('clubs_data.csv')

Expenses = df['Expenses'].to_list()[1:]
for i in range(1, 9):
    Expenses.extend(df['Expenses.' + str(i)].to_list()[1:])

Positions = df['League positions'].to_list()[1:]
for i in range(1, 9):
    Positions.extend(df['League positions.' + str(i)].to_list()[1:])

i = len(Expenses) - 1

while i >= 0:
    if Expenses[i] == '-' or Positions[i] == '-':
        Positions.pop(i)
        Expenses.pop(i)
    i -= 1

positions = {}

for i in range(1, 21):
    positions[str(i)] = []

for i in range(0, len(Positions)):
    positions[Positions[i]].append(int(Expenses[i]))

X = []
average_Y = []
median_Y = []

for k in positions.keys():
    average_Y.append(statistics.mean(positions[k]))
    median_Y.append(statistics.median(positions[k]))
    #dominanta

A = []

# for i in range(0, Expenses.count('-')):
#     Expenses.remove('-')

for y in Expenses:
    A.append(int(y))


print(len(Positions))
B = []

for x in Positions:
    B.append(int(x))


def getClubsPositions():
    return Positions

def getClubbsExpenses():
    return Expenses

def getAverageExpensesPerPosition():
    return average_Y

def getMedianExpensesPerPosition():
    return median_Y

def getEveryPossiblePosition():
    return list(positions.keys())
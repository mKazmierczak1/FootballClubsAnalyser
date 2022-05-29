from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import FootballClubsDataScraper as scraper
import seaborn as sns
from sklearn.linear_model import LinearRegression

#scraper.load_and_store_data_about_clubs_form_web(13, 22)
df = pd.read_csv('clubs_data.csv')

print(df.columns)


Expenses = df['Expenses'].to_list()[1:]
for i in range(1, 9):
    Expenses.extend(df['Expenses.' + str(i)].to_list()[1:])

Y = []
print(len(Expenses))
for i in range(0, Expenses.count('-')):
    Expenses.remove('-')

Expenses.pop()
Expenses.pop()
Expenses.pop()

for y in Expenses:
    Y.append(int(y))

Positions = df['League positions'].to_list()[1:]
for i in range(1, 9):
    Positions.extend(df['League positions.' + str(i)].to_list()[1:])
print(len(Positions))
X = []

for i in range(0, Positions.count('-')):
    Positions.remove('-')

for x in Positions:
    X.append(int(x))

# model_lin = LinearRegression()
# model_lin.fit(np.reshape(X, (-1,1)), Y)
# Y_pred = model_lin.predict(np.reshape(X, (-1,1)))

plt.figure(figsize=(20,20))
sns.scatterplot(x=Positions, y=Y)
# plt.plot(X, Y_pred, color="tab:orange")
plt.show()
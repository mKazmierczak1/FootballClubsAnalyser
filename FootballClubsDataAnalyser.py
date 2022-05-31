from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import FootballClubsDataMapper
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import statistics

Positions = FootballClubsDataMapper.getClubsPositions()
Expenses = FootballClubsDataMapper.getClubbsExpenses()
average_Y = FootballClubsDataMapper.getAverageExpensesPerPosition()
median_Y = FootballClubsDataMapper.getMedianExpensesPerPosition()

# model_lin = LinearRegression()
# model_lin.fit(np.reshape(X, (-1,1)), Y)


p = FootballClubsDataMapper.getEveryPossiblePosition()

# model = RandomForestRegressor(n_estimators=100, max_features=2)
# model.fit(np.reshape(p, (-1,1)), average_Y)
# Y_pred = model.predict(np.reshape(p, (-1,1)))

# model.fit(np.reshape(p, (-1,1)), median_Y)
# Y_pred2 = model.predict(np.reshape(p, (-1,1)))


plt.figure(figsize=(10,5))
sns.scatterplot(x=p, y=average_Y, label="average")
sns.scatterplot(x=p, y=median_Y, color='green', label="median")
# sns.scatterplot(x=A, y=Positions, color='black')
# plt.plot(p, Y_pred, color="tab:orange", label="average model")
# plt.plot(p, Y_pred2, color="tab:purple", label ="median model")

# xdata = np.asarray(X)
# ydata = np.asarray(Y)

# def Gauss(x, A, B):
#     y = A*np.exp(-1*B*x**2)
#     return y

# parameters, covariance = curve_fit(Gauss, xdata, ydata)

# fit_A = parameters[0]
# fit_B = parameters[1]

# fit_y = Gauss(xdata, fit_A, fit_B)
# plt.plot(xdata, ydata, 'o', label='data')
# plt.plot(xdata, fit_y, '-', label='fit')

for i in range(0, len(p) - 1):
    x = [p[i], p[i+1]]
    y1 = [average_Y[i], average_Y[i+1]]
    y2 = [median_Y[i], median_Y[i+1]]
    plt.plot(x, y1, color="orange", label="average line")
    plt.plot(x, y2, color="purple", label="median line")


plt.xlabel("Position")
plt.ylabel("Expenses")
plt.legend()
plt.show()
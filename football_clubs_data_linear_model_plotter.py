import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import football_clubs_data_mapper

average = football_clubs_data_mapper.getAverageExpensesPerPosition()
median = football_clubs_data_mapper.getMedianExpensesPerPosition()
positions = football_clubs_data_mapper.getEveryPossiblePosition()

model_lin = LinearRegression()
model_lin.fit(np.reshape(average, (-1,1)), positions)
Y_pred_avg = model_lin.predict(np.reshape(average, (-1,1)))

model_lin.fit(np.reshape(median, (-1,1)), positions)
Y_pred_median = model_lin.predict(np.reshape(median, (-1,1)))

plt.figure(figsize=(10,5))
sns.scatterplot(x=average, y=positions, color="orange", label="average expenses")
plt.plot(average, Y_pred_avg, color="tab:orange", label="average model")
sns.scatterplot(x=median, y=positions, color="purple", label="median expenses")
plt.plot(median, Y_pred_median, color="tab:purple", label ="median model")

plt.title("Linear model")
plt.xlabel("Expenses")
plt.ylabel("Positions")
plt.legend()
plt.show()
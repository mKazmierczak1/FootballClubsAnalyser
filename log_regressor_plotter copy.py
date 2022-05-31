import seaborn as sns
from matplotlib import pyplot as plt
import football_clubs_data_mapper
import my_log_regressor

average = football_clubs_data_mapper.getAverageExpensesPerPosition()
median = football_clubs_data_mapper.getMedianExpensesPerPosition()
positions = football_clubs_data_mapper.getEveryPossiblePosition()
positions = [int(i) for i in positions]

plt.figure(figsize=(10,5))
sns.scatterplot(x=average, y=positions, color="red", label="average expenses")
plt.plot(average, my_log_regressor.log_model_predict(average, positions), color="tab:red", label="average model")
sns.scatterplot(x=median, y=positions, color="blue", label="median expenses")
plt.plot(median, my_log_regressor.log_model_predict(median, positions), color="tab:blue", label="median model")

plt.ylim(0.5,20.5)
plt.title("Logarithmic regression")
plt.xlabel("Expenses")
plt.ylabel("Positions")
plt.legend()
plt.show()

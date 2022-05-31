import seaborn as sns
from matplotlib import pyplot as plt
import football_clubs_data_mapper

average_Y = football_clubs_data_mapper.getAverageExpensesPerPosition()
median_Y = football_clubs_data_mapper.getMedianExpensesPerPosition()
X = football_clubs_data_mapper.getEveryPossiblePosition()

plt.figure(figsize=(10,5))
sns.scatterplot(x=X, y=average_Y, color="orange", label="average")
sns.scatterplot(x=X, y=median_Y, color="purple", label="median")

for i in range(0, len(X) - 1):
    x = [X[i], X[i+1]]
    y1 = [average_Y[i], average_Y[i+1]]
    y2 = [median_Y[i], median_Y[i+1]]
    plt.plot(x, y1, color="orange")
    plt.plot(x, y2, color="purple")

plt.title("All clubs mean and median")
plt.xlabel("Position")
plt.ylabel("Expenses")
plt.legend()
plt.show()

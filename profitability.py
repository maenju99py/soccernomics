import pandas as pd
import matplotlib.pyplot as plt

country = 'paraguay'
year = 2022
tournament = 'apertura'

# load the data.
df = pd.read_csv('db/' + country + '/' + str(year) + '/' + tournament + '/bets.csv', sep=",")

margin = []
i = 1
for index, row in df.iterrows():
    jor = row['league_date']
    home = row['home']
    visitor = row['visitors']
    if row['bet'] == row['dummy_results'] or row['dummy_results'] == 0:
        profit = row['bet_odd'] - 1
    else:
        profit = -1

    margin.append([i, jor, home, visitor, profit])
    i += 1

total_profit = 0
t = []
list_profit = []
for x in margin:
    t.append(x[0])
    list_profit.append(x[4])
    total_profit += x[4]

plt.scatter(t, list_profit, c="blue")
print(total_profit / len(t))

# To show the plot
plt.show()

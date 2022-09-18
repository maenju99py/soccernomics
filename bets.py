import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge
from models import ridge_regression_v1

country = 'paraguay'
year = 2021
tournament = 'clausura'

jor_init = 12
rounds = 18
games_per_round = 5
lags = 11

# load the data.
df = pd.read_csv('db/' + country + '/' + str(year) + '/' + tournament + '/goals.csv', sep=";")
df_games = pd.read_csv('db/' + country + '/' + str(year) + '/' + tournament + '/goals.csv', sep=";").iloc[
           (jor_init - 1) * games_per_round:]
df_odds = pd.read_csv('db/' + country + '/' + str(year) + '/' + tournament + '/odds.csv', sep=";").iloc[
          (jor_init - 1) * games_per_round:]
df_odds.rename(columns={'visitor': 'visitors'}, inplace=True)

# Data Transformation
df_games['date'] = pd.to_datetime(df_games['date'].astype(str).str[:10], format='%d-%m-%Y')
df_games['goal_difference'] = df_games['goals_h'] - df_games['goals_v']

# Variables dummy que indican si la casa gana (1) o pierde (0)
df_games['dummy_results'] = np.where(df_games['goal_difference'] > 0, 1,
                                     np.where(df_games['goal_difference'] < 0, -1, 0))

# Simulador de apuesta seleccionada
bet_type, bet, rating_h, rating_v = [], [], [], []

for jornada in range(jor_init, rounds + 1):
    # Sacar los ratings para la jornada
    df_rating = ridge_regression_v1(df, jornada, games_per_round, lags)

    # Obtener solo la data de la jornada
    df_games_v2 = df_games.iloc[(jornada - jor_init) * games_per_round: (jornada - jor_init + 1) * games_per_round]

    for index, row in df_games_v2.iterrows():

        # Seleccionar el equipo por el que apostamos
        league_date = row['league_date']
        home = row['home']
        visitor = row['visitors']

        home_rating = df_rating.loc[df_rating['team'] == home, 'rating'].unique()[0]
        visitor_rating = df_rating.loc[df_rating['team'] == visitor, 'rating'].unique()[0]

        # model_winner is the bet we make (0:1X, 1:2X)
        if home_rating > visitor_rating:
            model_winner = 1
        else:
            model_winner = -1

        rating_h.append(home_rating)
        rating_v.append(visitor_rating)
        bet_type.append('double chance')
        bet.append(model_winner)

df_games['rating_h'] = rating_h
df_games['rating_v'] = rating_v
df_games['bet_type'] = bet_type
df_games['bet'] = bet

# Merge db's (results, odds)
df_merged = pd.merge(df_games, df_odds, on=['league_date', 'home', 'visitors'])

bet_odd = []
# Odd selector
profit_margin = 0
for index, row in df_merged.iterrows():
    if row['bet'] == 1:
        bet_odd.append(row['one_x_odd'])
    else:
        bet_odd.append(row['two_x_odd'])

df_merged['bet_odd'] = bet_odd

df_merged.to_csv('db/' + country + '/' + str(year) + '/' + tournament + '/bets.csv')

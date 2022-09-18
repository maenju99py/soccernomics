import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score


def ridge_regression_v1(dataframe, jor, games_per_jor, lags):
    """ Forecast the expected goals for every team using ridge regression.

        input: home, visitor and goal difference for every game
        output: expected goals (rating)

        :param dataframe: all games data of the jornada
        :param jor: jornada to forecast expected goal difference
        :param games_per_jor: number of games per jornada
        """
    # Drop data after jornada
    df = dataframe.iloc[(jor - lags - 1) * games_per_jor:(jor - 1) * games_per_jor].copy()

    # Data Transformation
    df['date'] = pd.to_datetime(df['date'].astype(str).str[:10], format='%d-%m-%Y')
    df['goal_difference'] = df['goals_h'] - df['goals_v']

    # Create new variables to show home team win or loss result
    df['home_win'] = np.where(df['goal_difference'] > 0, 1, 0)
    df['home_loss'] = np.where(df['goal_difference'] < 0, 1, 0)

    df_visitor = pd.get_dummies(df['visitors'], dtype=np.int64)
    df_home = pd.get_dummies(df['home'], dtype=np.int64)

    # Subtract home from visitor
    df_model = df_home.sub(df_visitor)
    df_model['goal_difference'] = df['goal_difference']

    # Not required but I like to rename my dataframe with the name train.
    df_train = df_model

    # Setting model
    lr = Ridge(alpha=0.001)
    X = df_train.drop(['goal_difference'], axis=1)
    y = df_train['goal_difference']

    # Fitting model to data
    lr.fit(X, y)

    # Expected goal differences
    df_ratings = pd.DataFrame(data={'team': X.columns, 'rating': lr.coef_})
    return df_ratings


df = pd.read_csv('db/paraguay/2022/clausura/goals.csv', sep=";")
print(ridge_regression_v1(df, 10, 6, 9))

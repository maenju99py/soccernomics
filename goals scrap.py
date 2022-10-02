from turtle import home
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

country = 'paraguay'
tournament = 'clausura'
year = '2022'
rounds = 12
total_rounds = 18
games_per_round = 6

country_tournament_links = {'paraguay': {'2022': {'apertura': 'https://football.nowgoal6.com/SubLeague/2022/354/56',
                                                  'clausura': 'https://football.nowgoal6.com/SubLeague/2022/354/57'},
                                         '2021': {'claus    ura': 'https://football.nowgoal6.com/SubLeague/2021/354/57'}
                                         },
                            'inglaterra': {'premier_league': 'https://football.nowgoal6.com/League/36'}}

link = country_tournament_links[country][year][tournament]

games = []

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def game_scrap(round, game):
    date = driver.find_element(By.XPATH, f"//table[contains(@id,'Table3')]//tr[{2 + game}]//td[2]").text
    home_team = driver.find_element(By.XPATH, f"//table[contains(@id,'Table3')]//tr[{2 + game}]//td[3]//a").text
    away_team = driver.find_element(By.XPATH, f"//table[contains(@id,'Table3')]//tr[{2 + game}]//td[5]//a").text
    home_goals = driver.find_element(By.XPATH, f"//table[contains(@id,'Table3')]//tr[{2 + game}]//div[contains(@class,'redf')]//font[1]").text
    away_goals = driver.find_element(By.XPATH, f"//table[contains(@id,'Table3')]//tr[{2 + game}]//div[contains(@class,'redf')]//font[2]").text

    if home_goals.find("-") == 1:
        home_goals = home_goals[0]
    else:
        away_goals = away_goals[1]

    data_inst = [round, date, home_team, home_goals, away_team, away_goals]
    print(data_inst)

    games.append(data_inst)


# Abrir pagina web
driver.get(link)

for round in range(1, rounds + 1):
    table_row = int((round / ((total_rounds / 2) + 1) // 1) + 1)
    cell_row = int(round - (table_row - 1) * (total_rounds / 2))

    # Cambiar a jornada
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH,
         f"//table[contains(@id,'Table2')]//tr[{table_row}]/td[contains(@class,'lsm2')][{cell_row}]"))).click()

    time.sleep(3)

    for game in range(1, games_per_round + 1):
        game_scrap(round, game)

with open('db/' + country + '/' + str(year) + '/' + tournament + '/goals.csv', "w", newline="") as f:
    writer = csv.writer(f)
    header = ['league_date', 'date', 'home', 'goals_h', 'visitors', 'goals_v']
    writer.writerow(header)
    writer.writerows(games)

driver.quit()

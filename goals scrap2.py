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
rounds = 13
total_rounds = 18
games_per_round = 6

country_tournament_links = {'paraguay': {'2022': {'apertura': 'https://football.nowgoal6.com/SubLeague/2022/354/56',
                                                  'clausura': 'https://football.nowgoal6.com/SubLeague/2022/354/57'},
                                         '2021': {'clausura': 'https://football.nowgoal6.com/SubLeague/2021/354/57'}
                                         },
                            'inglaterra': {'premier_league': 'https://football.nowgoal6.com/League/36'}}

link = country_tournament_links[country][year][tournament]

games = []

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def game_scrap(league):
    date = driver.find_element(By.XPATH, f"//span[contains(@name,'timeData')]").text
    home_team = driver.find_element(By.XPATH, f"//tr//td[1]/span/a").text
    away_team = driver.find_element(By.XPATH, f"//tr//td[3]/span/a").text
    home_goals = driver.find_element(By.XPATH, f"//div[contains(@class,'score')]").text
    away_goals = driver.find_element(By.XPATH, f"//div[contains(@class,'score')][2]").text

    data_inst = [league, date, home_team, home_goals, away_team, away_goals]

    games.append(data_inst)


# Abrir pagina web
driver.get(link)

for t in range(1, rounds + 1):
    table_row = int((t / ((total_rounds / 2) + 1) // 1) + 1)
    cell_row = int(t - (table_row - 1) * (total_rounds / 2))

    # Cambiar a jornada
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH,
         f"//table[contains(@id,'Table2')]//tr[{table_row}]/td[contains(@class,'lsm2')][{cell_row}]"))).click()

    for g in range(1, games_per_round + 1):
        time.sleep(3)
        # Ingresar a estadisticas
        element = driver.find_element(By.XPATH,
                                      f'//tbody/tr[{2 + g}]//td[9]/a[2]')
        driver.execute_script("arguments[0].click();", element)

        # Cambiar de ventana
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)

        # Game Data Scrapping
        time.sleep(1)
        try:
            game_scrap(t)
        except:
            driver.refresh()
            game_scrap(t)

        # Cambiar de ventana
        driver.close()
        driver.switch_to.window(window_before)

with open('db/' + country + '/' + str(year) + '/' + tournament + '/goals.csv', "w", newline="") as f:
    writer = csv.writer(f)
    header = ['league_date', 'date', 'home', 'goals_h', 'visitors', 'goals_v']
    writer.writerow(header)
    writer.writerows(games)

driver.quit()

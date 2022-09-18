from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import math

odds = []

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Parametros del Programa
country = 'paraguay'
year = 2022
tournament = 'clausura'
total_rounds = 18
rounds = 9
games_per_round = 6

# Links
country_tournament_links = {
    'paraguay': {'apertura': 'https://oddspedia.com/football/paraguay/primera-division-apertura',
                 'clausura': 'https://oddspedia.com/football/paraguay/primera-division-clausura'},
    'inglaterra': {'premier_league': 'https://football.nowgoal6.com/League/36'}}

link = country_tournament_links[country][tournament]

# Abrir pagina web
driver.get(link)

# Aceptar boton pop up
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH,
     f"//button[contains(@class,'cookie-popup__btn')]"))).click()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH,
     f"//button[contains(@class,'align-right primary slidedown-button')]"))).click()

# Abrir menu de anos
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH,
     f"//div[contains(@class,'dropdown content__header--league__dropdown dropdown--small dropdown--dark')]/button"))).click()

# Seleccionar ano
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH,
     f"//div[contains(@class,'dropdown__list-item') and contains(text(), '{str(year)}')]"))).click()
time.sleep(2)

# Cambiar de Week a Rounds
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH,
     f"/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div[2]/div/div[1]/div[1]/div[2]/div[1]/label/span[1]"))).click()

for jor in range(0, rounds):

    # Abrir lista de Jornadas
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH,
         f"/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div[2]/div/div[1]/div[1]/div[1]/button"))).click()

    # Elegir jornada
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH,
         f"//div[contains(@class,'dropdown match-list-league-subnav__list dropdown--small d-none d-sm-block dropdown__list--absolute active dropdown--uppercase dropdown--light dropdown--small')]/div/div[{total_rounds - jor + 4}]"))).click()

    for game in range(0, games_per_round):

        # Clicks para mostrar data del juego
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH,
             f"//div[contains(@class,'match-list-item')][{1 + game}]"))).click()

        jornada = jor + 1

        # Scrapear nombre de los clubes
        home = driver.find_element(By.XPATH,
                                   f"//div[contains(@class,'match-list-item')][{game + 1}]/div/a/div[2]/div[1]/div[1]").text
        visitor = driver.find_element(By.XPATH,
                                      f"//div[contains(@class,'match-list-item')][{game + 1}]/div/a/div[2]/div[2]/div[1]").text

        # Ingresar a pestana de apuestas
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH,
             f"//ul[contains(@class,'has-tabs-secondary')]/li[3]"))).click()

        # Scrapear apuestas clasicas
        win_odd_home = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class,'eoc-summary__row--info')]/div[2]/span[1]"))).text

        draw_odd = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class,'eoc-summary__row--info')]/div[2]/span[2]"))).text

        loss_odd_home = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class,'eoc-summary__row--info')]/div[2]/span[3]"))).text

        # Scrapear apuestas 2X
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH,
             f"//button[contains(@class,'eoc-markets__btn eoc-markets__btn--dropdown')]"))).click()

        try:
            bet_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH,
                 f"/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/aside/div[2]/div/div[1]/div/div/section[4]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/ul/li[5]/button"))).click()

            one_x_odd = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class,'eoc-summary__row--info')]/div[2]/span[1]"))).text

            one_two_odd = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class,'eoc-summary__row--info')]/div[2]/span[2]"))).text

            two_x_odd = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class,'eoc-summary__row--info')]/div[2]/span[3]"))).text

        except:
            one_x_odd = math.nan
            one_two_odd = math.nan
            two_x_odd = math.nan

        odds.append([jornada, home, visitor, win_odd_home, draw_odd, loss_odd_home, one_x_odd, one_two_odd, two_x_odd])

with open("db/" + country + '/' + str(year) + '/' + tournament + '/odds.csv', "w", newline="") as f:
    writer = csv.writer(f)
    header = ['league_date', 'home', 'visitor', 'win_odd_home', 'draw_odd', 'loss_odd_home', 'one_x_odd', 'one_two_odd',
              'two_x_odd']
    writer.writerow(header)
    writer.writerows(odds)

driver.quit()

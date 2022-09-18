from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


def game_scrap(league):
    i = 0

    league_date = league
    date = driver.find_element(By.XPATH, f"//span[contains(@name,'timeData')]").text

    home = driver.find_element(By.XPATH, f"//tr//td[1]/span/a").text
    visitors = driver.find_element(By.XPATH, f"//tr//td[3]/span/a").text

    goals_h = driver.find_element(By.XPATH, f"//div[contains(@class,'score')]").text
    goals_v = driver.find_element(By.XPATH, f"//div[contains(@class,'score')][2]").text

    games.append(
        [league_date, date, home, goals_h, visitors, goals_v])


games = []

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Abrir pagina web
driver.get("https://football.nowgoal6.com/SubLeague/2022/354/57")

for t in range(1, 9):
    # Cambiar a jornada
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, f"/html/body/div[2]/div[2]/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[{t + 1}]"))).click()

    for g in range(1, 7):
        time.sleep(3)
        # Ingresar a estadisticas
        element = driver.find_element(By.XPATH,
                                      f'/html/body/div[2]/div[2]/div[2]/div[4]/div[3]/table/tbody/tr[{g + 2}]/td[9]/a[2]')
        driver.execute_script("arguments[0].click();", element)

        # Cambiar de ventana
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)

        # Game Data Scrapping
        time.sleep(2)
        game_scrap(t)
        time.sleep(2)

        # Cambiar de ventana
        driver.close()
        driver.switch_to.window(window_before)

with open("goals.csv", "w", newline="") as f:
    writer = csv.writer(f)
    header = ['league_date', 'date', 'home', 'goals_h', 'visitors', 'goals_v']
    writer.writerow(header)
    writer.writerows(games)

print(games)

driver.quit()

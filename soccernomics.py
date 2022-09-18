from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

country = 'paraguay'

teams = {'resistencia SC': 'Resistencia FC',
         'Tacuary': 'Tacuary',
         'Sportivo Ameliano': 'Club Sportivo Ameliano',
         'Olimpia Asuncion': 'Club Olimpia',
         'General Caballero': 'General Caballero JLM',
         'Cerro Porteno': 'Cerro Porteno',
         'Guairena': 'Guairena FC',
         'Libertad': 'Club Libertad',
         'Sol de America': 'Sol de America',
         'FC Nacional Asuncion': 'Club Nacional',
         'Guarani CA': 'Guarani Asuncion',
         '12 de Octubre': 'Club 12 de Octubre Itaugua',
         }


def game_scrap(league):
    i = 0

    league_date = league
    date = driver.find_element(By.XPATH, f"//span[contains(@name,'timeData')]").text

    home = driver.find_element(By.XPATH, f"//tr//td[1]/span/a").text
    visitors = driver.find_element(By.XPATH, f"//tr//td[3]/span/a").text

    goals_h = driver.find_element(By.XPATH, f"//div[contains(@class,'score')]").text
    goals_v = driver.find_element(By.XPATH, f"//div[contains(@class,'score')][2]").text

    title_corner_kicks = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[1]/span[3]").text
    if title_corner_kicks == "Corner Kicks":
        cornerKicks_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[1]/span[1]").text
        cornerKicks_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[1]/span[5]").text
    else:
        cornerKicks_h = 0
        cornerKicks_v = 0
        i -= 1

    title_corner_kicks_ht = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{2 + i}]/span[3]").text
    if title_corner_kicks_ht == "Corner Kicks(HT)":
        cornerKicksHT_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{2 + i}]/span[1]").text
        cornerKicksHT_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{2 + i}]/span[5]").text
    else:
        cornerKicksHT_h = 0
        cornerKicksHT_v = 0
        i -= 1

    title_yellow_cards = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{3 + i}]/span[3]").text
    if title_yellow_cards == "Yellow Cards":
        yellowCards_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{3 + i}]/span[1]").text
        yellowCards_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{3 + i}]/span[5]").text
    else:
        yellowCards_h = 0
        yellowCards_v = 0
        i -= 1

    title_red_cards = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{4 + i}]/span[3]").text
    if title_red_cards == "Red Cards":
        redCards_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{4 + i}]/span[1]").text
        redCards_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{4 + i}]/span[5]").text
    else:
        redCards_h = 0
        redCards_v = 0
        i -= 1

    title_shots = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{5 + i}]/span[3]").text
    if title_shots == "Shots":
        shots_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{5 + i}]/span[1]").text
        shots_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{5 + i}]/span[5]").text
    else:
        shots_h = 0
        shots_v = 0
        i -= 1

    title_shots_on_goal = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{6 + i}]/span[3]").text
    if title_shots_on_goal == "Shots on Goal":
        shotsOnGoal_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{6 + i}]/span[1]").text
        shotsOnGoal_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{6 + i}]/span[5]").text
    else:
        shotsOnGoal_h = 0
        shotsOnGoal_v = 0
        i -= 1

    title_attacks = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{7 + i}]/span[3]").text
    if title_attacks == "Attacks":
        attacks_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{7 + i}]/span[1]").text
        attacks_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{7 + i}]/span[5]").text
    else:
        attacks_h = 0
        attacks_v = 0
        i -= 1

    title_dangerous_attack = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{8 + i}]/span[3]").text
    if title_dangerous_attack == "Dangerous Attacks":
        dangerousAttacks_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{8 + i}]/span[1]").text
        dangerousAttacks_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{8 + i}]/span[5]").text
    else:
        dangerousAttacks_h = 0
        dangerousAttacks_v = 0
        i -= 1

    title_shots_off_goal = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{9 + i}]/span[3]").text
    if title_shots_off_goal == "Shots off Goal":
        shotsOffGoal_h = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{9 + i}]/span[1]").text
        shotsOffGoal_v = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{9 + i}]/span[5]").text
    else:
        shotsOffGoal_h = 0
        shotsOffGoal_v = 0
        i -= 1

    try:
        title_possession = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{10 + i}]/span[3]").text
        if title_possession == "Possession":
            possession_h = int(
                driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{10 + i}]/span[1]").text[
                0:2]) / 100
            possession_v = int(
                driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{10 + i}]/span[5]").text[
                0:2]) / 100
        else:
            possession_h = 0
            possession_v = 0
            i -= 1
    except:
        possession_h = 0
        possession_v = 0
        i -= 1

    title_possession_ht = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{11 + i}]/span[3]").text
    if title_possession_ht == "Possession(HT)":
        possession_ht_h = int(
            driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{11 + i}]/span[1]").text[0:2]) / 100
        possession_ht_v = int(
            driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{11 + i}]/span[5]").text[0:2]) / 100
    else:
        possession_ht_h = 0
        possession_ht_v = 0

    games.append(
        [league_date, date, home, goals_h, cornerKicks_h, cornerKicksHT_h, yellowCards_h, redCards_h, shots_h,
         shotsOnGoal_h,
         attacks_h,
         dangerousAttacks_h, shotsOffGoal_h, possession_h, possession_ht_h, visitors, goals_v, cornerKicks_v,
         cornerKicksHT_v,
         yellowCards_v,
         redCards_v,
         shots_v, shotsOnGoal_v, attacks_v, dangerousAttacks_v, shotsOffGoal_v, possession_v, possession_ht_v])


games = []

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Abrir pagina web
driver.get("https://football.nowgoal6.com/League/36")

for t in range(1, 6):
    # Cambiar a jornada
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, f"/html/body/div[2]/div[2]/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[{t + 1}]"))).click()

    for g in range(1, 11):
        time.sleep(3)
        # Ingresar a estadisticas
        element = driver.find_element(By.XPATH,
                                      f'/html/body/div[2]/div[2]/div[2]/div[4]/div[3]/table/tbody/tr[{g + 2}]/td[9]/a[2]')
        driver.execute_script("arguments[0].click();", element)

        # Cambiar de ventana
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)

        # Ir a pestaña de detalles
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, f'/html/body/div[5]/div/ul[1]/li[2]/a'))).click()

        # Game Data Scrapping
        time.sleep(2)
        game_scrap(t)
        time.sleep(2)

        # Cambiar de ventana
        driver.close()
        driver.switch_to.window(window_before)

with open("db/" + country + "/data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    header = ['league_date', 'date', 'home', 'goals_h', 'cornerKicks_h', 'cornerKicksHT_h', 'yellowCards_h',
              'redCards_h',
              'shots_h', 'shotsOnGoal_h',
              'attacks_h',
              'dangerousAttacks_h', 'shotsOffGoal_h', 'possession_h', 'possession_ht_h', 'visitors', 'goals_v',
              'cornerKicks_v',
              'cornerKicksHT_v', 'yellowCards_v', 'redCards_v',
              'shots_v', 'shotsOnGoal_v', 'attacks_v', 'dangerousAttacks_v', 'shotsOffGoal_v', 'possession_v',
              'possession_ht_v']
    writer.writerow(header)
    writer.writerows(games)

print(games)

driver.quit()

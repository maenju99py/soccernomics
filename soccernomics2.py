from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

country = 'paraguay'
tournament = 'apertura'
rounds = 22
games_per_round = 6

country_tournament_links = {'paraguay': {'apertura': 'https://football.nowgoal6.com/SubLeague/2022/354/56',
                                         'clausura': 'https://football.nowgoal6.com/SubLeague/2022/354/57'},
                            'inglaterra': {'premier_league': 'https://football.nowgoal6.com/League/36'}}

link = country_tournament_links[country][tournament]

games = []
data = []

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def game_scrap(league):
    i = 1

    data_dict_instance = {'league_date': league,
                          'date': driver.find_element(By.XPATH, f"//span[contains(@name,'timeData')]").text,
                          'home': {'team': driver.find_element(By.XPATH, f"//tr//td[1]/span/a").text,
                                   'goals': driver.find_element(By.XPATH, f"//div[contains(@class,'score')]").text},
                          'away': {'team': driver.find_element(By.XPATH, f"//tr//td[3]/span/a").text,
                                   'goals': driver.find_element(By.XPATH, f"//div[contains(@class,'score')][2]").text}}

    while True:
        try:
            title = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{i}]/span[3]").text
        except:
            break
        else:
            home_data = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{i}]/span[1]").text
            away_data = driver.find_element(By.XPATH, f"//ul[contains(@class,'stat')]/li[{i}]/span[5]").text

            data_dict_instance['home'][title] = home_data
            data_dict_instance['away'][title] = away_data

            i += 1

    data.append(data_dict_instance)


def get_fields(list_dict):
    fields = []
    for record in list_dict:
        record_fields = list(record['home'])
        for field in record_fields:
            if field not in fields:
                fields.append(field)

    return fields


def fill_non_data(list_dict):
    fields = get_fields(list_dict)
    for record in list_dict:
        record_fields = list(record['home'])
        for field in fields:
            if field not in record_fields:
                record['home'][field] = 0
                record['away'][field] = 0

    return list_dict


# Abrir pagina web
driver.get(link)

for t in range(1, 2):
    # Cambiar a jornada
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, f"//td[contains(@class,'lsm2')][{t}]"))).click()

    for g in range(1, 3):
        time.sleep(3)
        # Ingresar a estadisticas
        element = driver.find_element(By.XPATH,
                                      f'//tbody/tr[{2 + g}]//td[9]/a[2]')
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

# with open("db/" + country + "/" + tournament + "/data.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     header = ['league_date', 'date', 'home', 'goals_h', 'cornerKicks_h', 'cornerKicksHT_h', 'yellowCards_h',
#               'redCards_h',
#               'shots_h', 'shotsOnGoal_h',
#               'attacks_h',
#               'dangerousAttacks_h', 'shotsOffGoal_h', 'possession_h', 'possession_ht_h', 'visitors', 'goals_v',
#               'cornerKicks_v',
#               'cornerKicksHT_v', 'yellowCards_v', 'redCards_v',
#               'shots_v', 'shotsOnGoal_v', 'attacks_v', 'dangerousAttacks_v', 'shotsOffGoal_v', 'possession_v',
#               'possession_ht_v']
#     writer.writerow(header)
#     writer.writerows(games)

print(games)

dick = fill_non_data(data)
print(dick)
driver.quit()

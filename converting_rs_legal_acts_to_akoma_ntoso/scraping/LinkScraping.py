from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import io

attribute = ['Назив прописа', 'ELI', 'Напомена издавача', 'Додатне информације', 'Врста прописа', 'Доносилац',
             'Област', 'Група', 'Датум усвајања', 'Гласило и датум објављивања',
             'Датум ступања на снагу основног текста',
             'Датум примене', 'Правни претходник', 'Издавач']

propisi = []


def write_json_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_csv_file(file_name, row):
    fd = open(file_name, 'a', encoding="utf-8")
    fd.write(row)
    fd.write('\n')
    fd.close()


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")

    browser = webdriver.Chrome(executable_path='C:\Chromedriver\chromedriver.exe', chrome_options=option)
    file_name = 'address.txt'
    file = open(file_name, "r")

    row = ""
    for i in range(0, len(attribute)):
        row += attribute[i]
        if i < len(attribute) - 1:
            row += "#"
    write_csv_file('propisi.csv', row)

    brojac = 0
    browser.get('http://www.pravno-informacioni-sistem.rs/SlGlasnikPortal/reg/advancedSearch')

    selectedLimit = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="resultLimit"]/option[6]')))
    selectedLimit.click()

    selectedLaw = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, '// *[ @ id = "docType"] / option[16]')))
    selectedLaw.click()
    #//*[@id="docType"]/option[3] Zakoni linkovi.txt
    #//*[@id="docType"]/option[9] = Odluka = linkovi2.txt
    #//*[@id="docType"]/option[7] Uredba linkovi3.txt
    #//*[@id="docType"]/option[16] Pravilnik linkovi4.txt
    time.sleep(1)
    first = True
    fajl = io.open("../data/linkovi/linkovi4.txt", mode="x", encoding="utf-8")
    for region in range(2,5):
        selectedRegion = WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located((By.XPATH, ' // *[ @ id = "podregistar"] / option[' + str(region) + ']')))
        selectedRegion.click()

        time.sleep(0.5)
        regions = browser.find_elements_by_xpath('// *[ @ id = "oblast"]//*')
        first = True
        for oblast in range(0,len(regions)):
            #print(regions[oblast].get_attribute("label"))
            time.sleep(2)

            selectedOblast = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, ' // *[ @ id = "oblast"] / option[' + str(oblast+1) + ']')))
            selectedOblast.click()
            time.sleep(0.5)

            selectedButton = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '// *[ @ id = "appContainer"] / div / div[1] / form / div[2] / div[4] / div / button[1]')))
            selectedButton.click()
            time.sleep(1)
           # browser.implicitly_wait(1)

            if first:
                first = False
                continue

            rows = browser.find_elements_by_xpath('//*[@id="resultTable"]/div/table/tbody/*')

            print('Oblast[i]=' + str(oblast) + 'Duzina=' + str(round(len(rows)/2)))



            for rowInTable in range(1,round(len(rows)/2)+1):
                if rowInTable == 501:
                    break

                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="resultTable"]/div/table/tbody/tr[' + str(rowInTable) + ']/td[4]/a'))
                )
                fajl.write(str(element.get_attribute("href")) + '\n')
    fajl.close()

    # for line in file:
    #     browser.get(line)
    #
    #     brojac += 1
    #     print(brojac)
    #
    #     try:
    #         o_aktu = WebDriverWait(browser, 30).until(
    #             EC.visibility_of_element_located((By.XPATH, ' // *[ @ id = "podregistar"] / option[2]')))
    #         o_aktu.click()
    #     except:
    #         continue
    #     try:
    #         tabela = WebDriverWait(browser, 20).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="actContentSecondary"]/table')))
    #     except:
    #         continue
    #
    #     redovi = tabela.find_elements(By.TAG_NAME, "tr")
    #
    #     labele = []
    #     vrednosti = []
    #
    #     for red in redovi:
    #         labela = red.find_element(By.CLASS_NAME, "act-idcard-label-cell-1")
    #         vrednost = red.find_element(By.CLASS_NAME, "act-idcard-value-cell-1")
    #
    #         p_labela = labela.find_element(By.TAG_NAME, "p")
    #         p_vrednost = vrednost.find_element(By.TAG_NAME, "p")
    #
    #         if p_labela.text not in attribute:
    #             continue
    #
    #         if p_labela.text not in labele:
    #             labele.append(p_labela.text)
    #             vrednosti.append(p_vrednost.text)
    #             print(p_labela.text)
    #             print(p_vrednost.text)
    #
    #     propis = "{"
    #     row = ""
    #     j = 0
    #     for i in range(0, len(attribute)):
    #         if len(labele) > j:
    #             if labele[j] == attribute[i]:
    #                 propis += '"' + labele[j] + '" : ' + '"' + vrednosti[j].replace('"', '').replace('\n', '') + '"'
    #                 row += vrednosti[j].replace('"', '').replace('\n', '')
    #                 j += 1
    #             else:
    #                 propis += '"' + attribute[i] + '" : ' + '""'
    #         else:
    #             propis += '"' + attribute[i] + '" : ' + '""'
    #
    #         if i < len(attribute) - 1:
    #             propis += ","
    #             row += "#"
    #
    #     propis += "}"
    #     propis_json = json.loads(propis)
    #
    #     propisi.append(propis_json)
    #
    #     write_json_file('propisi.json', propisi)
    #     write_csv_file('propisi.csv', row)
    #
    #     try:
    #         article = WebDriverWait(browser, 20).until(
    #             EC.presence_of_element_located((By.XPATH, '//article')))
    #     except:
    #         continue
    #     ## skidanje samog teksta akta u html foramtu
    #     fajl = io.open("../data/aktovi/" + str(brojac) + ".html", mode="w", encoding="utf-8")
    #     fajl.write(article.get_attribute('innerHTML'))
    #     fajl.close()

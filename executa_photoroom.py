from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, os, zipfile
from navegador import get_driver_navegador, get_element_by_text


def verifica_concluido(driver : webdriver.Chrome):
    style_barra_progresso = driver.find_element(By.CSS_SELECTOR, '#root > div.flex.h-screen.w-screen.overflow-hidden > div.relative.flex.h-full.grow.flex-col.overflow-y-auto.bg-white > div.grow > div.fixed.h-1.animate-pulse.rounded-r-300.bg-gradient-to-tl.from-pastel-pink.to-pastel-coral')\
    .get_attribute('style')
    print('style_barra_progresso: ', style_barra_progresso)
    return style_barra_progresso.count('100%') > 0

def espera_carregar(driver : webdriver.Chrome):
    time.sleep(2)
    carregando = True
    while(carregando):
        time.sleep(1)
        carregando = not verifica_concluido(driver)

def inicializa_photoroom(driver):
    driver.get('https://app.photoroom.com/batch?templateId=1bc00117-2bc4-4503-a632-071ce2719ad2')
    while len(driver.find_elements(By.CSS_SELECTOR, 'input[type=file]')) == 0:
        time.sleep(0.1)
    
    return [driver.find_element(By.CSS_SELECTOR, 'input[type=file]'), []]

def executar(driver = None):
    diretorio_atual = os.getcwd()

    arquivos_por_vez = 50

    if 'local_download' in os.environ.keys():
        local_download = os.environ['local_download']
    else:
        local_download = diretorio_atual

    #with get_driver_navegador() as driver:
    if not driver:
        driver = get_driver_navegador()
    caminhos = [os.path.join(diretorio_atual, nome) for nome in os.listdir(diretorio_atual)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]

    input_file, list_path_files = inicializa_photoroom(driver)

    for i, img_caminho in enumerate(jpgs):
        print(img_caminho)
        list_path_files.append(str(img_caminho).replace('\\\\', '\\'))
        
        if (i+1) % arquivos_por_vez == 0 or i == (len(jpgs) - 1):
            print(list_path_files)
            input_file.send_keys(' \n'.join(list_path_files))
            time.sleep(3)

            print('Aplicando modelo padrão')
            espera_carregar(driver)
            
            #CENTRALIZAR
            time.sleep(1)
            print('Centralizando...')
            #driver.find_element(By.CSS_SELECTOR, '#root > div.flex.h-screen.w-screen.overflow-hidden > div.relative.flex.h-full.grow.flex-col.overflow-y-auto.bg-white > div.grow > div.relative.flex.h-full.flex-col.bg-neutral-1 > div > div > div.flex.flex-wrap.items-center.gap-3 > button:nth-child(4)').click()
            #driver.find_element(By.CSS_SELECTOR, 'div > div > div > button:nth-child(2) > div > div > svg').click()
            driver.find_element(By.XPATH, '//*[text()="Inserção"]').click()
            driver.find_element(By.XPATH, '//*[text()="Centralizado"]').click()

            espera_carregar(driver)
            #SOMBRA LEVE
            time.sleep(1)

            print('Aplicando sombra')
            driver.find_element(By.XPATH, '//*[text()="Sobras IA"]').click()
            driver.find_element(By.XPATH, '//*[text()="Suave"]').click()
            espera_carregar(driver)
            
            while len(driver.find_elements(By.XPATH, '//*[text()="Baixe suas imagens"]')) == 0:
                time.sleep(1)
            driver.find_element(By.XPATH, '//*[text()="Baixe suas imagens"]').click()
            time.sleep(1)
            
            input_file, list_path_files = inicializa_photoroom(driver)

    print('Extrair ZIPs e excluir')

    caminhos = [os.path.join(local_download, nome) for nome in os.listdir(local_download)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    zips = [arq for arq in arquivos if arq.lower().count('photoroom') > 0 and arq.lower().endswith(".zip")]
    for zip in zips:
        print(zip)
        with zipfile.ZipFile(zip, 'r') as zip_ref:
            zip_ref.extractall(diretorio_atual)
        os.remove(zip)

    print('Finalizado')

    return driver

if __file__ == '__main__':
    executar()
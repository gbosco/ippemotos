import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navegador import get_driver_navegador, get_element_by_text, click

def esperar(tempo):
    time.sleep(tempo)

def executar(driver = None):
    
    #with get_driver_navegador() as driver:
    if not driver:
        driver = get_driver_navegador()

    driver.get('https://ippemoto.painel.magazord.com.br/')
    time.sleep(1)

    try:
        click(driver, get_element_by_text(driver, 'OK'))
    except:
        pass
    
    get_element_by_text(driver, 'MagaZord', texto_exato=False).click()
    driver.find_element(By.CSS_SELECTOR, '[title="Catálogo"]').click()
    driver.find_element(By.CSS_SELECTOR, '[title="Produtos"]').click()
    esperar(3)
    count = 0
    with open('links.txt') as arquivo:
        for linha in arquivo:
            sku, link = linha.split(',')
            link = link.replace(';;;', '')
            link = link.replace('https://youtu.be/', 'https://www.youtube.com/watch?v=')

            arquivo.seek

            driver.find_element(By.CSS_SELECTOR, '[name="codigo"]').clear()
            driver.find_element(By.CSS_SELECTOR, '[name="codigo"]').send_keys(sku)

            get_element_by_text(driver, 'Atualizar').click()
            esperar(2)

            get_element_by_text(driver, sku).click()
            get_element_by_text(driver, 'Alterar').click()
            get_element_by_text(driver, 'Alterar Produto (Novo)').click()
            esperar(2)

            get_element_by_text(driver, 'Mídias').click()
            esperar(1)
            
            driver.find_element(By.CSS_SELECTOR, f'label[for="uploadPhoto-{sku}"]').click()
            esperar(1)
            get_element_by_text(driver, 'Incluir', True)[1].click()
            esperar(1)

            driver.find_elements(By.CSS_SELECTOR, '[name="tipoMidia"]')[-1].clear()
            driver.find_elements(By.CSS_SELECTOR, '[name="tipoMidia"]')[-1].send_keys('2 - Vídeo')
            driver.find_elements(By.CSS_SELECTOR, '[name="tipoMidia"]')[-1].send_keys(Keys.ENTER)

            titulo_video = 'video-' + sku
            driver.find_elements(By.CSS_SELECTOR, '[name="title"]')[-1].send_keys(titulo_video)
            
            driver.find_element(By.CSS_SELECTOR, '[name="path"]').send_keys(link)

            click(driver, get_element_by_text(driver, 'Gravar'))
            esperar(3)
            click(driver, get_element_by_text(driver, 'Fechar', True)[-1])

            get_element_by_text(driver, titulo_video).click()
            get_element_by_text(driver, 'Selecionar').click()

            get_element_by_text(driver, 'Salvar').click()
            esperar(2)
            get_element_by_text(driver, 'Fechar').click()
    
    return driver
    
    

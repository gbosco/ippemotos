import os
import time
from selenium.webdriver.common.by import By
from navegador import get_driver_navegador, get_element_by_text

def executar(driver=None):
    
    url_upload = os.environ['url_yt_studio']
    
    if not driver:
        driver = get_driver_navegador()
   
    for video_file in os.listdir():
        if (video_file.endswith('.mp4') or video_file.endswith('.MOV')) and video_file.count('-feito.') == 0:
            driver.get(url_upload)
            time.sleep(1)

            video_path = os.path.abspath(video_file)
            video_title = os.path.splitext(video_file)[0].replace(' (1)', '')

            input_file = driver.find_element(By.CSS_SELECTOR, 'input[type=file]')
            input_file.send_keys(video_path.replace('\\\\', '\\'))
            
            time.sleep(2)
            while len(get_element_by_text(driver, 'Detalhes', True)) == 0:
                time.sleep(1)
            
            get_element_by_text(driver, 'Próximo').click()
            time.sleep(1)
            get_element_by_text(driver, 'Próximo').click()
            time.sleep(1)
            get_element_by_text(driver, 'Próximo').click()
            time.sleep(5)
            url = driver.find_element(By.CSS_SELECTOR, 'a.style-scope.ytcp-video-info').text
            url = url.replace('https://youtu.be/', 'https://www.youtube.com/watch?v=')
            get_element_by_text(driver, 'Salvar').click()
            
            print(video_title, ',', url)

            linha = video_title + ',' + url
            with open('links.txt', 'a') as arquivo:
                arquivo.write(linha + '\n')
            
            os.rename(video_file, video_file.replace('.', '-feito.'))            

            while len(driver.find_elements(By.CSS_SELECTOR, '#dialog > div > div > ytcp-video-upload-progress > span')) == 0:
                time.sleep(0.5)

            barra_progresso = ''
            while 'concluíd' not in barra_progresso:
                barra_progresso = driver.find_element(By.CSS_SELECTOR, '#dialog > div > div > ytcp-video-upload-progress > span').text
                time.sleep(1)

    return driver
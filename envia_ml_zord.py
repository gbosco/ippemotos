import re, time, sqlite3, os, time, pandas as pd
from navegador import click, get_element_by_text, get_driver_navegador
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path

def executar(driver = None, opcao_usuario = ''):
    ROOT_DIR = Path(os.getcwd())
    DB_NAME = 'db.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME

    #with get_driver_navegador() as driver:
    if not driver:
        driver = get_driver_navegador()
    driver.get('https://ippemoto.painel.magazord.com.br/')
    time.sleep(1)

    ###### Parte 1
    if opcao_usuario in ('1', ''):
        get_element_by_text(driver, 'MagaZord', texto_exato=False).click()
        driver.find_element(By.CSS_SELECTOR, '*[title="Marketplace"]').click()
        get_element_by_text(driver, 'Envios', texto_exato=False).click()
        
        url_for_pandas = f'https://docs.google.com/spreadsheets/d/1zxcKNwzU2v-q0Ms9b-3k_DnqiYsrbcpFas0IOwvAtcY/export?format=xlsx'
        df_categorias = pd.read_excel(url_for_pandas)

        driver.find_element(By.CSS_SELECTOR, '*[name="ml_premium"]').clear()
        driver.find_element(By.CSS_SELECTOR, '*[name="ml_premium"]').send_keys('Sem envio')
        driver.find_element(By.CSS_SELECTOR, '*[name="ml_premium"]').send_keys(Keys.TAB)

        driver.find_element(By.CSS_SELECTOR, '*[name="ml_normal"]').clear()
        driver.find_element(By.CSS_SELECTOR, '*[name="ml_normal"]').send_keys('Sem envio')
        driver.find_element(By.CSS_SELECTOR, '*[name="ml_normal"]').send_keys(Keys.TAB)

        driver.find_element(By.CSS_SELECTOR, '*[name="possuiEstoque"]').clear()
        driver.find_element(By.CSS_SELECTOR, '*[name="possuiEstoque"]').send_keys('Sim')
        driver.find_element(By.CSS_SELECTOR, '*[name="possuiEstoque"]').send_keys(Keys.TAB)
        
        driver.find_element(By.CSS_SELECTOR, '*[name="perpage"]').click()
        click(driver, get_element_by_text(driver, '500'))

        for i in range(len(df_categorias)):
            if str(df_categorias.loc[i, 'Categoria']) == 'nan':
                df_categorias.loc[i, 'Categoria'] = df_categorias.loc[i-1, 'Categoria']
            print('Procurando por:', df_categorias.loc[i, 'Peça'], ' - Categoria ser vinculado:', '-', df_categorias.loc[i, 'Categoria'])

            categoria = df_categorias.loc[i, 'Categoria']

            driver.find_element(By.CSS_SELECTOR, '*[name="nome"]').clear()
            driver.find_element(By.CSS_SELECTOR, '*[name="nome"]').send_keys(df_categorias.loc[i, 'Peça'])

            time.sleep(1)
            #Realizar pesquisa dos produtos da categoria (Por nome)
            get_element_by_text(driver, 'Atualizar').click()
            time.sleep(3)

            produtos_encontrados = []
            for tr in driver.find_elements(By.CSS_SELECTOR, 'tr[role="row"]'):
                busca_sku_re = re.match(r'\b\d{6}\b', tr.find_element(By.CSS_SELECTOR, '*:nth-child(2)').text)
                if busca_sku_re:
                    produtos_encontrados.append((busca_sku_re.string, categoria))
                    print('Produto selecionado: ', busca_sku_re.string)
                    
                    #Selecionar os produtor com o padrão de seis dígitos
                    tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').click()

            if len(produtos_encontrados) == 0:
                continue

            get_element_by_text(driver, 'Incluir Múltiplo').click()
            get_element_by_text(driver, 'Mercado Livre').click()

            time.sleep(2)

            driver.find_element(By.CSS_SELECTOR, '*[name="anuncioML/categoria"]').clear()
            driver.find_element(By.CSS_SELECTOR, '*[name="anuncioML/categoria"]').send_keys(categoria)
            driver.find_element(By.CSS_SELECTOR, '*[name="anuncioML/categoria"]').send_keys(Keys.TAB)
            time.sleep(3)
            
            driver.find_element(By.CSS_SELECTOR, '*[name="anuncioML/condicao"]').clear()
            driver.find_element(By.CSS_SELECTOR, '*[name="anuncioML/condicao"]').send_keys('Usado')
            driver.find_element(By.CSS_SELECTOR, '*[name="anuncioML/condicao"]').send_keys(Keys.TAB)
            
            #Cria o arquivo se ele não existir
            with open('db.sqlite3', 'a') as file:
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                #Cria a tabela se e somente se ela não existir
                cursor.execute(f'CREATE TABLE IF NOT EXISTS PRODUTO_CATEGORIA (PRODUTO TEXT(10) PRIMARY KEY,CATEGORIA TEXT(10))')
                try:
                    cursor.executemany('INSERT INTO PRODUTO_CATEGORIA (PRODUTO, CATEGORIA) VALUES (?,?)', produtos_encontrados)
                except Exception as ex:
                    print('Erro durante a inserção de produto/categoria no banco de dados:', ex)

                connection.commit()
                cursor.close()
                connection.close()

            click(driver, get_element_by_text(driver, 'Gravar'))
            time.sleep(2)
            click(driver, get_element_by_text(driver, 'OK', multiple=True), True)
            time.sleep(2)
            click(driver, get_element_by_text(driver, 'Fechar'))
            time.sleep(2)
            
    ### Parte 2
    if opcao_usuario in ('2', ''):
        get_element_by_text(driver, 'MagaZord', texto_exato=False).click()
        driver.find_element(By.CSS_SELECTOR, '*[title="Marketplace"]').click()
        driver.find_element(By.CSS_SELECTOR, '*[title="Mercado Livre"]').click()
        time.sleep(1)
        click(driver, get_element_by_text(driver, 'Outros'))
        click(driver, get_element_by_text(driver, 'Ficha Técnica'))
        time.sleep(1)

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor = cursor.execute('SELECT PRODUTO, CATEGORIA FROM PRODUTO_CATEGORIA')
        for linha in cursor.fetchall():
            #Pegar o último elemento criado com esse conteúdo. Pode existir o mesmo botão "Incluir" em outras abas
            click(driver, get_element_by_text(driver, 'Incluir', multiple=True)[-1])
            time.sleep(1)

            produto, categoria = linha
            print('Criar ficha ténica para ', produto, ' na categoria ', categoria)
            produtoEl = driver.find_elements(By.CSS_SELECTOR, '*[name="produtoDerivacao/codigo"]')[-1]
            produtoEl.send_keys(produto)
            produtoEl.send_keys(Keys.TAB)
            time.sleep(1)

            CategoriaEl = driver.find_elements(By.CSS_SELECTOR, '*[name="categoriaML"]')[-1]
            CategoriaEl.send_keys(categoria)
            CategoriaEl.send_keys(Keys.TAB)
            time.sleep(1)

            click(driver, get_element_by_text(driver, 'Carregar Info. Adicionais'))
            time.sleep(3)

            #Carregar Info. Adicionais
            seletor_tr = 'div.x-window-closable.x-resizable tr:has(> td > div.x-trigger-index-0)'
            for i, tr in enumerate(driver.find_elements(By.CSS_SELECTOR, seletor_tr)):
                if i == 0:
                    continue
                input = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1) input')
                if not input.get_property('value'):
                    #Estava fazendo muito rápido e dando alguns erros
                    time.sleep(0.5)
                    escolher_com_seta = True
                    if input.get_property('name').upper().count('COLOR'):
                        input.send_keys('Preto')
                        input.send_keys(Keys.TAB)                

                        escolher_com_seta = False
                    
                    if input.get_property('name').upper().count('POSITION'):
                        seletor_css_descricao_produto = 'input[name="produtoDerivacao/produto/nome"]:not([data-errorqtip])'
                        
                        if driver.find_element(By.CSS_SELECTOR, seletor_css_descricao_produto).get_property('value').upper().count('ESQUERD'):
                            input.send_keys('Esquerdo')                
                            input.send_keys(Keys.TAB)                
                            escolher_com_seta = False
                        if driver.find_element(By.CSS_SELECTOR, seletor_css_descricao_produto).get_property('value').upper().count('DIREIT'):
                            input.send_keys('Direito')
                            input.send_keys(Keys.TAB)                
                            escolher_com_seta = False

                        if driver.find_element(By.CSS_SELECTOR, seletor_css_descricao_produto).get_property('value').upper().count('DIANTEIR'):
                            input.send_keys('Dianteiro')
                            input.send_keys(Keys.TAB)                
                            escolher_com_seta = False
                        if driver.find_element(By.CSS_SELECTOR, seletor_css_descricao_produto).get_property('value').upper().count('TRASEIR'):
                            input.send_keys('Traseiro')
                            input.send_keys(Keys.TAB)                
                            escolher_com_seta = False

                    if escolher_com_seta:
                        #Clique na seta
                        tr.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').click()
                        #Apertar seta do teclado para baixo
                        input.send_keys(Keys.ARROW_DOWN)
                        input.send_keys(Keys.ENTER)
                    
            for el in driver.find_elements(By.CSS_SELECTOR, 'div.x-window-closable.x-resizable input[type="text"]'):
                if not el.get_property('value') and not el.get_property('name') in ('customFields/customAttValue', 'customFields/customAttName'):
                    el.send_keys('1')
            
            click(driver, get_element_by_text(driver, 'Gravar'))

            cursor.execute('DELETE FROM PRODUTO_CATEGORIA WHERE PRODUTO = ?', [produto])
            connection.commit()

            time.sleep(2)
            click(driver, get_element_by_text(driver, 'Fechar'))

        cursor.close()
        connection.close()

        '''
        #Volta para a aba de anúncios do ML
        get_element_by_text(driver, 'Consultar Anúncio Mercado Livre').click()
        driver.find_element(By.CSS_SELECTOR, '[name="anuml_situacao"]').click()
        get_element_by_text(driver, 'Não Enviado').click()
        click(driver, driver.find_elements(\
            By.CSS_SELECTOR, 'span > div > div > div > div > a > span > span > span.x-btn-inner.x-btn-inner-center'), True)

        time.sleep(2)
        
        for checkbox in driver.find_elements(By.CSS_SELECTOR, '.x-grid-row-checker'):
            checkbox.click()
        time.sleep(15)
        #get_element_by_text(driver, 'Enviar').click()
        '''
        print('Falta Enviar!')

    return driver

if __name__ == '__main__':
    executar()
    #print('.')
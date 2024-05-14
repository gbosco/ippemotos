import upload_yt, vincula_video_zord, executa_photoroom, envia_ml_zord
from navegador import get_driver_navegador

escolha_usuario = ''
driver = get_driver_navegador()

while escolha_usuario != '0':
    try:
        
        msg_menu = \
        '''
        Escolha uma opção:
        1 - Photoroom
        2 - UPLOAD vídeo para o YouTube e gerar arquivo 
        3 - Ler arquivo e víncular ao Produto no Zord
        4 - Realizar envios por categoria do ML

        0 - Para Sair
        '''
        escolha_usuario = input(msg_menu)
        if escolha_usuario == '1':
            driver = executa_photoroom.executar(driver)
        if escolha_usuario == '2':
            driver = upload_yt.executar(driver)
        if escolha_usuario == '3':
            driver = vincula_video_zord.executar(driver)
        if escolha_usuario == '4':
            driver = envia_ml_zord.executar(driver, input('1 - Somente carregar envios. 2 - Somente preencher ficha técnica. ENTER para ambos'))
    except Exception as ex:
        print('Erro:')
        print(ex)
        input('Aperte enter para prosseguir')
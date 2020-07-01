import requests as r
from bs4 import BeautifulSoup as BS


def getstatus():
    """
    ~~ Essa função verifica o status de um endereço web dado.
    :return: Retorna o código da requisição, caso haja erro, informa uma mensagem dizendo o nome do erro
    """
    try:
        # Variável global para poder manipular em outra função, se status_code == 200
        global resp
        resp = r.get('https://www.comprasparaguai.com.br')
        resp.encoding = 'utf-8'
    except r.exceptions.RequestException:
        print(f'Not possible ~~getstatus~~ {r.exceptions.RequestException.__name__}')
    finally:
        return resp.status_code


def getcoins():  # Pegando o status da página, consegue acessar, se disponível, os dados em json.
    """
    ~~ Essa função, através do código passado pela def getstatus, faz um scrap pegando a cotação
    do site Compras Paraguai e cria um arquivo json com esses valores.
    :return: Retorna uma mensagem de erro, caso a def getstatus não consiga acessar o link
    """
    if updates():
        if getstatus() == 200:
            html = BS(resp.text, 'html.parser')  # Passando para obj HTML

            # Lista com a tag atacada: valores das cotações
            cot = html.find_all(class_='flex justify-content-center align-items-center flex-grow-1 text-center')

            cotacoes = list()
            for m in cot:
                cotation = m.span.text
                flag = m.img['src']

                cotacoes.append({
                    'cotacao': cotation,
                    'bandeira': flag
                })

                # Tendo as infos, gravar em um arquivo local para não ter que consultar sempre o site
                with open('valores_dia.json', 'w') as json_file:  # Criando um json com os dados obtidos
                    import json
                    json.dump(cotacoes, json_file, indent=4, ensure_ascii=False)

        else:
            return f'Não foi possível: Code {getstatus()}'


def updates():
    from datetime import datetime

    update = datetime.now()  # Pegando a data e hora atual do sistema
    update = update.strftime('%d/%m - %H:%M:%S')  # Formatando no padrão DD/MM - HH:MM:SS

    try:
        if not check():
            arquivo = open('logs.txt', 'w')
        else:
            arquivo = open('logs.txt')
    except BaseException:
        print(f'Not possible ~~Updates~~: {BaseException.__name__}')
    else:
        if check() and delta(update) > 12 or not check():
            arquivo.write(update)
            up = True
        else:
            up = False
        arquivo.close()
        return up


def check():  # Checa se existe um arquivo de log
    """
    ~~ Função para verificar se há um arquivo de log criado.
    :return: Retorna True se já foi criado um arquivo de log e não está vazio,
    False se não existir o arquivo
    """
    try:
        arquivo = open('logs.txt')
    except BaseException:
        # Se não abre, ele cria retornando falso
        return False
    else:
        last_update = arquivo.readline()
        verif = True if last_update != '' else False
        arquivo.close()
        return verif


def delta(horario):
    """
    Essa função informa a diferença em horas entre duas datas. Uma, passada por parâmetro
    e a outra via arquivo.
    :param horario: Parâmetro passado em dd/mm - HH:MM:SS
    :return: Retorna a diferença entre HH(parâmetro) e HH(arquivo)
    """
    from datetime import datetime as dt
    global prev_up, last_up

    new = horario
    try:  # Tentando pegar a data e horário no arquivo de log
        arquivo = open('logs.txt')
        old = arquivo.readline()
    except BaseException:
        print(f'Not possible ~~delta~~: {BaseException.__name__}')
        prev_up = -1000  # Gambiarra provisória para deixar o dif negativo
    else:
        last_up = int(dt.strptime(new, '%d/%m - %H:%M:%S').strftime('%H'))
        prev_up = int(dt.strptime(old, '%d/%m - %H:%M:%S').strftime('%H'))
    finally:
        dif = last_up - prev_up
        dif = dif + 24 if dif < 0 else dif
    return dif

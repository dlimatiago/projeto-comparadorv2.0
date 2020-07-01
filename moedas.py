def convert_json_pyhton(arquivo):
    """
    ~~ Converte um arquivo json em um objeto python
    :param arquivo: Nome do arquivo json a ser convertido
    :return: um objeto python
    """
    import json as j

    try:
        with open(arquivo, 'r') as json_file:
            dados_m = j.load(json_file)  # Transformando em objeto python <dict>
            return dados_m
    except BaseException:
        return None


def usd_cot(pais='Brasil'):
    """
    ~~ Informa a cotação do dia, informado o país
    :param pais: Nome do país a ser consultada a cotação
    :return: Uma string formatada com a cotação dólar turístico - moeda escolhida
    """
    val = convert_json_pyhton('valores_dia.json')

    for p in val:
        if pais.lower() in p['bandeira']:
            return f"U$ 1,00 ➟ {p['cotacao']}"


if __name__ == '__main__':
    print(usd_cot())

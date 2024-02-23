import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urlencode
import concurrent.futures
import time
from datetime import datetime
import json

# Definir a URL base e os parâmetros padrão
base_url = 'https://www.melodybrazil.com/search'
default_params = {
    'updated-max': '2024-02-15T12%3A00%3A00-03%3A00',
    'max-results': '20',
}

# Função para extrair dados da página
def extrair_dados_pagina(url):
    print("Extraindo dados da página:", url)
    pagina = requests.get(url)
    site = BeautifulSoup(pagina.content, 'html.parser')
    music = site.find_all('div', attrs={'class': 'grid-posts'})
    dados = []
    for musi in music:
        for div in musi.find_all('div', recursive=False):
            url_publicacao = div.find('a')['href']
            nome_publicacao = div.find('h2', class_='post-title').text
            data_publicacao = div.find('time', class_='post-datepublished').text.strip()
            publicacao_por_tag = div.find('span', class_='post-author')
            publicacao_por = publicacao_por_tag.text.strip() if publicacao_por_tag else 'Autor Desconhecido'
            url_download = div.find('a', class_='read-more')['href']
            dados.append([url_publicacao, nome_publicacao, data_publicacao, publicacao_por, url_download])
    return dados

# Função para extrair dados de uma única página
def extrair_dados_pagina_individual(url):
    try:
        return extrair_dados_pagina(url)
    except Exception as e:
        print(f"Erro ao extrair dados da página {url}: {e}")
        return []

# Função para extrair dados de várias páginas em paralelo
def extrair_dados_paralelo(base_url, params, total_pages):
    dados_totais = []
    urls = [f'{base_url}?{urlencode(params)}&PageNo={i}' for i in range(total_pages)]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = executor.map(extrair_dados_pagina_individual, urls)
        for resultado in resultados:
            dados_totais.extend(resultado)
    
    return dados_totais

# Função para salvar dados em um arquivo JSON com a data da atualização
def salvar_dados_json_com_data(dados, prefixo='dados_melody_brazil'):
    data_atualizacao = datetime.now().strftime("%Y-%m-%d")
    filename = f'{prefixo}_{data_atualizacao}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {filename}")


# Número máximo de páginas para buscar inicialmente
MAX_PAGES_INITIAL = 2960
# Intervalo de atualização em segundos (24 horas)
UPDATE_INTERVAL_SECONDS = 24 * 60 * 60

# Loop infinito para extração e atualização de dados
while True:
    # Extrair dados de todas as páginas
    dados_totais = extrair_dados_paralelo(base_url, default_params, MAX_PAGES_INITIAL)
    
    # Salvar os dados em um arquivo JSON com a data da atualização
    salvar_dados_json_com_data(dados_totais)
    
    print("Aguardando próxima atualização...")
    # Aguardar o intervalo de atualização antes de executar novamente
    time.sleep(UPDATE_INTERVAL_SECONDS)



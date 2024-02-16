import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urlencode

# Definir a URL base e os parâmetros padrão
base_url = 'https://www.melodybrazil.com/search'
default_params = {
    'updated-max': '2024-02-15T12%3A00%3A00-03%3A00',
    'max-results': '20',
}

# Função para extrair dados da página
def extrair_dados_pagina(url):
    # Imprime a URL da página que está sendo extraída
    print("Extraindo dados da página:", url)
    
    # Faz uma requisição GET para a URL
    pagina = requests.get(url)
    
    # Usa BeautifulSoup para analisar o conteúdo da página
    site = BeautifulSoup(pagina.content, 'html.parser')
    
    # Encontra todos os elementos 'div' com a classe 'grid-posts'
    music = site.find_all('div', attrs={'class': 'grid-posts'})
    
    # Inicializa uma lista para armazenar os dados extraídos
    dados = []
    
    # Itera sobre cada elemento 'div' encontrado
    for musi in music:
        for div in musi.find_all('div', recursive=False):
            # Extrai a URL, o nome, a data e o autor da publicação
            url_publicacao = div.find('a')['href']
            nome_publicacao = div.find('h2', class_='post-title').text
            data_publicacao = div.find('time', class_='post-datepublished').text.strip()
            publicacao_por_tag = div.find('span', class_='post-author')
            publicacao_por = publicacao_por_tag.text.strip() if publicacao_por_tag else 'Autor Desconhecido'
            url_download = div.find('a', class_='read-more')['href']
            
            # Adiciona os dados extraídos à lista
            dados.append([url_publicacao, nome_publicacao, data_publicacao, publicacao_por, url_download])
    
    # Retorna a lista de dados
    return dados

# Extrair dados da página inicial
dados_totais = []
params = default_params.copy()
url = f'{base_url}?{urlencode(params)}'
dados_pagina = extrair_dados_pagina(url)
dados_totais.extend(dados_pagina)

# Extrair dados das demais páginas (se houver) até a página 100
pagina_atual = 0
while pagina_atual <= 100:  # Limite de 100 páginas
    params['PageNo'] = pagina_atual
    url = f'{base_url}?{urlencode(params)}'
    
    # Imprime a URL da página que está sendo extraída
    print("Extraindo dados da página:", url)
    
    # Faz uma requisição GET para a URL
    pagina = requests.get(url)
    
    # Se a página não existir (status code 404), interrompe o loop
    if pagina.status_code == 404:
        break
    
    # Usa BeautifulSoup para analisar o conteúdo da página
    site = BeautifulSoup(pagina.content, 'html.parser')
    
    # Se a página não contiver nenhum elemento 'div' com a classe 'grid-posts', interrompe o loop
    if not site.find('div', class_='grid-posts'):
        break
    
    # Extrai os dados da página
    dados_pagina = extrair_dados_pagina(url)
    
    # Adiciona os dados extraídos à lista total de dados
    dados_totais.extend(dados_pagina)
    
    # Incrementa o número da página
    pagina_atual += 1

# Criar DataFrame e salvar em um arquivo Excel
df = pd.DataFrame(dados_totais, columns=['URL da Publicação', 'Nome da Publicação', 'Data da Publicação', 'Publicado por', 'URL de Download'])
df.to_excel('dados_melody_brazil.xlsx', index=False)

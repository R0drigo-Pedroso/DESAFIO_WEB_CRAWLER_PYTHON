# Web Scraper para Melody Brazil

Este é um script Python para extrair dados do site Melody Brazil. Ele extrai informações como URL da publicação, nome da publicação, data da publicação, quem publicou e URL de download.

## Dependências

Este projeto depende das seguintes bibliotecas Python:

- requests
- BeautifulSoup4
- pandas

Você pode instalar essas dependências usando pip:

```bash
pip install requests beautifulsoup4 pandas
```

## Como usar

1. Clone este repositório ou baixe o arquivo do script.
2. Instale as dependências conforme descrito acima.
3. Execute o script com o comando `python nome_do_script.py`.
4. O script irá extrair os dados e salvá-los em um arquivo Excel chamado 'dados_melody_brazil.xlsx'.

## Detalhes do Código

O script começa definindo a URL base e os parâmetros padrão para a busca. Em seguida, ele define uma função `extrair_dados_pagina` que é usada para extrair os dados de uma única página. Esta função usa a biblioteca BeautifulSoup para analisar o HTML da página e extrair os dados relevantes.

Depois disso, o script extrai os dados da página inicial e, em seguida, entra em um loop para extrair dados das páginas subsequentes até a página 20 ou até que não haja mais páginas.

Finalmente, ele cria um DataFrame pandas com os dados extraídos e salva esse DataFrame em um arquivo Excel.
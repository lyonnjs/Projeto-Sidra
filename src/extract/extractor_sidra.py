import requests
import pandas as pd

class SidraExtractor:
    def __init__(self, api_base_url="https://apisidra.ibge.gov.br/values"):
        self.api_base_url = api_base_url

    def montar_url(self, tabela, variaveis, periodo,
                   classificacao=None, categorias=None,
                   nivel="n1", local="all"):

        url = f"{self.api_base_url}/t/{tabela}/{nivel}/{local}/v/{variaveis}/p/{periodo}"
        if classificacao and categorias:
            if isinstance(categorias, (list, tuple)):
                categorias = ",".join(map(str, list(set(categorias))))
            url += f"/c{classificacao}/{categorias}"
        return url

    def extrair(self, tabela, variaveis, periodo,
                classificacao=None, categorias=None,
                nivel="n1", local="all"):
 
        url = self.montar_url(tabela, variaveis, periodo, classificacao, categorias, nivel, local)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data[1:], columns=data[0])
        else:
            raise Exception(f"Erro ao conectar: {response.status_code}")
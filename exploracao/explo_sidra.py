import requests
import pandas as pd


# variaveis globais
api_base_url = "https://apisidra.ibge.gov.br/values"

def montar_url(tabela, variaveis, periodo, classificacao=None, categorias=None, nivel="n1", local="all"):
    url = f"{api_base_url}/t/{tabela}/{nivel}/{local}/v/{variaveis}/p/{periodo}"
    if classificacao and categorias:
        if isinstance(categorias, (list, tuple)):
            categorias = ",".join(map(str, list(set(categorias))))
        url += f"/c{classificacao}/{categorias}"
    return url

def extrai_dados(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    else:
        raise Exception(f"Erro ao acessar a API: {response.status_code}")


def salvar_dados(df, caminho_arquivo):
    df.to_csv(caminho_arquivo, index=False)

# Executar consulta
categorias = [107638, 12433, 7459, 12398, 47634, 107639, 107640, 107641, 107642, 107643]
url = montar_url(tabela=7060, variaveis=63, periodo="202001-202508", 
                 classificacao=315, categorias=categorias, nivel="n7", local="all")

df = extrai_dados(url)
salvar_dados(df, "bronze/dados_sidra.csv")

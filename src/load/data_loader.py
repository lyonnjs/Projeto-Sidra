import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from transform.transformer_data import TransformerData
from transform.transformer_gold import TransformerGold

class DataLoader:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def carregar_dados(self):
        return pd.read_csv(self.caminho_arquivo)

    def salvar_dados_csv(self, df, caminho_saida):
        df.to_csv(caminho_saida, index=False)
        
    def salvar_dados_parquet(self, df, caminho_saida):
        df.to_parquet(caminho_saida, index=False)
        
    def salvar_dados_gold(self, df, caminho_saida):
        df.to_csv(caminho_saida, index=False)       

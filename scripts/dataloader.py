import pandas as pd
import openpyxl

from transformer_data import TransformerData

class DataLoader:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def carregar_dados(self):
        return pd.read_csv(self.caminho_arquivo)

    def salvar_dados_csv(self, df, caminho_saida):
        df.to_csv(caminho_saida, index=False)
    
    def salvar_dados_excel(self, df, caminho_saida):
        df.to_excel(caminho_saida, index=False)

        
  
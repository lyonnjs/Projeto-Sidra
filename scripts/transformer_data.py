import pandas as pd

class TransformerData:
    def __init__(self, df):
        self.df = df


    def organizar_dados_regionais(self):
        df_clean = self.df.copy()
        
        df_clean ["Estado"] = df_clean["D1N"].str.extract(r' - ([A-Z]{2})$')
        
        df_clean['Regiao_Metropolitana'] = df_clean['D1N'].str.replace(r' - [A-Z]{2}$', '', regex=True)
           
        df_clean = df_clean.rename(columns={
        'D1N': 'RM_Completo',
        'D2N': 'Indicador', 
        'D3N': 'Periodo',
        'D4N': 'Categoria',
        'V': 'Valor',
        'MN': 'Unidade'
        })
    
        # Converter valores numéricos
        df_clean['Valor_Numerico'] = pd.to_numeric(df_clean['Valor'], errors='coerce')
        
        # Selecionar colunas relevantes
        colunas_finais = ['Estado', 'Regiao_Metropolitana', 'RM_Completo', 
                        'Indicador', 'Periodo', 'Categoria', 'Valor', 'Valor_Numerico', 'Unidade']
        
        return df_clean[colunas_finais]
    
    def transformar(self):
        df_transformado = self.organizar_dados_regionais()
        
        return df_transformado


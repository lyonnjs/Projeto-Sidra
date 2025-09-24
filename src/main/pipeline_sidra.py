import sys
import os
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.extractor_sidra import SidraExtractor
from transform.transformer_data import TransformerData
from transform.transformer_gold import TransformerGold
from load.data_loader import DataLoader

class PipelineSidra:
    def __init__(self, bronze_dir="bronze", silver_dir="silver", gold_dir="gold"):
        self.bronze_dir = bronze_dir
        self.silver_dir = silver_dir
        self.gold_dir = gold_dir
        self._criar_diretorios()
        
    
    def _criar_diretorios(self):
        os.makedirs(self.bronze_dir, exist_ok=True)
        os.makedirs(self.silver_dir, exist_ok=True)
        os.makedirs(self.gold_dir, exist_ok=True)
    
    
    def executar_pipeline(self, tabela, variaveis, periodo, classificacao=None, categorias=None,
                        nivel="n1", local="all", nome_arquivo="dados_sidra"):
        
        print("Iniciando extração de dados...")
        extractor = SidraExtractor()
        df_raw = extractor.extrair(
            tabela=tabela,
            variaveis=variaveis,
            periodo=periodo,
            classificacao=classificacao,
            categorias=categorias,
            nivel=nivel,
            local=local
        )
        
        #salvar dados brutos
        caminho_bronze = os.path.join(self.bronze_dir, f"{nome_arquivo}.csv")
        caminho_bronze_parquet = os.path.join(self.bronze_dir, f"{nome_arquivo}.parquet")
        loader_bronze = DataLoader(caminho_bronze)
        loader_bronze.salvar_dados_csv(df_raw, caminho_bronze)
        loader_bronze.salvar_dados_parquet(df_raw, caminho_bronze_parquet)
        print(f"Dados brutos salvos em {caminho_bronze} e {caminho_bronze_parquet}")

        # transformar dados
        print("Iniciando transformação de dados...")
        transformer = TransformerData(df_raw)
        df_transformado = transformer.transformar()
        print("Transformação concluída.")
        
        # salvar dados transformados
        caminho_silver = os.path.join(self.silver_dir, f"{nome_arquivo}_transformado.csv")
        caminho_silver_parquet = os.path.join(self.silver_dir, f"{nome_arquivo}_transformado.parquet")
        loader_silver = DataLoader(caminho_silver)
        loader_silver.salvar_dados_csv(df_transformado, caminho_silver)
        loader_silver.salvar_dados_parquet(df_transformado, caminho_silver_parquet)
        print(f"Dados transformados salvos em {caminho_silver} e {caminho_silver_parquet}")

        # transformar para gold
        print("Iniciando transformação para dados gold...")
        transformer_gold = TransformerGold(df_transformado)
        df_gold = transformer_gold.gerar_kpis()
        print("Transformação para gold concluída.")

        # salvar dados gold
        for nome_kpi, df_gold in df_gold.items():
            if isinstance(df_gold, pd.DataFrame):
                caminho_csv = os.path.join(self.gold_dir, f"{nome_arquivo}_{nome_kpi}.csv")
                caminho_parquet = os.path.join(self.gold_dir, f"{nome_arquivo}_{nome_kpi}.parquet")
                
                loader_gold = DataLoader(caminho_csv)
                loader_gold.salvar_dados_csv(df_gold, caminho_csv)
                loader_gold.salvar_dados_parquet(df_gold, caminho_parquet)
                print(f"KPI '{nome_kpi}' salvo em {caminho_csv} e {caminho_parquet}")
                
        return df_transformado                

            
if __name__ == "__main__":
    categorias = [107638, 12433, 7459, 12398, 47634, 107639, 107640, 107641, 107642, 107643]
    
    pipeline = PipelineSidra()
    df_final = pipeline.executar_pipeline(
        tabela=7060,
        variaveis=63,
        periodo="202001-202508",
        classificacao=315,
        categorias=categorias,
        nivel="n7",
        local="all",
        nome_arquivo="dados_sidra"
    )        
    
    print("\nExemplo dos dados transformados:")
    print(df_final.head())
        
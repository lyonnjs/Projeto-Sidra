import pandas as pd
from extractor_sidra import SidraExtractor
from dataloader import DataLoader
from transformer_data import TransformerData
from transformer_kpi import TransformerGold
import os

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
        loader_bronze = DataLoader(caminho_bronze)
        loader_bronze.salvar_dados_csv(df_raw, caminho_bronze)
        print(f"Dados brutos salvos em {caminho_bronze}")
        
        # transformar dados
        print("Iniciando transformação de dados...")
        transformer = TransformerData(df_raw)
        df_transformado = transformer.transformar()
        print("Transformação concluída.")
        
        # salvar dados transformados
        caminho_silver_csv = os.path.join(self.silver_dir, f"{nome_arquivo}_transformado.csv")
        caminho_silver_excel = os.path.join(self.silver_dir, f"{nome_arquivo}_transformado.xlsx")
        
        loader_silver = DataLoader(caminho_silver_csv)
        loader_silver.salvar_dados_csv(df_transformado, caminho_silver_csv)
        loader_silver.salvar_dados_excel(df_transformado, caminho_silver_excel)
        print(f"Dados transformados salvos em {caminho_silver_csv} e {caminho_silver_excel}")
        
        self._gerar_relatorio(df_raw, df_transformado)
        
        # gerar indicadores (gold)
        print("Gerando indicadores (KPI)...")
        gold = TransformerGold(df_transformado)
        kpis = gold.gerar_kpis()

        # salvar cada KPI em CSV e Excel
        for nome, df_kpi in kpis.items():
            caminho_csv = os.path.join(self.gold_dir, f"{nome}.csv")
            caminho_excel = os.path.join(self.gold_dir, f"{nome}.xlsx")
            df_kpi.to_csv(caminho_csv, index=False)
            df_kpi.to_excel(caminho_excel, index=False)
    
            print(f"KPI '{nome}' salvo em {caminho_csv} e {caminho_excel}")
            
        return df_transformado
    
    def _gerar_relatorio(self, df_raw, df_transformado):
        """Gera relatório da pipeline"""
        print("\n📊 RELATÓRIO DA PIPELINE:")
        print(f"   • Registros extraídos: {len(df_raw)}")
        print(f"   • Registros após transformação: {len(df_transformado)}")
        print(f"   • Colunas originais: {len(df_raw.columns)}")
        print(f"   • Colunas finais: {len(df_transformado.columns)}")
        print("✅ Pipeline executada com sucesso!")
        

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
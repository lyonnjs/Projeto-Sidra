import pandas as pd

class TransformerGold:
    def __init__(self, df_silver):
        self.df = df_silver

    def gerar_kpis(self):
        kpis = {}

        # 1. Variação média mensal por Estado
        kpis["media_estado_mensal"] = (
            self.df.groupby(["Estado", "Periodo"])["Valor_Numerico"]
            .mean()
            .reset_index()
        )

        # 2. Ranking de categorias (média geral no período)
        kpis["ranking_categorias"] = (
            self.df.groupby("Categoria")["Valor_Numerico"]
            .mean()
            .reset_index()
            .sort_values("Valor_Numerico", ascending=False)
        )

        # 3. Acumulado anual por Estado e Categoria
        if "Ano" not in self.df.columns:
            self.df["Ano"] = self.df["Periodo"].astype(str).str[:4]
        kpis["acumulado_anual_estado_categoria"] = (
            self.df.groupby(["Estado", "Ano", "Categoria"])["Valor_Numerico"]
            .sum()
            .reset_index()
        )

        # 4. Volatilidade por Categoria (desvio-padrão)
        kpis["volatilidade_categoria"] = (
            self.df.groupby("Categoria")["Valor_Numerico"]
            .std()
            .reset_index()
            .rename(columns={"Valor_Numerico": "Desvio_Padrao"})
        )

        # 5. Top 5 Regiões Metropolitanas com maior inflação média
        kpis["top5_rm"] = (
            self.df.groupby("Regiao_Metropolitana")["Valor_Numerico"]
            .mean()
            .reset_index()
            .sort_values("Valor_Numerico", ascending=False)
            .head(5)
        )

        return kpis
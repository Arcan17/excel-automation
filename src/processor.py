"""
Sales data processing and analysis.
"""
import pandas as pd
from dataclasses import dataclass


@dataclass
class SalesSummary:
    total_revenue: float
    total_units: int
    total_transactions: int
    avg_transaction: float
    monthly_sales: pd.DataFrame
    top_products: pd.DataFrame
    sales_by_seller: pd.DataFrame
    sales_by_region: pd.DataFrame


def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath, parse_dates=["Fecha"])
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["Fecha", "Producto", "Vendedor", "Total"])
    df = df[df["Total"] > 0]
    df = df[df["Cantidad"] > 0]
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Mes"] = df["Fecha"].dt.to_period("M")
    df["Mes_Nombre"] = df["Fecha"].dt.strftime("%B %Y")
    return df


def analyze(df: pd.DataFrame) -> SalesSummary:
    total_revenue = df["Total"].sum()
    total_units = df["Cantidad"].sum()
    total_transactions = len(df)
    avg_transaction = df["Total"].mean()

    monthly_sales = (
        df.groupby("Mes")
        .agg(
            Ventas_Totales=("Total", "sum"),
            Unidades=("Cantidad", "sum"),
            Transacciones=("Total", "count"),
        )
        .reset_index()
    )
    monthly_sales["Mes"] = monthly_sales["Mes"].astype(str)
    monthly_sales = monthly_sales.sort_values("Mes")

    top_products = (
        df.groupby("Producto")
        .agg(
            Ventas_Totales=("Total", "sum"),
            Unidades=("Cantidad", "sum"),
            Transacciones=("Total", "count"),
        )
        .reset_index()
        .sort_values("Ventas_Totales", ascending=False)
        .head(5)
    )

    sales_by_seller = (
        df.groupby("Vendedor")
        .agg(
            Ventas_Totales=("Total", "sum"),
            Unidades=("Cantidad", "sum"),
            Transacciones=("Total", "count"),
        )
        .reset_index()
        .sort_values("Ventas_Totales", ascending=False)
    )

    sales_by_region = (
        df.groupby("Region")
        .agg(
            Ventas_Totales=("Total", "sum"),
            Unidades=("Cantidad", "sum"),
        )
        .reset_index()
        .sort_values("Ventas_Totales", ascending=False)
    )

    return SalesSummary(
        total_revenue=total_revenue,
        total_units=total_units,
        total_transactions=total_transactions,
        avg_transaction=avg_transaction,
        monthly_sales=monthly_sales,
        top_products=top_products,
        sales_by_seller=sales_by_seller,
        sales_by_region=sales_by_region,
    )

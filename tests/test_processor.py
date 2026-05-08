"""
Unit tests for the processor module.
"""
import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from data_generator import generate_sales_data
from processor import clean_data, analyze, SalesSummary


@pytest.fixture
def raw_df():
    return generate_sales_data(n_rows=100, year=2024)


@pytest.fixture
def clean_df(raw_df):
    return clean_data(raw_df)


@pytest.fixture
def summary(clean_df):
    return analyze(clean_df)


# --- clean_data ---

def test_clean_data_returns_dataframe(raw_df):
    result = clean_data(raw_df)
    assert isinstance(result, pd.DataFrame)


def test_clean_data_drops_nulls():
    df = generate_sales_data(n_rows=50)
    df.loc[0, "Total"] = None
    df.loc[1, "Producto"] = None
    result = clean_data(df)
    assert result["Total"].isna().sum() == 0
    assert result["Producto"].isna().sum() == 0


def test_clean_data_removes_non_positive_totals():
    df = generate_sales_data(n_rows=50)
    df.loc[0, "Total"] = 0
    df.loc[1, "Total"] = -500
    result = clean_data(df)
    assert (result["Total"] > 0).all()


def test_clean_data_adds_mes_column(clean_df):
    assert "Mes" in clean_df.columns
    assert "Mes_Nombre" in clean_df.columns


def test_clean_data_fecha_is_datetime(clean_df):
    assert pd.api.types.is_datetime64_any_dtype(clean_df["Fecha"])


# --- analyze ---

def test_analyze_returns_summary(summary):
    assert isinstance(summary, SalesSummary)


def test_total_revenue_positive(summary):
    assert summary.total_revenue > 0


def test_total_units_positive(summary):
    assert summary.total_units > 0


def test_total_transactions_matches_row_count(clean_df, summary):
    assert summary.total_transactions == len(clean_df)


def test_avg_transaction_is_mean(clean_df, summary):
    expected = clean_df["Total"].mean()
    assert abs(summary.avg_transaction - expected) < 0.01


def test_monthly_sales_has_required_columns(summary):
    expected_cols = {"Mes", "Ventas_Totales", "Unidades", "Transacciones"}
    assert expected_cols.issubset(set(summary.monthly_sales.columns))


def test_monthly_sales_revenue_sum_matches_total(summary):
    assert abs(summary.monthly_sales["Ventas_Totales"].sum() - summary.total_revenue) < 1


def test_top_products_has_at_most_5_rows(summary):
    assert len(summary.top_products) <= 5


def test_top_products_sorted_descending(summary):
    revenues = summary.top_products["Ventas_Totales"].tolist()
    assert revenues == sorted(revenues, reverse=True)


def test_sales_by_seller_covers_all_sellers(clean_df, summary):
    sellers_in_data = set(clean_df["Vendedor"].unique())
    sellers_in_summary = set(summary.sales_by_seller["Vendedor"].tolist())
    assert sellers_in_data == sellers_in_summary


def test_sales_by_region_covers_all_regions(clean_df, summary):
    regions_in_data = set(clean_df["Region"].unique())
    regions_in_summary = set(summary.sales_by_region["Region"].tolist())
    assert regions_in_data == regions_in_summary

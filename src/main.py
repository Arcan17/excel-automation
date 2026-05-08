"""
Entry point: generates sample data, processes it, and creates the Excel report.
"""
import os
import sys

# Allow running from repo root or from src/
sys.path.insert(0, os.path.dirname(__file__))

from data_generator import generate_sales_data
from processor import clean_data, analyze
from report_generator import generate_report


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ventas.xlsx")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "informe_ventas_2024.xlsx")


def main():
    # 1. Generate (or load) sales data
    print("Generando datos de ventas...")
    df_raw = generate_sales_data(n_rows=200, year=2024)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df_raw.to_excel(DATA_PATH, index=False)
    print(f"  Datos guardados en: {DATA_PATH}")

    # 2. Clean & analyze
    print("Procesando datos...")
    df = clean_data(df_raw)
    summary = analyze(df)
    print(f"  Total ingresos  : {summary.total_revenue:,.0f} CLP")
    print(f"  Total unidades  : {summary.total_units:,}")
    print(f"  Transacciones   : {summary.total_transactions:,}")
    print(f"  Ticket promedio : {summary.avg_transaction:,.0f} CLP")

    # 3. Generate Excel report
    print("Generando informe Excel...")
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    generate_report(summary, REPORT_PATH)


if __name__ == "__main__":
    main()

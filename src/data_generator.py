"""
Generates sample sales data for testing/demo purposes.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


PRODUCTS = [
    "Laptop Pro 15",
    "Monitor 4K",
    "Teclado Mecánico",
    "Mouse Inalámbrico",
    "Auriculares BT",
    "Webcam HD",
    "Hub USB-C",
    "SSD Externo 1TB",
    "Tablet 10'",
    "Smartphone X12",
]

SELLERS = ["Ana García", "Carlos López", "María Torres", "Juan Pérez", "Sofía Ruiz"]

REGIONS = ["Norte", "Sur", "Centro", "Oriente", "Occidente"]


def generate_sales_data(n_rows: int = 200, year: int = 2024) -> pd.DataFrame:
    random.seed(42)
    np.random.seed(42)

    start_date = datetime(year, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 364)) for _ in range(n_rows)]

    products = random.choices(PRODUCTS, k=n_rows)
    sellers = random.choices(SELLERS, k=n_rows)
    regions = random.choices(REGIONS, k=n_rows)

    base_prices = {
        "Laptop Pro 15": 850000,
        "Monitor 4K": 320000,
        "Teclado Mecánico": 65000,
        "Mouse Inalámbrico": 35000,
        "Auriculares BT": 89000,
        "Webcam HD": 55000,
        "Hub USB-C": 28000,
        "SSD Externo 1TB": 75000,
        "Tablet 10'": 290000,
        "Smartphone X12": 480000,
    }

    prices = [
        round(base_prices[p] * np.random.uniform(0.9, 1.1) / 1000) * 1000
        for p in products
    ]
    quantities = [random.randint(1, 5) for _ in range(n_rows)]

    df = pd.DataFrame(
        {
            "Fecha": dates,
            "Producto": products,
            "Vendedor": sellers,
            "Region": regions,
            "Precio_Unitario": prices,
            "Cantidad": quantities,
            "Total": [p * q for p, q in zip(prices, quantities)],
        }
    )

    df = df.sort_values("Fecha").reset_index(drop=True)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df


if __name__ == "__main__":
    df = generate_sales_data()
    output_path = "data/ventas.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Datos generados: {len(df)} filas → {output_path}")

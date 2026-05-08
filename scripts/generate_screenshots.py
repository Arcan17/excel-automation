"""
Generates PNG screenshots of the report sheets for the README.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import numpy as np

from data_generator import generate_sales_data
from processor import clean_data, analyze

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
C_HEADER  = "#2E4057"
C_ACCENT  = "#048A81"
C_ACCENT_L = "#C8F4F1"
C_ALT     = "#F2F7F7"
C_TOTAL   = "#054A91"
C_WHITE   = "#FFFFFF"
C_FG      = "#FFFFFF"

df_raw = generate_sales_data(n_rows=200, year=2024)
df = clean_data(df_raw)
s = analyze(df)


# ── SHEET 1: Resumen Ejecutivo ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor("#F8FAFA")
fig.patch.set_facecolor("#F8FAFA")
ax.axis("off")

# Title bar
title_bg = FancyBboxPatch((0.03, 0.88), 0.94, 0.10,
                           boxstyle="round,pad=0.01", linewidth=0,
                           facecolor=C_HEADER, transform=ax.transAxes)
ax.add_patch(title_bg)
ax.text(0.50, 0.935, "INFORME DE VENTAS 2024", transform=ax.transAxes,
        fontsize=18, fontweight="bold", color=C_FG, ha="center", va="center")

# KPI cards
kpis = [
    ("Ingresos Totales",   f"{s.total_revenue:,.0f} CLP"),
    ("Unidades Vendidas",  f"{s.total_units:,}"),
    ("Transacciones",      f"{s.total_transactions:,}"),
]
card_w, card_h = 0.28, 0.12
card_y_label, card_y_value = 0.72, 0.58
for i, (label, value) in enumerate(kpis):
    x = 0.05 + i * 0.32
    # label bg
    lbg = FancyBboxPatch((x, card_y_label), card_w, 0.07,
                          boxstyle="round,pad=0.005", linewidth=0,
                          facecolor=C_ACCENT, transform=ax.transAxes)
    ax.add_patch(lbg)
    ax.text(x + card_w/2, card_y_label + 0.035, label, transform=ax.transAxes,
            fontsize=9, fontweight="bold", color=C_FG, ha="center", va="center")
    # value bg
    vbg = FancyBboxPatch((x, card_y_value), card_w, 0.085,
                          boxstyle="round,pad=0.005", linewidth=0.8,
                          edgecolor="#CCCCCC", facecolor=C_WHITE, transform=ax.transAxes)
    ax.add_patch(vbg)
    ax.text(x + card_w/2, card_y_value + 0.042, value, transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=C_HEADER, ha="center", va="center")

# Top 5 table
ax.text(0.05, 0.53, "Top 5 Productos", transform=ax.transAxes,
        fontsize=12, fontweight="bold", color=C_HEADER, va="top")

top5 = s.top_products[["Producto", "Ventas_Totales", "Unidades"]].copy()
top5.columns = ["Producto", "Ventas (CLP)", "Unidades"]
top5["Ventas (CLP)"] = top5["Ventas (CLP)"].apply(lambda x: f"{x:,.0f}")
top5["Unidades"] = top5["Unidades"].apply(lambda x: f"{x:,}")

col_labels = list(top5.columns)
col_x = [0.05, 0.50, 0.80]
col_w = [0.43, 0.28, 0.17]
row_h = 0.055
header_y = 0.46

for ci, (lbl, cx) in enumerate(zip(col_labels, col_x)):
    hbg = patches.Rectangle((cx, header_y), col_w[ci], row_h,
                              linewidth=0, facecolor=C_HEADER, transform=ax.transAxes, clip_on=False)
    ax.add_patch(hbg)
    ax.text(cx + col_w[ci]/2, header_y + row_h/2, lbl, transform=ax.transAxes,
            fontsize=8.5, fontweight="bold", color=C_FG, ha="center", va="center")

for ri, row in enumerate(top5.itertuples(index=False)):
    row_y = header_y - (ri + 1) * row_h
    bg_col = C_ALT if ri % 2 == 1 else C_WHITE
    for ci, (val, cx) in enumerate(zip(row, col_x)):
        rbg = patches.Rectangle((cx, row_y), col_w[ci], row_h,
                                  linewidth=0.4, edgecolor="#CCCCCC",
                                  facecolor=bg_col, transform=ax.transAxes, clip_on=False)
        ax.add_patch(rbg)
        ha = "right" if ci > 0 else "left"
        tx = cx + col_w[ci] - 0.01 if ci > 0 else cx + 0.01
        ax.text(tx, row_y + row_h/2, str(val), transform=ax.transAxes,
                fontsize=8, color="#333333", ha=ha, va="center")

plt.tight_layout(pad=0.5)
out = os.path.join(OUT_DIR, "resumen_ejecutivo.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")


# ── SHEET 2: Ventas Mensuales ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#F8FAFA")

# Left: table
ax_t = axes[0]
ax_t.set_facecolor("#F8FAFA")
ax_t.axis("off")

# Title
tbg = FancyBboxPatch((0.0, 0.92), 1.0, 0.08, boxstyle="round,pad=0.005",
                      linewidth=0, facecolor=C_HEADER, transform=ax_t.transAxes)
ax_t.add_patch(tbg)
ax_t.text(0.5, 0.96, "VENTAS MENSUALES 2024", transform=ax_t.transAxes,
          fontsize=13, fontweight="bold", color=C_FG, ha="center", va="center")

df_m = s.monthly_sales.copy()
df_m.columns = ["Mes", "Ventas Totales", "Unidades", "Trans."]
df_m["Ventas Totales"] = df_m["Ventas Totales"].apply(lambda x: f"{x:,.0f}")
df_m["Unidades"] = df_m["Unidades"].apply(lambda x: f"{x:,}")
df_m["Trans."] = df_m["Trans."].apply(lambda x: f"{x:,}")

mcols = list(df_m.columns)
mw = [0.30, 0.38, 0.17, 0.15]
mx = [0.0, 0.30, 0.68, 0.85]
rh = 0.055
hy = 0.83

for ci, (lbl, cx, cw) in enumerate(zip(mcols, mx, mw)):
    hbg = patches.Rectangle((cx, hy), cw, rh, linewidth=0,
                              facecolor=C_HEADER, transform=ax_t.transAxes, clip_on=False)
    ax_t.add_patch(hbg)
    ax_t.text(cx + cw/2, hy + rh/2, lbl, transform=ax_t.transAxes,
              fontsize=8, fontweight="bold", color=C_FG, ha="center", va="center")

for ri, row in enumerate(df_m.itertuples(index=False)):
    ry = hy - (ri + 1) * rh
    bg = C_ALT if ri % 2 == 1 else C_WHITE
    for ci, (val, cx, cw) in enumerate(zip(row, mx, mw)):
        rbg = patches.Rectangle((cx, ry), cw, rh, linewidth=0.4,
                                  edgecolor="#CCCCCC", facecolor=bg,
                                  transform=ax_t.transAxes, clip_on=False)
        ax_t.add_patch(rbg)
        ha = "right" if ci > 0 else "left"
        tx = cx + cw - 0.01 if ci > 0 else cx + 0.01
        ax_t.text(tx, ry + rh/2, str(val), transform=ax_t.transAxes,
                  fontsize=7.5, color="#333333", ha=ha, va="center")

# Total row
total_y = hy - (len(df_m) + 1) * rh
for ci, (cx, cw) in enumerate(zip(mx, mw)):
    tbg2 = patches.Rectangle((cx, total_y), cw, rh, linewidth=0,
                               facecolor=C_TOTAL, transform=ax_t.transAxes, clip_on=False)
    ax_t.add_patch(tbg2)
totals = ["TOTAL",
          f"{s.total_revenue:,.0f}",
          f"{s.total_units:,}",
          f"{s.total_transactions:,}"]
for ci, (val, cx, cw) in enumerate(zip(totals, mx, mw)):
    ha = "right" if ci > 0 else "left"
    tx = cx + cw - 0.01 if ci > 0 else cx + 0.01
    ax_t.text(tx, total_y + rh/2, val, transform=ax_t.transAxes,
              fontsize=7.5, fontweight="bold", color=C_FG, ha=ha, va="center")

# Right: bar chart
ax_c = axes[1]
ax_c.set_facecolor("#FFFFFF")
months = s.monthly_sales["Mes"].tolist()
revenues = s.monthly_sales["Ventas_Totales"].tolist()
short_months = [m[-7:] for m in months]  # e.g. "2024-01" → last 7 chars

bars = ax_c.bar(short_months, [r / 1_000_000 for r in revenues],
                color=C_ACCENT, edgecolor="white", linewidth=0.5)
ax_c.set_title("Ventas Mensuales (CLP)", fontsize=12, fontweight="bold",
               color=C_HEADER, pad=10)
ax_c.set_xlabel("Mes", fontsize=9, color="#555555")
ax_c.set_ylabel("Millones CLP", fontsize=9, color="#555555")
ax_c.tick_params(axis="x", rotation=45, labelsize=7.5)
ax_c.tick_params(axis="y", labelsize=8)
ax_c.spines["top"].set_visible(False)
ax_c.spines["right"].set_visible(False)
ax_c.set_facecolor("#FAFAFA")
ax_c.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CCCCCC")
ax_c.set_axisbelow(True)

plt.tight_layout(pad=1.5)
out = os.path.join(OUT_DIR, "ventas_mensuales.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")

print("Done.")

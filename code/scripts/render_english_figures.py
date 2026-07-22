#!/usr/bin/env python3
"""Render English master figures for the PLOS ONE submission package.

This script rebuilds the six master PNG figures from the frozen source-data
CSV files and the Fig 5/6 textual specifications. The resulting PNG masters
can then be converted to the TIFF submission files.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from textwrap import fill

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = ROOT / "figures"
MASTERS_DIR = FIGURES_DIR / "masters"
DATA_DIR = ROOT / "data" / "derived"


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, name: str, width: float, height: float) -> None:
    MASTERS_DIR.mkdir(parents=True, exist_ok=True)
    fig.set_size_inches(width, height)
    fig.savefig(MASTERS_DIR / name, dpi=300, bbox_inches=None)
    plt.close(fig)


def add_panel_label(ax: plt.Axes, label: str, x: float = 0.0, y: float = 1.02) -> None:
    ax.text(x, y, label, transform=ax.transAxes, ha="left", va="bottom", fontsize=13, color="#4b5563")


def figure1() -> None:
    rows = read_csv(DATA_DIR / "figures" / "Fig1_source_data.csv")
    years = [int(row["year"]) for row in rows]
    contracts = [int(float(row["contracts_indexed_bd"])) for row in rows]
    values = [float(row["value_billones_cop"]) for row in rows]

    fig, axes = plt.subplots(1, 2)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.24, wspace=0.18)

    ax = axes[0]
    ax.grid(axis="y", color="#e8edf3", linewidth=0.9, zorder=0)
    ax.bar(years, contracts, color="#1f6acb", width=0.78, zorder=2)
    ax.set_ylim(0, 65000)
    ax.set_yticks([0, 20000, 40000, 60000])
    ax.set_yticklabels(["0k", "20k", "40k", "60k"])
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_title("A. Contracts per Year", loc="left", fontsize=12, color="#475569", pad=8)
    ax.legend(["Contracts"], frameon=False, loc="upper center", bbox_to_anchor=(0.50, 0.93), fontsize=11, labelcolor="#333333", handlelength=1.2)
    ax.text(0.5, -0.20, "2021 peak: COVID-19 response", transform=ax.transAxes, ha="center", va="top", color="#5b6b7a", fontsize=9.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, colors="#4b5563")

    ax = axes[1]
    ax.grid(axis="y", color="#e8edf3", linewidth=0.9, zorder=0)
    ax.bar(years, values, color="#ef6100", width=0.78, zorder=2)
    ax.set_ylim(0, 6.4)
    ax.set_yticks([0, 2, 4, 6])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{int(value)}"))
    ax.set_ylabel("COP trillions", fontsize=10.5, color="#5b6b7a")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_title("B. Contracted Value per Year (COP Trillions)", loc="left", fontsize=12, color="#475569", pad=8)
    ax.legend(["Value (COP trillions)"], frameon=False, loc="upper center", bbox_to_anchor=(0.50, 0.93), fontsize=11, labelcolor="#333333", handlelength=1.2)
    ax.text(0.5, -0.20, "2025 value peak: COP 5.50 trillion", transform=ax.transAxes, ha="center", va="top", color="#5b6b7a", fontsize=9.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, colors="#4b5563")

    save(fig, "bigloi_fig1_master.png", 9.1, 3.25)


def figure2() -> None:
    rows = read_csv(DATA_DIR / "figures" / "Fig2_source_data.csv")
    names = [row["region"] for row in rows]
    values = [float(row["value_thousand_million_cop"]) for row in rows]
    shares = [float(row["pct_total_national_value"]) for row in rows]

    fig = plt.figure()
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 0.75], left=0.14, right=0.98, top=0.83, bottom=0.07, wspace=0.14)

    ax_left = fig.add_subplot(gs[0, 0])
    display_names = ["Bogota D.C.", "Antioquia", "Valle del Cauca", "Boyaca", "Tolima", "Santander", "Huila", "Cauca", "Atlantico"]
    ax_left.barh(list(reversed(display_names)), list(reversed(values)), color="#1f6acb")
    ax_left.set_xlim(0, 10000)
    ax_left.set_xticks([0, 1000, 3000, 5000, 7000, 9000])
    ax_left.set_xticklabels(["0", "1,000", "3,000", "5,000", "7,000", "9,000"])
    ax_left.set_yticks(range(len(display_names)))
    ax_left.set_yticklabels(list(reversed(display_names)))
    ax_left.set_title("Geographic Distribution of Procurement Value", loc="left", fontsize=12, color="#475569", pad=20)
    ax_left.text(0.5, 1.01, "Value (COP billions)", transform=ax_left.transAxes, ha="center", va="bottom", fontsize=11)
    ax_left.tick_params(axis="y", length=0, labelsize=10)
    ax_left.tick_params(axis="x", length=0, colors="#4b5563")
    for spine in ax_left.spines.values():
        spine.set_visible(False)

    ax_right = fig.add_subplot(gs[0, 1])
    ax_right.set_axis_off()
    card = patches.FancyBboxPatch((0.01, 0.02), 0.98, 0.96, boxstyle="round,pad=0.02,rounding_size=0.04", linewidth=1.2, edgecolor="#d1d5db", facecolor="#f6f8fb", transform=ax_right.transAxes)
    ax_right.add_patch(card)
    ax_right.text(0.06, 0.94, "Share of Total National Value", transform=ax_right.transAxes, ha="left", va="top", fontsize=13, weight="bold", color="#1f2937")

    y = 0.83
    step = 0.09
    max_share = max(shares)
    for name, share in zip(names, shares):
        display = "Bogota D.C." if name == "Bogota D.C. combined" else name
        ax_right.text(0.06, y + 0.025, display, transform=ax_right.transAxes, ha="left", va="center", fontsize=11, color="#2f3547")
        ax_right.text(0.96, y + 0.025, f"{share:.1f}%", transform=ax_right.transAxes, ha="right", va="center", fontsize=11, color="#1f6acb", weight="bold")
        ax_right.add_patch(patches.FancyBboxPatch((0.06, y - 0.01), 0.88, 0.012, boxstyle="round,pad=0.003,rounding_size=0.008", linewidth=0, facecolor="#d6dee6", transform=ax_right.transAxes))
        ax_right.add_patch(patches.FancyBboxPatch((0.06, y - 0.01), 0.88 * (share / max_share), 0.012, boxstyle="round,pad=0.003,rounding_size=0.008", linewidth=0, facecolor="#4c86d0", transform=ax_right.transAxes))
        y -= step

    ax_right.add_line(plt.Line2D([0.06, 0.94], [0.11, 0.11], transform=ax_right.transAxes, color="#cbd5e1", linewidth=1))
    ax_right.text(0.06, 0.07, "Bogota D.C. = 56.7% of value. Top 9 regions = 83.9% of total.", transform=ax_right.transAxes, ha="left", va="top", fontsize=9.5, color="#5b6b7a", wrap=True)

    save(fig, "bigloi_fig2_master.png", 9.1, 4.04)


def figure3() -> None:
    cat_rows = read_csv(DATA_DIR / "figures" / "Fig3_category_source_data.csv")
    yearly_rows = read_csv(DATA_DIR / "figures" / "Fig3_yearly_source_data.csv")

    cats = ["Analgesics", "Diabetes", "Antivirals", "Antibiotics", "Medical supplies", "Oncology"]
    pct = [float(r["pct_with_alert"]) for r in cat_rows]
    zmax = {row["category_label"]: float(row["z_max"]) for row in cat_rows}
    ratio = {row["category_label"]: float(row["ratio_max_to_category_mean"]) for row in cat_rows}
    order_keys = ["Analgesico", "Diabetes", "Antiviral", "Antibiotico", "Insumo medico", "Oncologico"]

    years = [int(r["year"]) for r in yearly_rows]
    analyzed = [int(r["contracts_analyzed"]) for r in yearly_rows]
    alerts = [int(r["contracts_with_alert"]) for r in yearly_rows]
    rates = [float(r["alert_rate_pct"]) for r in yearly_rows]

    fig = plt.figure()
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.38], width_ratios=[1, 1], left=0.14, right=0.98, top=0.92, bottom=0.05, wspace=0.22, hspace=0.18)

    ax_l = fig.add_subplot(gs[0, 0])
    ax_l.barh(list(reversed(cats)), list(reversed(pct)), color="#ef6100")
    ax_l.set_xlim(0, 10)
    ax_l.set_xticks([0, 2, 4, 6, 8, 10])
    ax_l.set_xticklabels([f"{t}%" for t in [0, 2, 4, 6, 8, 10]])
    ax_l.set_title("A. Alerts by Category (|Z| >= 1.5 sigma)", loc="left", fontsize=12, color="#475569", pad=8)
    ax_l.legend(["% with alert"], frameon=False, loc="upper center", bbox_to_anchor=(0.54, 0.93), fontsize=11, labelcolor="#333333", handlelength=1.2)
    ax_l.tick_params(axis="y", length=0)
    ax_l.tick_params(axis="x", length=0, colors="#4b5563")
    for spine in ax_l.spines.values():
        spine.set_visible(False)

    ax_r = fig.add_subplot(gs[0, 1])
    ax_r.fill_between(years, rates, color="#ef2f2f", alpha=0.92)
    ax_r.plot(years, rates, color="#d82d2d", linewidth=3.0)
    ax_r.scatter(years, rates, s=180, facecolor="white", edgecolor="#c53030", linewidth=2.5, zorder=3)
    ax_r.set_xlim(2019.8, 2025.2)
    ax_r.set_ylim(0, 1.6)
    ax_r.set_xticks(years)
    ax_r.set_yticks([0, 0.5, 1.0, 1.5])
    ax_r.set_yticklabels(["0%", "0.5%", "1%", "1.5%"])
    ax_r.set_title("B. Annual Alert Rate", loc="left", fontsize=12, color="#475569", pad=8)
    ax_r.legend(["Alert rate (%)"], frameon=False, loc="upper center", bbox_to_anchor=(0.57, 0.93), fontsize=11, labelcolor="#333333", handlelength=1.2)
    ax_r.text(0.50, -0.16, "Increase +331% (2021 to 2025): 0.30% -> 1.31%", transform=ax_r.transAxes, ha="center", va="top", color="#d82d2d", fontsize=9.5)
    ax_r.tick_params(axis="both", length=0, colors="#4b5563")
    for spine in ax_r.spines.values():
        spine.set_visible(False)

    callout = fig.add_subplot(gs[1, :])
    callout.set_axis_off()
    box = patches.FancyBboxPatch((0.01, 0.10), 0.98, 0.80, boxstyle="round,pad=0.02,rounding_size=0.04", linewidth=1.2, edgecolor="#f7c948", facecolor="#fff8e1", transform=callout.transAxes)
    callout.add_patch(box)
    text = (
        "Key findings: Medical supplies: Z_max = 22.34 sigma (maximum value 88.7x the category mean) "
        "· Analgesics: 9.5% with alert · Oncology: Z_max = 19.27 sigma "
        "(ratio 138.5x the mean) - high intrinsic variance in high-cost biologics · "
        "295 contracts at CRITICAL level (|Z| >= 3.0 sigma)"
    )
    callout.text(0.03, 0.54, fill(text, width=92), transform=callout.transAxes, ha="left", va="center", fontsize=9.4, color="#4b5563")

    save(fig, "bigloi_fig3_master.png", 9.1, 4.5)


def figure4() -> None:
    top10 = read_csv(DATA_DIR / "figures" / "Fig4_top10_source_data.csv")
    lorenz = read_csv(DATA_DIR / "figures" / "Fig4_lorenz_source_data.csv")

    names = [r["provider_label"] for r in top10]
    shares = [float(r["pct_share_total_value"]) for r in top10]
    cum = [float(r["cumulative_pct_share"]) for r in top10]
    x = [float(r["provider_share_pct"]) for r in lorenz]
    y = [float(r["cumulative_value_pct"]) for r in lorenz]

    fig = plt.figure()
    gs = fig.add_gridspec(1, 2, width_ratios=[0.85, 1.1], left=0.07, right=0.98, top=0.92, bottom=0.25, wspace=0.28)

    ax_l = fig.add_subplot(gs[0, 0])
    ax_l.set_xscale("log")
    ax_l.plot(x, y, color="#1f6acb", linewidth=3.0)
    ax_l.fill_between(x, y, color="#4c86d0", alpha=0.08)
    ax_l.plot([0.01, 1], [0, 100], linestyle="--", color="#94a3b8", linewidth=1.5)
    ax_l.scatter([3.0], [85.8305], color="#d82d2d", s=70, zorder=3)
    ax_l.text(2.6, 76, "Top 3% = 85.8%", color="#d82d2d", fontsize=11, ha="right", va="top")
    ax_l.set_xlim(0.01, 100)
    ax_l.set_ylim(0, 100)
    ax_l.set_xticks([0.01, 0.1, 1, 10, 100])
    ax_l.set_xticklabels(["0.01%", "0.1%", "1%", "10%", "100%"])
    ax_l.set_yticks([0, 25, 50, 75, 100])
    ax_l.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax_l.set_title("Cumulative Concentration Curve", loc="left", fontsize=12, color="#475569", pad=8)
    ax_l.text(0.5, -0.18, "% of top-ranked suppliers (log scale)", transform=ax_l.transAxes, ha="center", va="top", fontsize=10.5, color="#5b6b7a")
    ax_l.set_ylabel("% cumulative contracted value", fontsize=10.5, color="#5b6b7a")
    ax_l.tick_params(axis="both", length=0, colors="#4b5563")
    for spine in ax_l.spines.values():
        spine.set_color("#334155")
        spine.set_linewidth(1.0)
    ax_l.spines["top"].set_visible(False)
    ax_l.spines["right"].set_visible(False)

    ax_r = fig.add_subplot(gs[0, 1])
    ax_r.barh(list(reversed(names)), list(reversed(shares)), color="#1f6acb")
    ax_r.set_xlim(0, 6.1)
    ax_r.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax_r.set_xticklabels([f"{t}%" for t in [0, 1, 2, 3, 4, 5, 6]])
    ax_r.set_title("Top 10 Suppliers", loc="left", fontsize=12, color="#475569", pad=8)
    ax_r.legend(["% of total value"], frameon=False, loc="lower right", bbox_to_anchor=(0.98, 0.04), fontsize=11, labelcolor="#333333", handlelength=1.2)
    ax_r.tick_params(axis="y", length=0)
    ax_r.tick_params(axis="x", length=0, colors="#4b5563")
    for spine in ax_r.spines.values():
        spine.set_visible(False)
    ax_r.text(0.5, -0.14, "50,225 active suppliers - top 3% (1,507 suppliers) = 85.8%\nHHI 120.99 · *retained human-health immunobiologics contract", transform=ax_r.transAxes, ha="center", va="top", fontsize=8.9, color="#5b6b7a", linespacing=1.35)

    save(fig, "bigloi_fig4_master.png", 9.1, 3.97)


def figure5() -> None:
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    ax.text(0.5, 0.975, "Workflow vs BigLoI Digital Prototype", ha="center", va="top", fontsize=15, color="#1f2937", weight="bold")
    ax.text(0.5, 0.938, "Left: current institutional workflow. Right: prototype digital states.", ha="center", va="top", fontsize=10.5, color="#55616f")

    left_box = patches.FancyBboxPatch((0.10, 0.19), 0.34, 0.66, boxstyle="round,pad=0.02,rounding_size=0.02", linewidth=0, facecolor="#fff6e8")
    right_box = patches.FancyBboxPatch((0.67, 0.19), 0.22, 0.66, boxstyle="round,pad=0.02,rounding_size=0.02", linewidth=0, facecolor="#eef7ea")
    ax.add_patch(left_box)
    ax.add_patch(right_box)

    ax.text(0.27, 0.88, "CURRENT INSTITUTIONAL WORKFLOW", ha="center", va="center", fontsize=13, color="#ef6100", weight="bold")
    ax.text(0.27, 0.846, "local evidence + general financial segment", ha="center", va="center", fontsize=10.5, color="#5b6b7a")
    ax.text(0.78, 0.88, "PROTOTYPE DIGITAL STATES", ha="center", va="center", fontsize=13, color="#3b8d3d", weight="bold")
    ax.text(0.78, 0.846, "~30 reference hours", ha="center", va="center", fontsize=10.5, color="#5b6b7a")

    left_steps = [
        ("Institutional need", 0.74),
        ("Order / request", 0.62),
        ("Technical receipt and registration", 0.50),
        ("Invoice filing, review, and accrual", 0.38),
        ("Treasury and final payment", 0.26),
    ]
    for label, y in left_steps:
        face = "#fff2d8" if y > 0.30 else "#ef6100"
        text_color = "#ef6100" if y > 0.30 else "white"
        rect = patches.FancyBboxPatch((0.13, y), 0.28, 0.085, boxstyle="round,pad=0.01,rounding_size=0.01", linewidth=2, edgecolor="#ef6100", facecolor=face)
        ax.add_patch(rect)
        ax.text(0.27, y + 0.042, fill(label, width=22), ha="center", va="center", fontsize=10.5, color=text_color, weight="bold")

    for y in [0.705, 0.585, 0.465, 0.345]:
        ax.annotate("", xy=(0.27, y - 0.02), xytext=(0.27, y + 0.02), arrowprops=dict(arrowstyle="-|>", color="#ef6100", lw=2.0))

    right_steps = [
        ("Contract validated", "green", 0.74),
        ("Dispatch registered\n< 24 hours", "light", 0.62),
        ("Delivery verified\n~4 hours", "light", 0.50),
        ("CRE / digital invoice\n~1 hour", "light", 0.38),
        ("Payment released\n~1 hour", "dark", 0.26),
    ]
    for label, tone, y in right_steps:
        if tone == "green":
            face = "#e9f5e8"
            edge = "#3b8d3d"
            color = "#3b8d3d"
        elif tone == "dark":
            face = "#3b8d3d"
            edge = "#3b8d3d"
            color = "white"
        else:
            face = "#e9f5e8"
            edge = "#3b8d3d"
            color = "#3b8d3d"
        rect = patches.FancyBboxPatch((0.70, y), 0.18, 0.085, boxstyle="round,pad=0.01,rounding_size=0.01", linewidth=2, edgecolor=edge, facecolor=face)
        ax.add_patch(rect)
        ax.text(0.79, y + 0.042, label, ha="center", va="center", fontsize=10.5, color=color, weight="bold")

    for y in [0.705, 0.585, 0.465, 0.345]:
        ax.annotate("", xy=(0.79, y - 0.02), xytext=(0.79, y + 0.02), arrowprops=dict(arrowstyle="-|>", color="#3b8d3d", lw=2.0))

    ax.text(0.27, 0.18, "Current aggregated cycle: median 90 days", ha="center", va="center", fontsize=10.5, color="#ef6100", weight="bold",
            bbox=dict(boxstyle="round,pad=0.5,rounding_size=0.15", fc="#fff3e3", ec="#ef6100", lw=2))
    ax.text(0.79, 0.18, "Prototype reference digital total: ~30 hours", ha="center", va="center", fontsize=10.5, color="#3b8d3d", weight="bold",
            bbox=dict(boxstyle="round,pad=0.5,rounding_size=0.15", fc="#eef7ea", ec="#3b8d3d", lw=2))
    ax.text(0.50, 0.09, "Illustrative financial scenario: COP 167-325 billion/year\n2% monthly financing cost x corrected flow of COP 2.82 trillion (mean) or COP 5.50 trillion (2025)\nx reference reduction of the digital administrative cycle from 90 days to ~30 hours", ha="center", va="center", fontsize=9.5, color="#5b6b7a",
            bbox=dict(boxstyle="round,pad=0.8,rounding_size=0.15", fc="#eaf3ff", ec="#2d71c8", lw=2))

    save(fig, "bigloi_fig5_master.png", 9.1, 5.94)


def figure6() -> None:
    rows = read_csv(DATA_DIR / "figures" / "Fig6_components.csv")

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.text(0.5, 0.965, "BigLoI Platform Architecture", ha="center", va="top", fontsize=14, color="#4b5563")
    ax.text(0.5, 0.925, "data flow: layer 1 -> layer 7", ha="center", va="top", fontsize=11, color="#4b5563")

    colors = ["#c51f1a", "#ee6100", "#398c39", "#0696a4", "#00786f", "#4f2da7", "#1f6acb"]
    english_names = {
        "Recoleccion de datos": "Data collection",
        "Almacenamiento": "Storage",
        "Procesamiento / API": "Processing / API",
        "IA generativa (RAG)": "Generative AI (RAG)",
        "Aprendizaje automatico": "Machine learning",
        "Contratos inteligentes": "Smart contracts",
        "Visualizacion": "Visualization",
    }
    y_positions = [0.72, 0.61, 0.50, 0.39, 0.28, 0.17, 0.06]
    box_h = 0.10
    for row, color, y in zip(rows, colors[::-1], y_positions):
        rect = patches.FancyBboxPatch((0.03, y), 0.94, box_h, boxstyle="round,pad=0.005,rounding_size=0.008", linewidth=0, facecolor=color)
        ax.add_patch(rect)
        title = f"{row['layer_number']}. {english_names.get(row['layer_name'], row['layer_name'])}"
        ax.text(0.05, y + box_h * 0.64, title, ha="left", va="center", fontsize=14, color="white", weight="bold")
        ax.text(0.05, y + box_h * 0.28, row["primary_technology"], ha="left", va="center", fontsize=11.5, color="white")
        ax.text(0.43, y + box_h * 0.28, row["function_or_scope"], ha="left", va="center", fontsize=10.2, color="#f8fafc")
    save(fig, "bigloi_fig6_master.png", 9.1, 4.2)


def main() -> None:
    figure1()
    figure2()
    figure3()
    figure4()
    figure5()
    figure6()
    print("Rendered English master figures:")
    for idx in range(1, 7):
        print(f"- figures/masters/bigloi_fig{idx}_master.png")


if __name__ == "__main__":
    main()

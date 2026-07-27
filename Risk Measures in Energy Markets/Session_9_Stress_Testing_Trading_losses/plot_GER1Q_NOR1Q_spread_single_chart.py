from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def create_chart(input_path: Path, sheet_name: str, output_path: Path) -> None:
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    required_columns = {"Date", "GER1Q", "NOR1Q"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Spread_GER1Q_NOR1Q"] = df["GER1Q"] - df["NOR1Q"]

    fig, ax = plt.subplots(figsize=(13, 6.5))

    ax.plot(df["Date"], df["GER1Q"], label="GER1Q", linewidth=1.8, color="#1f77b4")
    ax.plot(df["Date"], df["NOR1Q"], label="NOR1Q", linewidth=1.8, color="#ff7f0e")
    ax.plot(
        df["Date"],
        df["Spread_GER1Q_NOR1Q"],
        label="Spread GER1Q - NOR1Q",
        linewidth=1.8,
        color="#2ca02c",
    )

    ax.set_title("GER1Q, NOR1Q and Spread", fontsize=14, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Settlement Price (EUR/MWh)")

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate(rotation=45, ha="right")

    ax.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.4)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a single chart for GER1Q, NOR1Q, and their spread."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("Session_9_Data_completed.xlsx"),
        help="Path to the Excel workbook.",
    )
    parser.add_argument(
        "--sheet",
        default="Data",
        help="Worksheet name containing the time series.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output image path. Defaults to the workbook directory.",
    )
    args = parser.parse_args()

    output_path = args.output or args.input.with_name("GER1Q_NOR1Q_spread_single_chart.png")
    create_chart(args.input, args.sheet, output_path)
    print(f"Saved chart to: {output_path}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


SERIES_COLUMNS = ["GER1M", "GER1Q", "NOR1M", "NOR1Q"]


def create_timeseries_plot(input_path: Path, sheet_name: str, output_path: Path) -> None:
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    required_columns = {"Date", *SERIES_COLUMNS}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    colors = {
        "GER1M": "#1f77b4",
        "GER1Q": "#ff7f0e",
        "NOR1M": "#2ca02c",
        "NOR1Q": "#d62728",
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    for column in SERIES_COLUMNS:
        ax.plot(df["Date"], df[column], linewidth=1.8, label=column, color=colors[column])

    ax.set_title("Furtue Front price EUR Mwh", fontsize=14, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Settlement Price")

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate(rotation=45, ha="right")

    ax.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.4)
    ax.legend(frameon=False, ncol=2, loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a multi-series EEX time series chart from an Excel workbook."
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

    output_path = args.output or args.input.with_name("EEX_Future_Front_Price_timeseries.png")
    create_timeseries_plot(args.input, args.sheet, output_path)
    print(f"Saved chart to: {output_path}")


if __name__ == "__main__":
    main()

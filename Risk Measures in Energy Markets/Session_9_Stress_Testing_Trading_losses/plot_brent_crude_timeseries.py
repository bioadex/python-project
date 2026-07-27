from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def create_timeseries_plot(input_path: Path, sheet_name: str, output_path: Path) -> None:
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    required_columns = {"Date", "Brent Crude Oil 1M"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["Date"], df["Brent Crude Oil 1M"], linewidth=1.8, color="#1f77b4")

    ax.set_title("Brent Crude Oil 1M", fontsize=14, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Settlement Price")

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate(rotation=45, ha="right")

    ax.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Brent Crude Oil 1M time series chart from an Excel workbook."
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
        default=Path("Brent_Crude_Oil_1M_timeseries.png"),
        help="Path for the saved chart image.",
    )
    args = parser.parse_args()

    create_timeseries_plot(args.input, args.sheet, args.output)
    print(f"Saved chart to: {args.output}")


if __name__ == "__main__":
    main()

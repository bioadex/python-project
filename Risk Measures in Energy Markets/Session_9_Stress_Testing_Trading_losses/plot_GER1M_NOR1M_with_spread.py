from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    stats = df[["GER1M", "NOR1M", "Difference_GER1M_NOR1M"]].describe().T
    stats.index.name = "Series"
    return stats


def create_chart(input_path: Path, sheet_name: str, output_path: Path) -> pd.DataFrame:
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    required_columns = {"Date", "GER1M", "NOR1M"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Difference_GER1M_NOR1M"] = df["GER1M"] - df["NOR1M"]

    stats = calculate_statistics(df)

    fig, (ax_main, ax_spread) = plt.subplots(
        2,
        1,
        figsize=(13, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )

    ax_main.plot(df["Date"], df["GER1M"], label="GER1M", linewidth=1.8, color="#1f77b4")
    ax_main.plot(df["Date"], df["NOR1M"], label="NOR1M", linewidth=1.8, color="#ff7f0e")
    ax_main.set_ylabel("Settlement Price (EUR/MWh)")
    ax_main.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.4)
    ax_main.legend(frameon=False, loc="upper left")

    ax_spread.plot(
        df["Date"],
        df["Difference_GER1M_NOR1M"],
        label="difference GER1M and NOR1M",
        linewidth=1.8,
        color="#2ca02c",
    )
    ax_spread.axhline(0, color="black", linewidth=0.8, linestyle=":")
    ax_spread.set_xlabel("Date")
    ax_spread.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.4)
    ax_spread.legend(frameon=False, loc="upper left")

    ax_spread.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax_spread.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate(rotation=45, ha="right")

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a two-panel chart for GER1M and NOR1M plus their difference."
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
    parser.add_argument(
        "--stats-output",
        type=Path,
        default=None,
        help="Optional CSV output path for the descriptive statistics.",
    )
    args = parser.parse_args()

    output_path = args.output or args.input.with_name("GER1M_NOR1M_timeseries_spread.png")
    stats_output = args.stats_output or args.input.with_name("GER1M_NOR1M_statistics.csv")

    stats = create_chart(args.input, args.sheet, output_path)
    stats.to_csv(stats_output)

    print(f"Saved chart to: {output_path}")
    print(f"Saved statistics to: {stats_output}")
    print(stats.to_string())


if __name__ == "__main__":
    main()

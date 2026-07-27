from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_completed_sheet(input_path: Path, sheet_name: str = "Data") -> tuple[pd.DataFrame, list[str]]:
    df = pd.read_excel(input_path, sheet_name=sheet_name)

    if "Date" not in df.columns:
        raise ValueError("The workbook does not contain a 'Date' column.")

    df["Date"] = pd.to_datetime(df["Date"]).dt.normalize()
    df = df.sort_values("Date").reset_index(drop=True)

    expected_dates = pd.bdate_range(df["Date"].min(), df["Date"].max())
    existing_dates = pd.DatetimeIndex(df["Date"])
    missing_dates = expected_dates.difference(existing_dates)

    completed_dates = existing_dates.union(missing_dates).sort_values()
    completed = (
        df.set_index("Date")
        .reindex(completed_dates)
        .rename_axis("Date")
        .reset_index()
    )

    inserted_dates = [d.strftime("%Y-%m-%d") for d in missing_dates]
    return completed, inserted_dates


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Insert missing business dates into the Date column of the Data sheet."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("Session_9_Data.xlsx"),
        help="Path to the source workbook.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Session_9_Data_completed.xlsx"),
        help="Path for the completed workbook.",
    )
    parser.add_argument(
        "--sheet",
        default="Data",
        help="Worksheet name containing the Date column.",
    )
    args = parser.parse_args()

    completed, inserted_dates = build_completed_sheet(args.input, args.sheet)

    with pd.ExcelWriter(
        args.output,
        engine="openpyxl",
        date_format="yyyy-mm-dd",
        datetime_format="yyyy-mm-dd",
    ) as writer:
        completed.to_excel(writer, sheet_name=args.sheet, index=False)

    print(f"Saved: {args.output}")
    print(f"Inserted {len(inserted_dates)} missing business dates.")
    if inserted_dates:
        print("Missing dates:")
        for date in inserted_dates:
            print(date)


if __name__ == "__main__":
    main()

import pandas as pd
from datetime import timedelta

def convert_timeseries_format(input_file, output_file):
    # Read the CSV file with semicolon as separator
    df = pd.read_csv(input_file, sep=';', header=None, names=['Datetime', 'Value'])

    # Convert the datetime format and handle 24:00:00 if it exists
    def handle_datetime_conversion(dt):
        try:
            dt = pd.to_datetime(dt)
        except ValueError:
            # If time is "24:00:00", shift to "00:00:00" of the next day
            if "24:00:00" in dt:
                dt = pd.to_datetime(dt.replace("24:00:00", "00:00:00")) + timedelta(days=1)
        return dt.strftime('%d.%m.%Y %H:%M:%S')

    df['Datetime'] = df['Datetime'].apply(handle_datetime_conversion)

    # Write the modified dataframe to a new CSV file
    df.to_csv(output_file, sep=';', index=False, header=False)

if __name__ == "__main__":
    input_file = 'HISTORY_WIND.csv'  # Change this to your input CSV file name
    output_file = 'NEW_HISTORY_WIND.csv'  # Change this to your desired output CSV file name

    convert_timeseries_format(input_file, output_file)
    print(f"Conversion complete. Output saved to {output_file}.")

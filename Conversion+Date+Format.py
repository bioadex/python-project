import pandas as pd


def convert_timeseries_format(input_file, output_file):
    # Read the CSV file with semicolon as separator
    df = pd.read_csv('Price-it-Solar-forecast.csv', sep=';', header=None, names=['Datetime', 'Value'])

    # Convert the datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Datetime'] = df['Datetime'].dt.strftime('%d.%m.%Y %H:%M:%S')

    # Write the modified dataframe to a new CSV file
    df.to_csv(output_file, sep=';', index=False, header=False)


if __name__ == "__main__":
    input_file = 'Price-it-Solar-forecast.csv'  # Change this to your input CSV file name
    output_file = 'new_price-it_de_Solar_Forecast.csv'  # Change this to your desired output CSV file name

    convert_timeseries_format(input_file, output_file)
    print(f"Conversion complete. Output saved to {output_file}.")

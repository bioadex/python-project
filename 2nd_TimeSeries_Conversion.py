import pandas as pd

def convert_timeseries_format(input_file, output_file):
    # Read the CSV file with semicolon as separator
    df = pd.read_csv(input_file, sep=';', header=None, names=['Datetime', 'Value'])

    # Convert the datetime format from DD.MM.YYYY HH:MM to YYYY-MM-DD HH:MM
    df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d.%m.%Y %H:%M')

    # Write the modified dataframe to a new CSV file with the updated format
    df.to_csv(output_file, sep=';', index=False, header=False, date_format='%Y-%m-%d %H:%M')


if __name__ == "__main__":
    input_file = '20241010_HPFC_DYN_S1_Model_Id001002_S1_XC_GREEN_v001.001.000_2024-09-10.csv'  # Change this to your input CSV file name
    output_file = '20241010_HPFC_DYN_S1_Model_Id001002_S1_XC_GREEN_v001.001.000_2024-09-10.csv'  # Change this to your desired output CSV file name

    convert_timeseries_format(input_file, output_file)
    print(f"Conversion complete. Output saved to {output_file}.")
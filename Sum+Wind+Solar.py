import pandas as pd

# Load the Solar and Wind data from CSV files
solar_file = 'eq_data_2024-12-10_1025_Solar_DE.csv'
wind_file = 'eq_data_2024-12-10_1022_Wind_DE.csv'

# Assuming the files are in the format: "DateTime;Value"
solar_df = pd.read_csv(solar_file, sep=';', names=['DateTime', 'Solar_Value'], parse_dates=['DateTime'])
wind_df = pd.read_csv(wind_file, sep=';', names=['DateTime', 'Wind_Value'], parse_dates=['DateTime'])

# Merge the dataframes on DateTime
merged_df = pd.merge(solar_df, wind_df, on='DateTime')

# Add a new column for the summed values
merged_df['New_Value'] = merged_df['Solar_Value'] + merged_df['Wind_Value']

# Create a simplified dataframe with only DateTime and New_Value
final_df = merged_df[['DateTime', 'New_Value']]

# Save the result to a new CSV
output_file = 'sum+wind+solar.csv'
final_df.to_csv(output_file, index=False, sep=';')

print(f"Summed time series saved to {output_file}")

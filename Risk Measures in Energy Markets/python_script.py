import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Explicitly create copies to avoid SettingWithCopyWarning and ensure independent dataframes
historical_price_data = historical_price_data.copy()
historical_price_q1_data = historical_price_q1_data.copy()

# Convert 'Date' column in historical_price_data to datetime
historical_price_data['Date'] = pd.to_datetime(historical_price_data['Date'])

# Process historical_price_q1_data: handle potential renaming of 'Date.1' to 'Date'
if 'Date.1' in historical_price_q1_data.columns:
    historical_price_q1_data['Date.1'] = pd.to_datetime(historical_price_q1_data['Date.1'])
    # Rename 'Date.1' to 'Date' for merging
    historical_price_q1_data = historical_price_q1_data.rename(columns={'Date.1': 'Date'})
elif 'Date' in historical_price_q1_data.columns:
    # If 'Date.1' was already renamed to 'Date' in a previous run, ensure 'Date' is datetime
    historical_price_q1_data['Date'] = pd.to_datetime(historical_price_q1_data['Date'])
else:
    # Fallback/Error case: neither 'Date.1' nor 'Date' found.
    print("Error: Neither 'Date.1' nor 'Date' column found in historical_price_q1_data. Cannot plot.")
    # You might want to raise an error or handle this case more specifically

# Merge the two DataFrames on the 'Date' column
# We are merging on the 'Date' column which is now consistently named 'Date' in both dataframes
merged_data = pd.merge(historical_price_data[['Date', 'Settlement']],
                       historical_price_q1_data[['Date', 'Settlement.1']],
                       on='Date', how='outer')

# Sort the data by date to ensure correct line plotting
merged_data = merged_data.sort_values(by='Date')

# Plotting the data
plt.figure(figsize=(14, 7))
sns.lineplot(x='Date', y='Settlement', data=merged_data, label='EEX DEB M0 Settlement')
sns.lineplot(x='Date', y='Settlement.1', data=merged_data, label='EEX DEB Q1 Settlement')

plt.title('EEX DEB M0 vs EEX DEB Q1 Settlement Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Settlement Price')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
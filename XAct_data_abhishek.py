
from xact_header import headers, element_names
import matplotlib.pyplot as plt
import pandas as pd
import os

path = os.getcwd()

daterange = '7_20_2023_8_31_2023'
start_date = pd.to_datetime('2023-07-20 00:00:00')  # Specify your start date
end_date = pd.to_datetime('2023-08-31 23:00:00')  # Specify your end date


# Load data - the element concentrations and uncertainties are in ng/m3
elements = pd.read_csv(path + '/Xact_data/XAct_summary_7_20_2023__8_31_2023.txt', delimiter=',', skiprows=2, names=headers, index_col=False)

# We have 'TIME' and 'PUMP START TIME' columns. Let's remove the 'PUMP START TIME' column to avoid duplicacy.
elements = elements.drop(columns=['PUMP START TIME'])

# Replace timestamps "00:30:00" with "00:00:00" in the 'TIME' column
'''Energy calibration - 00:00:00-00:15:00
   QA upscale - '00:15:00-00:30:00
   So, data points labelled 00:30:00 measures 00:30:00 to 01:00:00 and I am assuming it to represent 00:00:00-01:00:00 hour.'''

elements['TIME'] = elements['TIME'].str.replace('00:30:00', '00:00:00')

# Convert 'TIME' column to datetime objects
elements['TIME'] = pd.to_datetime(elements['TIME'])

# Remove rows where the timestamp is  "00:15:00"
elements = elements[~(elements['TIME'].dt.strftime('%H:%M:%S') == '00:15:00')]

# Rename the 'TIME' column to 'datetime'
elements = elements.rename(columns={'TIME': 'datetime'})


# Filter the data based on the specified start and end dates
filtered_elements = elements[(elements['datetime'] >= start_date) & (elements['datetime'] <= end_date)]

# Save the filtered data to a CSV file
filtered_elements.to_csv('Xact_data/XAct_data_' + daterange + '.csv', index=False)

# Plot an element
element = 'S 16 (ng/m3)'
plt.figure(figsize=(10, 6))  # Adjust the figure size
plt.scatter(filtered_elements['datetime'], filtered_elements[element], marker='o', linestyle='-', color='b', label=element)
plt.xlabel('DateTime')
plt.ylabel(f'{element} Concentration')
plt.title(f'{element} Concentration Over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.xticks(rotation=30)
plt.show()
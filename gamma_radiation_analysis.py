# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from google.colab import files

# Step 1: Upload the spreadsheets
uploaded_files = files.upload()  # Upload Excel files

# Step 2: Read and process the spreadsheets
dataframes = {}
colors = {}  # Dictionary to store colors for each spreadsheet

for file_name in uploaded_files.keys():
    try:
        # Prompt the user for a description or name for each spreadsheet
        spreadsheet_name = input(f"Please enter a name for the spreadsheet {file_name}: ")
        
        # Prompt the user for a color for the spreadsheet
        color = input(f"Please enter a color for {spreadsheet_name}: ")
        
        # Read the Excel file directly
        df = pd.read_excel(file_name, decimal=".")
        
        # Convert all data to numeric, coercing errors to NaN
        df = df.apply(pd.to_numeric, errors='coerce')
        
        # Trim all columns to 301 values (first 301 rows)
        df = df.iloc[:301, :]
        
        # Add to the dictionary of dataframes with the user-provided name
        dataframes[spreadsheet_name] = df
        colors[spreadsheet_name] = color  # Store the color for this spreadsheet
    except Exception as e:
        print(f"Error reading {file_name}: {e}")

# Step 3: Plot all spreadsheets on the same axes
plt.figure(figsize=(12, 8))  # Create a new figure for the combined plot

# Loop through each spreadsheet and plot its data
for spreadsheet_name, df in dataframes.items():
    # Define x-axis as 301 time points per column, total length = 301 * number_of_columns
    x = range(1, 301 * df.shape[1] + 1)  # x-axis: time points
    
    # Initialize an empty list to store the step function y-values
    y_values = []

    # Loop through all columns (representing data at different voltage steps)
    for column_index in range(df.shape[1]):
        # Compute the average value for each column (voltage step)
        avg_value = df.iloc[:, column_index].mean()
        
        # Append the average value for this column to the y-values list
        y_values.extend([avg_value] * 301)  # Each step lasts for 301 time points

    # Plot the step function (increasing y-values) with the specified color on the same axes
    plt.step(x, y_values, label=spreadsheet_name, where='post', color=colors[spreadsheet_name])

# Customize the plot
plt.xlabel('Time (s)')
plt.ylabel('Current (mA)')
plt.title('Current Measured from a CNS Irradiated by Different Doses of Gamma Radiation')
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
plt.grid()
plt.tight_layout()  # Adjust layout for better visibility
plt.show()

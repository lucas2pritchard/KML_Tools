import csv
import pandas as pd
import numpy as np

def process_ascii_files(file1, file2, output_csv1, output_csv2, final_csv):
    # Step 1: Extract values from the first ASCII file
    with open(file1, 'r') as f1:
        reader = csv.reader(f1)
        data1 = []
        for row in reader:
            if len(row) > 15:  # Ensure the row has enough values
                data1.append({
                    "Time": row[6],  # 7th value
                    "Lat (deg)": row[11],  # 13th value
                    "Lon (deg)": row[12],  # 14th value
                    "Altitude (m)": row[13],  # 15th value
                })

    # Write the extracted data to the first CSV
    with open(output_csv1, 'w', newline='') as csvfile:
        fieldnames = ["Time", "Lat (deg)", "Lon (deg)", "Altitude (m)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data1)

    # Step 2: Extract values from the second ASCII file
    with open(file2, 'r') as f2:
        reader = csv.reader(f2)
        data2 = []
        for row in reader:
            if len(row) > 13:  # Ensure the row has enough values
                data2.append({
                    "Time": float(row[6]),  # 7th value
                    "Yaw (deg)": float(row[12]),  # 13th value
                })

    # Extend the time column to half-second intervals and extrapolate Yaw values
    extended_data2 = []
    for i in range(len(data2) - 1):
        current_time = data2[i]["Time"]
        next_time = data2[i + 1]["Time"]
        current_yaw = data2[i]["Yaw (deg)"]
        next_yaw = data2[i + 1]["Yaw (deg)"]

        # Add the current row
        extended_data2.append({"Time": current_time, "Yaw (deg)": current_yaw})

        # Add interpolated rows for half-second intervals
        while current_time + 0.5 < next_time:
            current_time += 0.5
            interpolated_yaw = current_yaw + (next_yaw - current_yaw) * 0.5 / (next_time - data2[i]["Time"])
            extended_data2.append({"Time": current_time, "Yaw (deg)": interpolated_yaw})

    # Add the last row
    extended_data2.append(data2[-1])

    # Write the extended data to the second CSV
    with open(output_csv2, 'w', newline='') as csvfile:
        fieldnames = ["Time", "Yaw (deg)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(extended_data2)

    # Step 3: Merge the two CSVs by matching the "Time" column
    df1 = pd.read_csv(output_csv1)
    df2 = pd.read_csv(output_csv2)

    merged_df = pd.merge(df1, df2, on="Time", how="inner")

    # Step 4: Insert a row with "Localization Subsystem" above the column names
    header_row = ["Localization Subsystem"] * len(merged_df.columns)
    merged_df.loc[-1] = header_row  # Add new row at the top
    merged_df.index = merged_df.index + 1  # Shift index
    merged_df = merged_df.sort_index()  # Sort by index

    # Step 5: Write the final merged CSV
    merged_df.to_csv(final_csv, index=False)

# Example usage
file1 = "NMUT24080027D_2025-06-28_04-42-38_PPPPOS.ASCII"  # Replace with the path to your first ASCII file
file2 = "NMUT24080027D_2025-06-28_04-42-38_HEADING2.ASCII"  # Replace with the path to your second ASCII file
output_csv1 = "output1.csv"  # Path for the first intermediate CSV
output_csv2 = "output2.csv"  # Path for the second intermediate CSV
final_csv = "final_output.csv"  # Path for the final merged CSV

process_ascii_files(file1, file2, output_csv1, output_csv2, final_csv)
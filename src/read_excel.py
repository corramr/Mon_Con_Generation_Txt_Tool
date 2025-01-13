import pandas as pd
import os


def read_excel_file(file_path, sheet, fields):

    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet)

    # Filter specific messages
    # (filtering rows)
    filtered_df = df[
        (df["Signal name"] == "VUx Status Data")
        | (df["Signal name"] == "VUx Mode")
        | (df["Signal name"] == "VUx SATURN Status")
        | (df["Signal name"] == "VUx SATURN Parameters")
        | (df["Signal name"] == "VUx IBIT/PBIT Status")
    ]

    # Select only the specified fields
    # it's like filtering the columns you want to read from the excel file
    # (filtering columns)
    selected_df = filtered_df[fields]

    # Convert the filtered and selected DataFrame to a string
    df_string = selected_df.to_string(index=False)

    # create filtered_data folder if not present
    output_folder = "output/filtered_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the filtered DataFrame to a text file
    with open("./output/filtered_data/filtered_data.txt", "w", encoding="utf-8") as file:
        file.write(df_string)

    return selected_df

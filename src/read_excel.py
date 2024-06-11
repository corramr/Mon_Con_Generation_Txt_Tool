import pandas as pd


def read_excel_file(file_path, sheet, fields):

    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet)

    # Filter specific messages (filtering rows)
    filtered_df = df[
        (df["Signal name"] == "VUx Status Data")
        | (df["Signal name"] == "VUx Mode")
        | (df["Signal name"] == "VUx SATURN Status")
        | (df["Signal name"] == "VUx SATURN Parameters")
        | (df["Signal name"] == "VUx IBIT/PBIT Status")
    ]

    # Select only the specified fields (filtering columns)
    selected_df = filtered_df[fields]

    # Convert the filtered and selected DataFrame to a string
    df_string = selected_df.to_string(index=False)

    # Save the filtered DataFrame to a text file
    with open("filtered_todos.txt", "w", encoding="utf-8") as file:
        file.write(df_string)

    return selected_df

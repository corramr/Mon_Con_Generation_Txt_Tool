from src.read_excel import read_excel_file
from src.process_data import process_data
from src.generate_code import generate_code
import os
import json

# entry point
def main():

    # Specify the relative file path
    file_path = os.path.join("sample_files", "C27J-FBS_SRD_Data_Dictionary.xlsm")

    # Specify sheet of excel file
    sheet = "IRS"

    # Define fields to be processed by reading a json file
    with open("./config/config.json", "r") as config_file:
        config = json.load(config_file)
    selected_fields = config["selected_fields"]

    # Read the Excel file, filter rows, and select specific fields
    filtered_data = read_excel_file(file_path, sheet, selected_fields)
    processed_data = process_data(filtered_data)
    generate_code(processed_data)


# define entry point
if __name__ == "__main__":
    main()

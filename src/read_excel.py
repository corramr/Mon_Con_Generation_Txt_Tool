import openpyxl

#def read_excel_file(filename):

#    raw_data = []
    
#    return raw_data

def parse_excel_table(file_path, sheet_name,start_cell, end_cell):
    data_list = []

    # Load the Excel file
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]

    # Get the range of cells between start_cell and end_cell
    start_cell_name = start_cell[0] + str(start_cell[1])
    end_cell_name = end_cell[0] + str(end_cell[1])
    table_range = sheet[start_cell_name:end_cell_name]

    # Iterate through each row in the table
    for row in table_range:
        data = {
            "Device_Name": row[2].value,
            "Signal_Name": row[3].value,
            "Src": row[4].value,
            "Dst": row[5].value,
            "IRS_Name": row[7].value,
            "Type": row[13].value,
            "Map": parse_map(row[15].value) if row[15].value else None,
            "Word_S": row[9].value,
            "Word_E": row[10].value,
            "Msb": row[11].value,
            "Lsb": row[12].value,
            "Min": row[13].value,
            "Max": row[14].value,
            "Weight": row[15].value
        }
        data_list.append(data)

    return data_list

def parse_map(map_str):
    map_list = []
    lines = map_str.split(",\n")
    for line in lines:
        line = line.strip()
        print(line)
        dec_code, name = values = line.split(" ",1)
        map_list.append({"Dec_Code": dec_code, "Name": name})
    return map_list

# Example usage
file_path = "C:\\Users\\fabate\\Downloads\\C27J-FBS_SRD_Data_Dictionary.xlsm"  # Update with your Excel file path
sheet_name = "IRS"
start_cell = ("A", 2)    # Update with start cell coordinates
end_cell = ("P", 10)    # Update with end cell coordinates

parsed_data = parse_excel_table(file_path, sheet_name,start_cell, end_cell)
for data in parsed_data:
    print(data)




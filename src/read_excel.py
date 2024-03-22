import openpyxl
import tkinter as tk
from tkinter import filedialog, messagebox

def parse_excel_table(file_path, sheet_name, start_cell, end_cell):
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
            "Weight": row[15].value,
            "Generate_Code": True
        }
        data_list.append(data)

    return data_list

def parse_map(map_str):
    map_list = []
    lines = map_str.split(",\n")
    for line in lines:
        line = line.strip()
        if line:
            try:
                dec_code, name = line.split(" ", 1)
                map_list.append({"Dec_Code": dec_code, "Name": name})
            except ValueError:
                # Handle the case when there are not enough values to unpack
                pass
    return map_list

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def run_parse():
    file_path = file_entry.get()
    sheet_name = sheet_entry.get()
    start_cell = start_entry.get()
    end_cell = end_entry.get()

    if not all([file_path, sheet_name, start_cell, end_cell]):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not (start_cell[0].isalpha() and start_cell[1:].isdigit() and end_cell[0].isalpha() and end_cell[1:].isdigit()):
        messagebox.showerror("Error", "Invalid cell coordinates.")
        return
    
    start_row = int(start_cell[1:])
    end_row = int(end_cell[1:])

    # Check if start cell is before end cell
    if start_row >= end_row:
        messagebox.showerror("Error", "Start cell must be before end cell.")
        return

    start_cell = (start_cell[0], int(start_cell[1:]))
    end_cell = (end_cell[0], int(end_cell[1:]))

    start_col = start_cell[0]
    end_col = end_cell[0]

    # Check if end cell column is before column "P"
    if end_col < "P":
        messagebox.showerror("Error", "End cell column cannot be before column 'P'.")
        return

    try:
        wb = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return

    sheet = wb[sheet_name]

    # Check for empty lines between start and end rows
    for row_num in range(start_row + 1, end_row):
        if all(cell.value is None for cell in sheet[row_num]):
            messagebox.showerror("Error", "Empty line found between the provided cells.")
            return

    parsed_data = parse_excel_table(file_path, sheet_name, start_cell, end_cell)
    for data in parsed_data:
        print(data)

# Create the main window
root = tk.Tk()
root.title("Excel Parser")

# File path entry
file_label = tk.Label(root, text="File Path:")
file_label.grid(row=0, column=0, sticky="e")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, columnspan=2)
file_button = tk.Button(root, text="Browse", command=lambda: browse_file(file_entry))
file_button.grid(row=0, column=3)

# Sheet name entry
sheet_label = tk.Label(root, text="Sheet Name:")
sheet_label.grid(row=1, column=0, sticky="e")
sheet_entry = tk.Entry(root)
sheet_entry.grid(row=1, column=1)

# Start cell entry
start_label = tk.Label(root, text="Start Cell:")
start_label.grid(row=2, column=0, sticky="e")
start_entry = tk.Entry(root)
start_entry.grid(row=2, column=1)

# End cell entry
end_label = tk.Label(root, text="End Cell:")
end_label.grid(row=3, column=0, sticky="e")
end_entry = tk.Entry(root)
end_entry.grid(row=3, column=1)

# Run button
run_button = tk.Button(root, text="Run", command=run_parse)
run_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start the GUI main loop
root.mainloop()

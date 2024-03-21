from src.read_excel import read_excel_file
from src.process_data import process_data
from src.generate_code import generate_code

def main():
    raw_data = read_excel_file('data/input.xlsx')
    processed_data = process_data(raw_data)
    generate_code(processed_data)

if __name__ == '__main__':
    main()

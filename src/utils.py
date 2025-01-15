#Misc functions

# filters out blank spaces at beginning and end and enables Pascal case 
def clean_string(text):
    result = text.replace("/", "_").replace("-", "_").replace(" ", "_")
    result = '_'.join(result.capitalize() for result in result.split('_')).strip()
    return result


# for each field in TextChunk iterate, and if value exists write each item in filename
def write_fields_to_file(object,file_name):
    for field, value in vars(object).items():        
        if value:          
            if  isinstance(value , dict):
                for key, element in value.items():
                    for a in element:
                        file_name.write(a)
            elif isinstance(value, list):
                for item in value:
                    file_name.write(item)      

def update_traceability(text_chunks,count,message):


    string_start = "-- @MODIF " + str(text_chunks.scr_num)+"\n"
    string_end = "-- /@MODIF " + str(int(message.scr_num))+"\n"

    for attr_name, value in text_chunks.__dict__.items():
        # Skip non-list fields (e.g., scr_num), TODO for dictionaries
        if isinstance(value, list):
            # Ensure 'count' is within valid range
            if 0 <= count <= len(value):
                value.insert(count, string_start)
                value.insert(count, string_end)
            else:
                print(f"Index {count} is out of bounds for field '{attr_name}'.")
    text_chunks.scr_num = int(message.scr_num)

#Misc types


# define dictionary for Mon data format
di2_mon_data_format_dict = {
    "Scaled_Float": "Dig6_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Scaled_Float_15": "Dig15_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Dec_Float_32": "Dec_Float_32 => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Dec_Float_64": "Dec_Float_64 => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Scaled_Int": """
Scaled_Int_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address,
Scaled_Int_Size => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Size)
""",
    "Straight_Int": """
Straight_Int_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address,
Straight_Int_Size => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Size)
""",
    "Lookup_Straight_1_Bit": "Lu_S_1_Bit_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Lookup_Straight_3_Bit": "Lu_S_2_Bit_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Lookup_Straight_2_Bit": "Lu_S_3_Bit_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Lookup_Straight_4_Bit": "Lu_S_4_Bit_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Lookup_Straight_6_Bit": "Lu_S_6_Bit_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    "Lookup_Straight_9_Bit": "Lu_S_9_Bit_Ptr => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Value'Address",
    # "Simple_String" : ""
}

# define dict for Mon Validity Kind
di2_mon_validity_kind_dict: {
    "Trustable": [
        "(Mon_Validity_Kind => Conversion_Types.Non_Trustable,",
        "Non_Trust_Ptr     => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Valid'Address);",
    ],  # type: ignore
    "Non_Trustable": [
        "(Mon_Validity_Kind => Conversion_Types.Non_Trustable,",
        "Non_Trust_Ptr     => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Valid'Address);",
    ],  # type: ignore
    "None": ["(Mon_Validity_Kind => Conversion_Types.Non_Trustable);"],  # type: ignore
}  # type: ignore

import os
from src import utils



# define dictionary for Mon data format
mon_data_format_dict = {
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


# generate content for file "di.1.txt"
def generate_di_1_code(file, device, device_data_dict):

    # define text chunks class present "di.1.ada"

    # create instance
    class Text_Chunk(): 
        def __init__(self):
    # Initializing each field as an empty list
            self.monTypes = ["Mon Types\n","\n\n\n"]
            self.monGetProcedures = ["Mon Get procedures \n","\n\n\n"]
            self.monArrayOf = ["Mon array of \n","\n\n\n"]
            self.monSideType = ["Mon Side type\n","\n\n\n"]

    text_chunks = Text_Chunk()

    # loop over signals within device ("VUx Mode", "VUx Status data", ...)
    for signal in device_data_dict["IN"].keys():
        # loop over input messages within signal
        # each signal is made of several messages which are located in specific words
        # for example, the signal VUx Mode contains:  (Aj_Select, Aj_Master, Time_Mode, ...)
        for message in device_data_dict["IN"][signal]:
           
            # clean up variables without impacting raw data
            cleaned_variable_name = utils.clean_string(message.variable_name) 
            cleaned_device = utils.clean_string(device)
            
            # store mon types
            chunk = f"""type {cleaned_device}_{cleaned_variable_name}_Mon_Type   is limited private\n"""

            text_chunks.monTypes.insert(1,chunk +"\n\n")

            # store mon procedures
            chunk = f"""procedure Get_{cleaned_variable_name}  
   (Dev_Index : in  Fmsb_Config_Types.{message.index_name}; 
   Mon       : in  {cleaned_device}_{cleaned_variable_name}_Mon_Type;
   Value     : out {cleaned_device}_Types.{cleaned_variable_name}_Type;
   Valid     : out Boolean);"""

            text_chunks.monGetProcedures.insert(1, chunk + "\n\n")

            # store definition of MonArrayOf 
            chunk = f"""type {cleaned_device}_{cleaned_variable_name}_Mon_Type is
   array (Fmsb_Config_Types.{message.index_name}) of {cleaned_device}_{cleaned_variable_name}_Mon_Side_Type;
            """

            text_chunks.monArrayOf.insert(1,chunk + "\n\n")

            # store side types
            chunk = f"""type {cleaned_device}_{cleaned_variable_name}_Mon_Side_Type is
   record
      Value: ***PLACEHOLDER***;
      Valid: Boolean;
   end record;
            """

            text_chunks.monSideType.insert(1,chunk + "\n\n")

    ####################################################################

    # write mon types
    utils.write_fields_to_file(text_chunks,file)


    '''
    if len(text_chunks.monTypes) > 0:
        # add heading comments
        text_chunks.monTypes.insert(0, "-- Mon types\n")
        # add some new empty lines at the end of mon types as separators
        text_chunks.monTypes.append("\n\n\n")
        # write
        for mon_chunk in text_chunks.monTypes:
            file.write(mon_chunk)

    # write mon procedures
    if len(text_chunks.monGetProcedures) > 0:
        # add heading comments
        text_chunks.monGetProcedures.insert(0, "-- Get mon procedures\n")
        # write
        for mon_chunk in text_chunks.monGetProcedures:
            file.write(mon_chunk)

    # write arrayof types
    if len(text_chunks.monArrayOf) > 0:
        # add heading comments
        text_chunks.monArrayOf.insert(0, "-- Mon array of type\n")
        # add some new empty lines at the end of mon types as separators
        text_chunks.monArrayOf.append("\n\n\n")
        # write
        for mon_chunk in text_chunks.monArrayOf:
            file.write(mon_chunk)
            '''


# generate content for file "di.2.txt"
def generate_di_2_code(file, device, device_data_dict):

    # define text chunks class present "di.2.ada"
    class TextChunks:
        def __init__(self):
            # Initializing each field as an empty list
            self.tableDeclaration = {"in": [], "out": []}
            self.messageDeclaration = {"in": [], "out": []}
            self.tableAssignment = {"in": [], "out": []}
            self.messageAssignment = {"in": [], "out": []}
            self.monGetProcedures = []

    # create instance
    text_chunks = TextChunks()

    # # loop over signals within device
    for in_out in device_data_dict.keys():
        # input case
        if in_out == "IN":
            # loop over input messages within signal
            for signal in device_data_dict["IN"].keys():
                # store data into table declaration field
                text_chunks.tableDeclaration["in"].append(
                    "In"
                    + "_"
                    + device
                    + "_"
                    + signal
                    + "_Table : "
                    + "In_Table_Info_Type\n"
                )

            # store data for table assignment
            for signal, data_list in device_data_dict["IN"].items():
                for data in data_list:

                    # define dict for Mon Validity Kind
                    mon_validity_kind_dict: {
                        "Trustable": [
                            "(Mon_Validity_Kind => Conversion_Types.Non_Trustable,",
                            f"Non_Trust_Ptr     => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Valid'Address);",
                        ],  # type: ignore
                        "Non_Trustable": [
                            "(Mon_Validity_Kind => Conversion_Types.Non_Trustable,",
                            f"Non_Trust_Ptr     => {device}_State.{device}_{data.variable_name}_Mon({data.index_name}).Valid'Address);",
                        ],  # type: ignore
                        "None": ["(Mon_Validity_Kind => Conversion_Types.Non_Trustable);"],  # type: ignore
                    }  # type: ignore

                    # mon_validity_multilines = "\n".join(
                    #     mon_validity_kind_dict[data.mon_format_validity].values()
                    # )

        #                     text_chunks.tableAssignment["in"].append(
        #                         f"""
        # In_{device}_{signal}_Msg ({data.index_name})
        #    ({device}_Icd_Types.{data.variable_name}).Mon_Validity :=
        #       {mon_validity_multilines}

        # In_{device}_{signal}_Msg ({data.index_name})
        #    ({device}_Icd_Types.{data.variable_name}).Mon_Data :=
        #       (Mon_Validity_Kind => Conversion_Types.Non_Trustable,
        #       Non_Trust_Ptr => {device}_State.{device}_{signal}_{data.variable_name}_Mon({data.index_name}).Valid'Address);
        # """
        #                     )

        # output case
        elif in_out == "OUT":
            # loop over input messages within signal
            for signal in device_data_dict["OUT"].keys():
                # store data into table declaration field
                text_chunks.tableDeclaration["out"].append(
                    "Out"
                    + "_"
                    + device
                    + "_"
                    + signal
                    + "_Table : "
                    + "Out_Table_Info_Type\n"
                )

    # write table declaration
    for in_out in text_chunks.tableDeclaration.keys():
        if len(text_chunks.tableDeclaration[in_out]) > 0:

            # input case
            if in_out == "in":
                # add heading comments
                text_chunks.tableDeclaration["in"].insert(0, "--Define input tables\n")
                # add some new empty lines at the end of mon types as separators
                text_chunks.tableDeclaration["in"].append("\n\n\n")
                # write
                for input_table_declaration in text_chunks.tableDeclaration["in"]:
                    file.write(input_table_declaration)

            # output case
            elif in_out == "out":
                # add heading comments
                text_chunks.tableDeclaration["out"].insert(
                    0, "--Define output tables\n"
                )
                # add some new empty lines at the end of mon types as separators
                text_chunks.tableDeclaration["in"].append("\n\n\n")
                # write
                for output_table_declaration in text_chunks.tableDeclaration["out"]:
                    file.write(output_table_declaration)


# generate content for file "icd_types.1.txt"
def generate_icd_types_1_code(file, device_data_dict):
    pass


# generate content for file "state.1.txt"
def generate_state_1_code(file, device_data_dict):
    pass


# entry point
def generate_code(data_dict):

    # create final_output folder if not present
    output_folder = "output/final_output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # loop through
    # device -> ("VUHF", "EGI", "TACAN", ...)
    # device_data_dict -> dictonary associated to each device
    for device, device_data_dict in data_dict.items():

        # generate file -> di.1.txt
        file_name = device.lower() + "_di_1.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as di_1_file:
            generate_di_1_code(di_1_file, device, device_data_dict)

        # generate file -> di.2.txt"
        file_name = device.lower() + "_di_2_.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as di_2_file:
            generate_di_2_code(di_2_file, device, device_data_dict)

        # generate file -> icd_types.1.txt
        file_name = device.lower() + "_icd_types_1.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as icd_types_1_file:
            generate_icd_types_1_code(icd_types_1_file, device_data_dict)

        # generate file -> state.1.txt
        file_name = device.lower() + "_state_1.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as state_1_file:
            generate_state_1_code(state_1_file, device_data_dict)

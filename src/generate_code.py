import os

# generate content for file "di.1.txt"
def generate_di_1_code(file, device, device_data_dict):

    # define text chunks class present "di.1.ada"
    class TextChunks:
        def __init__(self):
            # Initializing each field as an empty list
            self.monTypes = []
            self.monGetProcedures = []

    # create instance
    text_chunks = TextChunks()

    # loop over signals within device
    for signal in device_data_dict["IN"].keys():
        # loop over input messages within signal
        for message in device_data_dict["IN"][signal]:
            # store mon types
            text_chunks.monTypes.append(
                "type "
                + device
                + "_"
                + message.variable_name
                + "_"
                + "Mon_Type   "
                + "is limited private\n"
            )

            # store mon procedures
            chunk = f"""procedure Get_{message.variable_name}
   (Dev_Index : in  Fmsb_Config_Types.Vuhf_Index;
   Mon       : in  {device}_{message.variable_name}_Mon_Type;
   Value     : out {device}_Types.{message.variable_name}_Type;
   Valid     : out Boolean);"""

            text_chunks.monGetProcedures.append(chunk + "\n\n")

    # write mon types
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
    # for signal in device_data_dict.keys():
    #     # loop over input messages within signal
    #     for in_out in device_data_dict[signal].keys():
    #         if in_out == "IN":
    #             text_chunks.tableDeclaration["in"].append(
    #                 "In_" + device + "_" + signal + "_Table"
    #             )
    #         elif in_out == "OUT":
    #             text_chunks.tableDeclaration["out"].append(
    #                 "Out_" + device + "_" + signal + "_Table"
    #             )

    # # write table declaration
    # if len() > 0:
    #     # add heading comments
    #     text_chunks.tableDeclaration["in"].insert(0, "--Define input tables\n")
    #     # write


# generate content for file "icd_types.1.txt"
def generate_icd_types_1_code(file, device_data_dict):
    pass


# generate content for file "state.1.txt"
def generate_state_1_code(file, device_data_dict):
    pass


# generate files
def generate_code(data_dict):

    # create output folder if not present
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for device, device_data_dict in data_dict.items():

        # di.1.txt
        file_name = device.lower() + "_di_1.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as di_1_file:
            generate_di_1_code(di_1_file, device, device_data_dict)

        # di.2.txt"
        file_name = device.lower() + "_di_2_.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as di_2_file:
            generate_di_2_code(di_2_file, device, device_data_dict)

        # icd_types.1.txt
        file_name = device.lower() + "_icd_types_1.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as icd_types_1_file:
            generate_icd_types_1_code(icd_types_1_file, device_data_dict)

        # state.1.txt
        file_name = device.lower() + "_state_1.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as state_1_file:
            generate_state_1_code(state_1_file, device_data_dict)

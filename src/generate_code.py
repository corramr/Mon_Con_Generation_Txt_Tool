import os
from src import utils





# generate content for file "di.1.txt"
def generate_di_1_code(file, device, device_data_dict):

    # create instance
    class Text_Chunk(): 
        def __init__(self):
    # Initializing each field as an empty list
            self.scr_num = 0
            self.traceability_start = "-- @MODIF "+str(self.scr_num) +"\n"
            self.traceability_end = "-- @/MODIF "+str(self.scr_num) +"\n"
            self.monTypes = ["--Mon Types\n","\n\n\n"]
            self.monGetProcedures = ["--Mon Get procedures \n","\n\n\n"]
            self.monArrayOf = ["--Mon array of \n","\n\n\n"]
            self.monSideType = ["--Mon Side type\n","\n\n\n"]
            self.nullConstant = ["--Null constants\n","\n\n\n"]
    
    text_chunks = Text_Chunk()
    first_row = True 

    count = 2

    # loop over signals within device ("VUx Mode", "VUx Status data", ...)
    for signal in device_data_dict["IN"].keys():
        print(str(len(device_data_dict["IN"][signal])))
        # loop over input messages within signal
        # each signal is made of several messages which are located in specific words
        # for example, the signal VUx Mode contains:  (Aj_Select, Aj_Master, Time_Mode, ...)
        for message in device_data_dict["IN"][signal]:
            
            if first_row:
                first_row = False
                for attr_name, value in text_chunks.__dict__.items():
                    print(type(value))

                        # Skip non-list fields (e.g., scr_num), TODO for dictionaries
                    if isinstance(value, list):
                        value.insert(1,"-- @MODIF " + str(int(message.scr_num)) + "\n")
                
                text_chunks.scr_num = int(message.scr_num)
                print("sono in if first")

            print("text chunk scr : "+ str(text_chunks.scr_num))
            print("message scr: " + str(int(message.scr_num))) 
            # clean up variables without impacting raw data
            cleaned_variable_name = utils.clean_string(message.variable_name) 
            cleaned_device = utils.clean_string(device)
            
            # store mon types
            chunk = f"""type {cleaned_device}_{cleaned_variable_name}_Mon_Type   is limited private\n"""

            text_chunks.scr_number = message.scr_num
            

            text_chunks.monTypes.insert(count,chunk +"\n\n")


            # store mon procedures
            chunk = f"""procedure Get_{cleaned_variable_name}  
   (Dev_Index : in  Fmsb_Config_Types.{message.index_name}; 
   Mon       : in  {cleaned_device}_{cleaned_variable_name}_Mon_Type;
   Value     : out {cleaned_device}_Types.{cleaned_variable_name}_Type;
   Valid     : out Boolean);"""

            text_chunks.monGetProcedures.insert(count, chunk + "\n\n")

            # store definition of MonArrayOf 
            chunk = f"""type {cleaned_device}_{cleaned_variable_name}_Mon_Type is
   array (Fmsb_Config_Types.{message.index_name}) of {cleaned_device}_{cleaned_variable_name}_Mon_Side_Type;
            """

            text_chunks.monArrayOf.insert(count,chunk + "\n\n")

            # store side types
            chunk = f"""type {cleaned_device}_{cleaned_variable_name}_Mon_Side_Type is
   record
      Value: ***PLACEHOLDER***;
      Valid: Boolean;
   end record;
            """

            text_chunks.monSideType.insert(count,chunk + "\n\n")

            # store null constants
            
            chunk = f"""NULL_{cleaned_variable_name.upper()}_MON_SIDE :
   constant {cleaned_device}_{cleaned_variable_name}_Mon_Side_Type :=
      {cleaned_device}_{cleaned_variable_name}_Mon_Side_Type'
         (Value => ***PLACEHOLDER***,
          Valid => False);
        """
            
            text_chunks.nullConstant.insert(count,chunk + "\n\n")
            
            count = count + 1
            print(count)

        if text_chunks.scr_num != message.scr_num:
            print("entro in if diverso")
            utils.update_traceability(text_chunks,count,message)


    text_chunks.monTypes.append("-- @/MODIF "+str(text_chunks.scr_num)+"\n")



    ####################################################################

    # write mon types
    utils.write_fields_to_file(text_chunks,file)

# generate content for file "di.2.txt"
def generate_di_2_code(file, device, device_data_dict):

    # define text chunks class present "di.2.ada"
    class TextChunks:
        def __init__(self):
            # Initializing each field as an empty list
            self.tableDeclaration = {"In": ["--Input table type\n","\n\n\n"], "Out": ["--Output table type:\n","\n\n\n"]}
            self.messageDeclaration = {"in": [], "out": []}
            self.tableAssignment = {"In": [], "Out": []}
            self.messageAssignment = {"in": [], "out": []}
            self.monGetProcedures = []

    # create instance
    text_chunks = TextChunks()
    
    # clean up input for ADA standards
    cleaned_device = utils.clean_string(device)

    for in_out, values in device_data_dict.items():
        cleaned_input = utils.clean_string(in_out)
        for signal in values:
            cleaned_signal = utils.clean_string(signal)
            data_table = f"""{cleaned_input}_{cleaned_signal}_Data_Table """
            chunk = f"""{data_table}     : {cleaned_input}_Table_Info_Type;"""     
            text_chunks.tableDeclaration[cleaned_input].insert(1,chunk+"\n\n")
            print(str(signal))
            for message in device_data_dict[in_out][signal]:
                cleaned_index =utils.clean_string(message.index_name)
                if in_out == "IN":
                    chunk = f"""{data_table}({cleaned_index}) :=
    Conversion.In_Table_Type_Info'
        (Msg_Format   => {cleaned_device}_Icd_Types.In_{cleaned_device}_Data_Format'Address,
         Mon_List     => In_{cleaned_device}_Data_Msg ({cleaned_index})'Address,
         Num_Mons     => {cleaned_device}_Icd_Types.In_{cleaned_device}_Data_Format'Lenght);
                """
                else:
                    chunk = f"""{data_table} ({cleaned_index}) := 
    (Lenght_Of_Msg => {cleaned_device}_Icd_Types.OUT_{cleaned_signal.upper()}_LEN,
     Msg_Format    => {cleaned_device}_Icd_Types.Out_{cleaned_device}_Data_Format'Address,
     Con_List      => Out_{cleaned_device}_Data_Msg ({cleaned_index})'Address,
     Num_Cons      => {cleaned_device}_Icd_Types.Out_{cleaned_device}_Data_Format'Lenght);"""
            text_chunks.tableAssignment[cleaned_input].insert(1,chunk+"\n\n")

    utils.write_fields_to_file(text_chunks,file)
    '''
    # # loop over signals within device
    for in_out in device_data_dict.keys():
        # input case
    
        if in_out == "IN":
            # loop over input messages within signal
            for signal in device_data_dict["IN"].keys():
                # store data into table declaration field
                cleaned_signal = utils.clean_string(signal)

                chunk = f"""In_{cleaned_device}_{cleaned_signal}_Table    : In_Table_Info_Type\n"""
                print(chunk)

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

                    
                    
                    dictionary = mon_validity_kind_dict["Trustable"] 
                    print(dictionary)

                    # mon_validity_multilines = "\n".join(
                    #     mon_validity_kind_dict[data.mon_format_validity].values()
                    # )
                    '''
    '''
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

'''

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
def generate_state_1_code(file, device_data_dict, device):
    class Text_Chunk:
        def __init__(self):
            self.MonSubtypeDefinition = ["--Subtype definition: ","\n\n\n"]
            self.MonSubtypeDeclaration = ["--Subtype declaration: ", "\n\n\n"]
    
    text_chunks = Text_Chunk()

    for signal in device_data_dict["IN"].keys():
        # loop over input messages within signal
        # each signal is made of several messages which are located in specific words
        # for example, the signal VUx Mode contains:  (Aj_Select, Aj_Master, Time_Mode, ...)
        for message in device_data_dict["IN"][signal]:
           cleaned_variable_name = utils.clean_string(message.variable_name)
           cleaned_device = utils.clean_string(device)

           # store mon subtype definition

           mon_type = f"""{cleaned_device}_{cleaned_variable_name}_Mon_Type"""
           mon_name = f"""{cleaned_device}_{cleaned_variable_name}_Mon"""

           chunk = f"""subtype {mon_type}   is {cleaned_device}_Di.{cleaned_device}_{cleaned_variable_name}_Mon_Type;"""
           
           text_chunks.MonSubtypeDefinition.insert(1,chunk + "\n\n")

           # store mon subtype declaration
           chunk = f"""{mon_name}   : {mon_type}"""

           text_chunks.MonSubtypeDeclaration.insert(1,chunk + "\n\n")
    
    utils.write_fields_to_file(text_chunks,file)


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
            generate_state_1_code(state_1_file, device_data_dict, device)

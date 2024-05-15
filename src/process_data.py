def process_data(raw_data):

    # Initialized processed data
    processed_data = []

    # Get the 'function' column and remove duplicates
    components = list(set(raw_data['Function']))

    raw_data

    # for component in components:
    #     component_dict = {}
    #     for 
    #     process_data.append()


    processed_data = [
        {
            "Generate_Code": "True",
            "Device_Name": "Vuhf",
            "Signal_Name": "Vux_Status_Data",
            "Input_Output": "Input",
            "Validity": False,
            "Format_Name": "Frequency_Tens_Digit",
            "Type": "Scaled_Int",
            "Enum_Values": None,
            "Record": True,
            "Word": 1,
            "Msb": 0,
            "Lsb": 3,
            "Msb_Sign_Bit": False,
            "Lsb_Weight": 10,
            "Max_Value": 150,
            "Min_Value": 0,
        },
        {
            "Generate_Code": "True",
            "Device_Name": "Vuhf",
            "Signal_Name": "Vux_Status_Data",
            "Input_Output": "Input",
            "Validity": False,
            "Format_Name": "Frequency_Ones_Digit",
            "Type": "Scaled_Int",
            "Enum_Values": None,
            "Record": True,
            "Word": 1,
            "Msb": 4,
            "Lsb": 7,
            "Msb_Sign_Bit": False,
            "Lsb_Weight": 1,
            "Max_Value": 15,
            "Min_Value": 0,
        },
        {
            "Generate_Code": "True",
            "Device_Name": "Vuhf",
            "Signal_Name": "Vux_Status_Data",
            "Input_Output": "Input",
            "Validity": False,
            "Format_Name": "Frequency_Tenths_Digit",
            "Type": "Scaled_Int",
            "Enum_Values": None,
            "Record": True,
            "Word": 1,
            "Msb": 8,
            "Lsb": 11,
            "Msb_Sign_Bit": False,
            "Lsb_Weight": 1,
            "Max_Value": 15,
            "Min_Value": 0,
        },
        {
            "Generate_Code": "True",
            "Device_Name": "Vuhf",
            "Signal_Name": "Vux_Status_Data",
            "Input_Output": "Input",
            "Validity": False,
            "Format_Name": "Frequency_Offset_50_Khz",
            "Type": "Bool",
            "Enum_Values": None,
            "Record": False,
            "Word": 1,
            "Msb": 12,
            "Lsb": 12,
            "Msb_Sign_Bit": None,
            "Lsb_Weight": None,
            "Max_Value": None,
            "Min_Value": None,
        },
        {
            "Generate_Code": "True",
            "Device_Name": "Vuhf",
            "Signal_Name": "Vux_Status_Data",
            "Input_Output": "Input",
            "Validity": False,
            "Format_Name": "Rt_Mode",
            "Type": "Lookup_Straight_2_Bit",
            "Enum_Values": {
                "Format": "Bin",
                "Values": [
                    {"Dec_Code": 0, "Value": "Tr"},
                    {"Dec_Code": 1, "Value": "Tr_G"},
                    {"Dec_Code": 2, "Value": "Spare"},
                    {"Dec_Code": 3, "Value": "Unknown"},
                ],
            },
            "Record": False,
            "Word": 2,
            "Msb": 0,
            "Lsb": 1,
            "Msb_Sign_Bit": None,
            "Lsb_Weight": None,
            "Max_Value": None,
            "Min_Value": None,
        },
        {
            "Generate_Code": "True",
            "Device_Name": "Vuhf",
            "Signal_Name": "Vux_Data_Fill",
            "Input_Output": "Output",
            "Validity": False,
            "Format_Name": "Command_Word",
            "Type": "Lookup_Straight_32_Val",
            "Enum_Values": {
                "Format": "Hex",
                "Values": [
                    {"Dec_Code": 10, "Value": "Wod_Mwod_Load"},
                    {"Dec_Code": 12, "Value": "Have_Quick_Ii_Fmt_Load"},
                    {"Dec_Code": 30, "Value": "Saturn_Special_Training_Frequencies"},
                ],
            },
            "Record": False,
            "Word": 1,
            "Msb": 0,
            "Lsb": 15,
            "Msb_Sign_Bit": None,
            "Lsb_Weight": None,
            "Max_Value": None,
            "Min_Value": None,
        },
    ]
    return processed_data

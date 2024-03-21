def generate_code(processed_data):

    generate_icd_types()


def generate_icd_types():

    Format_Element_Array = [
        "Frequency_Tens_Digit",
        "Frequency_Ones_Digit",
        "Frequency_Tenths_Digit",
        "Frequency_Offset_50_Khz",
        "Rt_Mode",
    ]

    Input_Output = "Input"

    class Message:
        def __init__(self, format_name, type, word, msb, lsb):

            self.format_name = format_name
            self.type = type
            self.word = word
            self.msb = msb
            self.lsb = lsb

    # Creating a list of Signal objects
    signal = [
        Message(
            format_name="Frequency_Tens_Digit", type="Scaled_Int", word=1, msb=0, lsb=3
        ),
        Message(
            format_name="Frequency_Ones_Digit", type="Scaled_Int", word=2, msb=4, lsb=7
        ),
        Message(
            format_name="Frequency_Tenths_Digit",
            type="Scaled_Int",
            word=3,
            msb=8,
            lsb=11,
        ),
        # Add more objects as needed
    ]

    var = "vuhf"
    filename = f"{var}_icd_types.txt"

    content = f"""
           {signal[0].format_name} =>
             (Kind           => Conversion_Types.Scaled_Int,
              In_Validity    => (Kind => Conversion_Types.Msg_Only),
              Scaled_Int_Fmt =>
                (Location     => (Word => 0, Msb => 0, Lsb => 3),
                 Msb_Sign_Bit    => False,
                 Min_Value       => 0,
                 Max_Value       => 150,
                 Lsb_Weight      => 10)),
    """

    # Open the file in write mode and write the content
    with open(filename, "w") as file:
        file.write(content)

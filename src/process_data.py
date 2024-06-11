from collections import defaultdict


# Define class: each row of the excel file will be an instance of this class
class DataRow:
    def __init__(
        self,
        device,
        message_name,
        variable_name,
        word_start,
        word_end,
        msb,
        lsb,
        variable_type,
        min,
        max,
        lsb_weight,
        in_out,
        mon_data_validity,
        mon_format_validity,
        index_name,
        index_num,
        enabled,
    ):
        self.device = device
        self.message_name = message_name
        self.variable_name = variable_name
        self.word_start = word_start
        self.word_end = word_end
        self.msb = msb
        self.lsb = lsb
        self.variable_type = variable_type
        self.min = min
        self.max = max
        self.lsb_weight = lsb_weight
        self.in_out = in_out
        self.mon_data_validity = mon_data_validity
        self.mon_format_validity = mon_format_validity
        self.index_name = index_name
        self.index_num = index_num
        self.enabled = enabled


def process_data(raw_data):

    # Initialize
    data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    # Arrange data into a dictionary of  a list of objects
    # The key is the device (VUHF, HF, EGI, MC ...)
    # To each key is associated a number of objects (one object corresponds to one row in the excel file)
    for _, row in raw_data.iterrows():
        data_row = DataRow(
            row["Function"],
            row["Signal name"],
            row["ICD VARIABLE_NAME"],
            row["word start"],
            row["word end"],
            row["msb"],
            row["lsb"],
            row["type (IRS)"],
            row["Min"],
            row["Max"],
            row["RES /\nLSB weight"],
            row["IN / OUT"],
            row["MON DATA VALIDITY"],
            row["MON FORMAT VALIDITY"],
            row["INDEX NAME"],
            row["INDEX NUM"],
            row["ENABLED"],
        )

        data_dict[row["Function"]][row["IN / OUT"]][row["Signal name"]].append(data_row)

    # Return dictionary
    return data_dict

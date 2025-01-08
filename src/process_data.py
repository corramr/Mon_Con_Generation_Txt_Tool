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

    # Filter and Sort the lists in the nested dictionary
    for function_dict in data_dict.values():
        for in_out_dict in function_dict.values():
            for signal_name, data_list in in_out_dict.items():

                # filter according to "ENABLED" field
                filtered_list = [data for data in data_list if data.enabled]

                # Sort with custom key
                sorted_list = sorted(filtered_list, key=lambda x: (x.word_start, x.msb))

                # Check for duplicates
                for i in range(1, len(sorted_list)):
                    if (
                        sorted_list[i].word_start == sorted_list[i - 1].word_start
                        and sorted_list[i].msb == sorted_list[i - 1].msb
                    ):
                        raise ValueError(
                            f"Duplicate entry found with the same 'word_start' and 'msb' for Signal name: {signal_name}"
                        )

                # Update the list with the sorted one
                in_out_dict[signal_name] = sorted_list

    # Return dictionary
    return data_dict

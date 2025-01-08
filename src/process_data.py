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


# entry point
def process_data(filtered_data):

    # Initialize a dictionary which a dictionary which contains a dictionary which contains a list
    # See below for better clarifications
    data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    # Now we need to process filtered_data
    # filter_data is a subset of the total row and columns of the original excel file
    # you can see what filtered_data looks like in the folder output/filtered_data

    # for each row of filtered data we create an instance of the class DataRow
    # The instance of the class DataRow contains all the data of the current row
    for _, row in filtered_data.iterrows():
        data_row = DataRow(
            device=row["Function"],
            message_name=row["Signal name"],
            variable_name=row["ICD VARIABLE_NAME"],
            word_start=row["word start"],
            word_end=row["word end"],
            msb=row["msb"],
            lsb=row["lsb"],
            variable_type=row["type (IRS)"],
            min=row["Min"],
            max=row["Max"],
            lsb_weight=row["RES /\nLSB weight"],
            in_out=row["IN / OUT"],
            mon_data_validity=row["MON DATA VALIDITY"],
            mon_format_validity=row["MON FORMAT VALIDITY"],
            index_name=row["INDEX NAME"],
            index_num=row["INDEX NUM"],
            enabled=row["ENABLED"],
        )

        # We now allocate the current instance of data_row into data_dict structure
        # The data_row instance is allocated according to:
        # row["function"]     (device: VUHF, HF, ...)
        # row["IN / OUT"]     (in_out: IN, OUT)
        # row["signal_name"]  (message_name: VUx Mode, VUx Status Data, ...)

        # here below is reported an example of what data_dict might look like
        # data_dict = {
        #               "VUHF": {
        #                         "OUT": {
        #                                  "VUx Mode": [data_row, data_row, data_row, ...]
        #                                  "VUx Status Data": [data_row, data_row, ...]
        #                                  "VUx Saturn Parameters": [data_row, data_row, data_row, data_row, ...]
        #                                  "..."
        #                                }
        #                         "IN": ...
        #                       }
        #               "..."
        #             }
        data_dict[row["Function"]][row["IN / OUT"]][row["Signal name"]].append(data_row)

    # Filter and Sort the lists in the nested dictionary
    for function_dict in data_dict.values():
        for in_out_dict in function_dict.values():
            for signal_name, data_list in in_out_dict.items():

                # filter according to "ENABLED" field
                # you only want to the rows with the "ENABLED" field set to TRUE
                filtered_list = [data for data in data_list if data.enabled]

                # Here all the several data_row instances (of a specific device, in/out, signal name) are sorted according
                # to the word_start and to the most_significant_bit (msb)
                # this will be useful when generating mons and cons
                sorted_list = sorted(
                    filtered_list, key=lambda row: (row.word_start, row.msb)
                )

                # Check for duplicates
                # we perform a double check for duplicates since we do not want to generate twice a mon/con
                # if we find a duplicate we raise an error
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

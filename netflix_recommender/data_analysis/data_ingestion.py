import os
import re
import pandas as pd
from data_analysis.data_ingestion_utils import split_list, input_num_to_string

# TODO: wrap a part in data_ingestion_utils and create a single csv in pandas to output
#  \n This will be preprocessed and be ready for analysis

working_dir = os.getcwd()

list_of_dataframes = []
for data_file in os.listdir(working_dir):
    pattern = "_\d.txt"
    match = re.search(pattern, data_file)
    if match:
        print(f"Matching file: {match}")
        line_nums = []
        data_lines = []
        i = 1
        with open(data_file) as f:
            for line in f:
                line = line.replace('\n', '')
                if ':' in line:
                    line_nums.append(line.replace(":", ''))
                    data_lines.append('sep')
                else:
                    data_lines.append(line)
            i += 1

        lines_split = split_list(data_lines, 'sep')
        all_lines_complete = []
        for i in range(len(line_nums)):
            for j in range(len(lines_split[i])):
                item_data_line = input_num_to_string(lines_split[i][j], line_nums[i])
                all_lines_complete.append(item_data_line.split(','))

        df = pd.DataFrame(all_lines_complete, columns=["itemID", "userID", "rating", "date"])
        list_of_dataframes.append(df)
        print(f"Ended appending file: {data_file}")

pd.concat(list_of_dataframes).to_csv(working_dir + '/dataframes_3_4.csv')
print("Ending print")
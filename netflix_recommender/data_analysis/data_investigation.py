import pandas as pd
from data_analysis.analysis_utils import split_list


line_nums = []
lines = []
upper_limit = 10000
i = 1
with open("./combined_data_1.txt") as f:
    for line in f:
        line = line.replace('\n', '')
        if ':' in line:
            line_nums.append(line.replace(":", ''))
            lines.append('sep')
        else:
            lines.append(line)
    i += 1

lines_split = split_list(lines, 'sep')
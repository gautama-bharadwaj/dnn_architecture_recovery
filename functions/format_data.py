import pandas as pd
import csv
from time import sleep

def time_series_write_to_csv(filename):
    file_name, num = filename.split("-")
    df = pd.read_fwf('raw_output/'+file_name+'.txt', skiprows = [0,1], delim_whitespace=True)
    df = df.rename(columns=lambda x:x.strip())
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('^unit')]
    df = df.apply(lambda x: x.str.strip() if x.dtype=="object" else x)

    csv_file = open('output/'+filename+'.csv', 'w', encoding='UTF8')
    writer = csv.writer(csv_file)
    csv_header = ['time']
    dict_keys = []
    data_dict = {}
    for index, row in df.iterrows():
        if (row['count'].replace(',', '') == 'count'):
            continue
        if row['time'] not in data_dict:
            data_dict[row['time']] = {}
        # print(row['count'].replace(',', ''))
        if (row['count'].replace(',', '') == 't counted>' or row['count'].replace(',', '') == 'counted>' or row['count'].replace(',', '') == '<not counted>'):
            row['count'] = '0'
        if (row['event'] not in csv_header):
            csv_header.append(row['event'])
            dict_keys.append(row['event'])
        # if ('label' not in csv_header):
        #     csv_header.append('label')
        #     dict_keys.append('label')
        data_dict[row['time']][row['event']] = int(row['count'].replace(',',''))
        # data_dict[row['time']]['label'] = file_name
        lines = index
    writer.writerow(csv_header)
    for key in data_dict.keys():
        csv_row = []
        csv_row.append(float(key))
        for sub_key in dict_keys:
            csv_row.append(data_dict[key][sub_key])
        writer.writerow(csv_row)
    return len(data_dict.keys())+1


def aggregate_write_to_csv(filename):
    sleep(1)
    file_name, num = filename.split("-")
    f = open('raw_output/test.txt', 'r')
    hpc = ['cycles', 'branches', 'instructions', 'cache-references', 'cache-misses', 'bus-cycles', 'branch-loads', 'iTLB-load-misses', 'dTLB-load-misses']
    lines = f.readlines()
    count_list = []
    event_list = []
    for line in lines:
        line_list = line.split()
        print(line_list)
        if ((len(line_list)>0) and (line_list[1] in hpc)):
            count = int(line_list[0].replace(',',''))
            event = line_list[1]
            count_list.append(count)
            print(event)
            event_list.append(event)
    count_list.append(file_name)
    print(count_list)
    print(event_list)
    csv_file = open('output/aggregate.csv',
                    'a', encoding='UTF8')
    writer = csv.writer(csv_file)
    writer.writerow(count_list)
    # with open('raw_output/'+file_name+'.txt', 'r') as current:
    #     lines = current.readlines()
    #     if not lines:
    #         print('FILE IS EMPTY')
    #     else:
    #         for line in lines:
    #             print(line)
    # print(df)
    # df = df.rename(columns=lambda x: x.strip())
    # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # df = df.loc[:, ~df.columns.str.contains('^unit')]
    # df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

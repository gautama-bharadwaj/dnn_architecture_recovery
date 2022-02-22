import pandas as pd
import csv

def write_to_csv(file_name):
    df = pd.read_fwf('raw_output/'+file_name+'.txt', skiprows = [0,1], delim_whitespace=True)
    df = df.rename(columns=lambda x:x.strip())
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('^unit')]
    df = df.apply(lambda x: x.str.strip() if x.dtype=="object" else x)

    csv_file = open('output/'+file_name+'.csv', 'w', encoding='UTF8')
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
        if (row['count'].replace(',', '') == 't counted>' or row['count'].replace(',', '') == '<not counted>'):
            row['count'] = '0'
        if (row['event'] not in csv_header):
            csv_header.append(row['event'])
            dict_keys.append(row['event'])
        data_dict[row['time']][row['event']] = int(row['count'].replace(',',''))
    writer.writerow(csv_header)
    for key in data_dict.keys():
        csv_row = []
        csv_row.append(float(key))
        for sub_key in dict_keys:
            csv_row.append(data_dict[key][sub_key])
        writer.writerow(csv_row)

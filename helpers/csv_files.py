import re
import csv
def read_data_csv():
    a = [];
    with open('data.csv', 'r', encoding='utf-8') as csvfile:
        for row in csvfile:
            a.append(re.sub('^"|"$', '', row.replace('\n', '').replace('""', '"')))
    return a

def write_data_csv(result_row):
    with open('contract_features.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow(['tot_claim_cnt_l180d', 'disb_bank_loan_wo_tbc', 'day_sinlastloan'])
        writer.writerow(result_row)

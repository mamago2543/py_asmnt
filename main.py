from helpers import csv_files, arrays, features

if __name__ == '__main__':
    #Читаем файл
    arr = csv_files.read_data_csv()
    # Видим, что в некоторых местах произошёл разрыв строки - исправляем
    arrays.unite_gap(arr)
    #Надо сделать функцию на проврку корректности введённых данных?

    h = arr.pop(0).split(',')
    arrays.decode_str(h, arr)
    result_row = [];
    result_row.append(features.tot_claim_cnt_l180d(arr)) #задание 1
    result_row.append(features.disb_bank_loan_wo_tbc(arr))  # задание 2
    result_row.append(features.day_sinlastloan(arr))  # задание 3

    csv_files.write_data_csv(result_row)






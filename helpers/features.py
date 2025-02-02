import datetime
def tot_claim_cnt_l180d(arr, dt = '' ):
    #   В массивах JSON-в обрабатываемых сообщений можно увидеть контракты с повторяющимся claim_id содержащими идентичные данные,
    #поэтому будем запоминать номера контратов по которым мы прошлись, чтобы не дублировать подсчитанные займы
    #   Сделал возможность передать дату в формате yyyy-mm-dd, если вдруг захочется считать на указанную дату
    #   Пустые claim_id считаем как полноценное значение, если claim_date не пуст- это следует из условия
    if dt == '':
        today_date = datetime.datetime.today() #сегодня не округляем, чтобы займы на дату вычисления учитывать
    else:
        today_date = datetime.datetime.strptime(dt, "%Y-%m-%d")
    start_date = today_date - datetime.timedelta(days=180)
    claims_array = [] # уже учтённые займы
    result = 0
    for k in range(0,len(arr)):
        for i in range(0,len(arr[k]['contracts'])):
            if arr[k]['contracts'][i]['claim_date'] == '':
                continue
            claim_date = datetime.datetime.strptime(arr[k]['contracts'][i]['claim_date'], "%d.%m.%Y")
            if claim_date > start_date and claim_date <= today_date:
                if arr[k]['contracts'][i]['claim_id'] not in claims_array:
                    claims_array.append(arr[k]['contracts'][i]['claim_id'])
                    result += 1
    if len(claims_array) == 0:
        return -3
    else:
        return result

def disb_bank_loan_wo_tbc(arr):
    #   Есть ли тут вероятность посчитать какие-то данные дважды?
    #Посмотрел все контракты, где loan_summa не пустая и больше нуля - вижу повторяющиеся контракты :
    #(номер строки в arr, номер контракта в строке, сам контракт
    #989 3 {'contract_id': 3304674, 'bank': '062', 'summa': 405000000, 'loan_summa': 217320883, 'claim_date': '14.02.2022', 'claim_id': 3304674, 'contract_date': '14.02.2022'}
    #991 3 {'contract_id': 3304674, 'bank': '062', 'summa': 405000000, 'loan_summa': 217320883, 'claim_date': '14.02.2022', 'claim_id': 3304674, 'contract_date': '14.02.2022'}
    #995 3 {'contract_id': 3304674, 'bank': '062', 'summa': 405000000, 'loan_summa': 217320883, 'claim_date': '14.02.2022', 'claim_id': 3304674, 'contract_date': '14.02.2022'}
    #Исходя из всех данных, сделал вывод, что сумму мы считаем, по уникальным claim_id
    #   Не очень понятна часть условия "Disbursed loans means loans where contract_date is not null" - кредиты, по которым были выплаты имет дату контракта не null
    #А как нам это помогает? По данным, всякий контракт, где loan_summa не пустая и больше нуля, имеет не пустую contract_date
    #В итоге поставлю ограничение на поле cjntract_date, но в текущих данных оно ничего не фильтрует
    claims_array = []
    loan_summ = 0;
    for k in range(0, len(arr)):
        for i in range(0, len(arr[k]['contracts'])):
            contract = arr[k]['contracts'][i]
            if 'bank' in contract:
                bank = contract['bank']
            else:
                bank = ''
            if contract['loan_summa'] != '' and contract['loan_summa'] !=0 and bank not in ['LIZ', 'LOM', 'MKO', 'SUG', ''] and contract['claim_id'] not in claims_array:
                claims_array.append(contract['claim_id'])
                loan_summ += contract['loan_summa']

    if len(claims_array) == 0:
        return -3
    if loan_summ == 0:
        return -1
    return loan_summ

def day_sinlastloan(arr):
    #   Как я понимаю в данном контексте под клиентом мы понимаем contract_id, то есть клиента идентифицирует контракт в данном контексте
    #   Либо под клиентом мы понимаем строку нашего файла
    #   В итоге как я понял задание: для каждого application(строки) находим самый поздний контракт, где summa не пусто - считаем разницу с application_date и потом суммируем по всем строкам
    found_claim = False
    result = 0
    for k in range(0, len(arr)):
        found_date = False
        for i in range(0, len(arr[k]['contracts'])):
            if arr[k]['contracts'][i]['summa'] != '' and arr[k]['contracts'][i]['contract_date'] != '':
                contract_date = datetime.datetime.strptime(arr[k]['contracts'][i]['contract_date'], "%d.%m.%Y")
                found_claim = True
                if not found_date:
                    found_date = True
                    max_date_contract = contract_date
                else:
                    if max_date_contract < contract_date:
                        max_date_contract = contract_date
        if found_date:
            result += ((arr[k]['application_date']).replace(tzinfo=None) - max_date_contract).days
    if not found_claim:
        return -3
    if result == 0:
        return -1
    return result

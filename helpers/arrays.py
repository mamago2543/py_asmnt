import re
import datetime
def unite_gap(arr):
    for i in range(len(arr) - 1, -1, -1):
        if arr[i].count('[') != arr[i].count(']'):
            arr[i - 1] += arr[i]
            arr.pop(i)

def decode_str(header, arr):
    def parse_contracts(str):
        if str == '':
            str = '[]'
        str = re.sub('^"|"$','',str).replace('""', '"')
        if str.count('[') == 0 and str.count(']') == 0:
            str = '[' + str + ']'
        exec( 'a =' + str, globals())
        return a

    for i in range(0,len(arr)) :
        splt = arr[i].split(',',2)
        arr[i] = {}
        arr[i][header[0]] = splt[0]
        try:
            arr[i][header[1]] = datetime.datetime.strptime(splt[1], "%Y-%m-%d %H:%M:%S.%f%z")
        except:
            print('Warning: Сообщение с id = ' + splt[0] + ' имеет нестандартный(%Y-%m-%d %H:%M:%S.%f%z) формат application_date')
            arr[i][header[1]] = datetime.datetime.strptime(splt[1], "%Y-%m-%d %H:%M:%S%z")
            print("     Оно имеет формат application_date в виде (%Y-%m-%d %H:%M:%S%z)")
        arr[i][header[2]] = parse_contracts(splt[2])
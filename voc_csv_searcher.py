import sys, os
import csv

if __name__ == '__main__':
    # ファイルをすべて読み込み
    data = []
    for csv_file in os.listdir('./voccsv/'):
        if csv_file[-4:] == '.csv':
            print(csv_file)

            #csv読み込み
            with open(csv_file) as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    data.append(row)
                    print(i+1, row)
    print('total', len(data), 'words')

    # 検索単語入力
    while True:
        print('---- input word ----')
        str_ = input()
        if str_ == 'exit':
            break
        for datum in data:
            if str_ == datum[0]:
                print(datum)
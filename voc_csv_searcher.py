import sys, os
import csv

if __name__ == '__main__':
    # ファイルをすべて読み込み
    csv_dir = './voccsv/'
    data = []
    for csv_file in os.listdir(csv_dir):
        if csv_file[-4:] == '.csv':
            #csv読み込み
            print(csv_dir + csv_file)
            with open(csv_dir + csv_file) as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    data.append((row, csv_file))
                    # print(i+1, row)
    print('total', len(data), 'words')

    # 検索単語入力
    while True:
        print('---- input word ----')
        str_ = input()
        if str_ == 'exit':
            break
        for datum in data:
            if str_ == datum[0][0]:
                print(datum)
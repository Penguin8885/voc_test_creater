import sys, os
import csv

if __name__ == '__main__':
    #csvファイル列挙 & 選択
    csv_dir = './voccsv/'
    for i, csv_file in enumerate(os.listdir(csv_dir)):
        if csv_file[-4:] == '.csv':
            print(i, csv_file)
    csvfile_index = int(input('choose number: '))
    csv_file = csv_dir + os.listdir(csv_dir)[csvfile_index]

    #csv読み込み
    data = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            data.append(row)
            print(i+1, row)

    #新規データ入力
    indata = []
    print('---- input word ----')
    while True:
        str_ = input()
        if str_ == 'exit':
            break
        if str_ == 'rm':
            rm = indata.pop()
            print('-> remove', rm)
            continue
        # word = [str_, '', ''] # 英単語だけ登録
        word = str_.replace('　', ' ').split(' ') # スペース区切りで分割
        word[0] = word[0].replace('_', ' ')       # アンダースコアは空白に直す
        if len(word) != 3:
            print('-> invaild')
            continue
        indata.append(word)
        print('-> add', word)

    #結合
    data.extend(indata)

    #csv書き込み
    with open(csv_file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    print('---- complete ----')

import sys, os
import subprocess
import csv

## CSVファイル選択画面表示関数
def printCsvSelectionScreen(csv_dir):
    # csvファイル列挙 & 選択
    for i, csv_file in enumerate(os.listdir(csv_dir)):
        if csv_file[-4:] == '.csv':
            print(i, csv_file)
    csvfile_index = int(input('choose number: '))

    return csv_dir + os.listdir(csv_dir)[csvfile_index] # 選択されたcsvファイル名を返却

## CSVファイルの読み込み関数
def inputWordData(csv_file):
    # CSVデータ読み込み，データリストの作成
    data = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row) # レコードを取り出して登録
    for i, datum in enumerate(data):
        print(i, datum)
    return data

## 単語がデータベースにあるか検索する関数
def search(target, data):
    for i, datum in enumerate(data):
        if datum[0] == target:
            return i
    else:
        return None

## 二次元リストをCSVに保存する関数
def save_csv(data, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    print('saved')


if __name__ == '__main__':
    # 情報
    csv_dir = './voccsv/'

    # データベース読み込み
    csv_filename = printCsvSelectionScreen(csv_dir)
    data = inputWordData(csv_filename)

    # 入力
    print('\ninput words you need')
    list_ = []
    while True:
        str_ = input()
        if str_ == 'exit':
            break

        # 検索
        index = search(str_, data)
        if index == None:
            print('cannot find "%s"' % str_)
        else:
            print('add -> ', data[index])
            list_.append(data[index])

    # 表示
    print('\nwords you input')
    for i, word in enumerate(list_):
        print(i+1, word)

    # 保存
    new_csv_filename = input('\ninput new csv filename to save: ')
    save_csv(list_, csv_dir + new_csv_filename)
import sys, os
import csv

if __name__ == '__main__':
    #csvファイル確認
    csv_file = sys.argv[1]
    if os.path.exists(csv_file) is False:
        if os.path.exitts('./' + csv_file) is False:
            print(sys.argv[1], 'does not exist')
            sys.exit(0)
        else:
            csv_file = './' + csv_file
    else:
        pass

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

    #ソート
    #data.sort(key=lambda x: x[0])

    #csv書き込み
    with open(csv_file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    print('---- complete ----')

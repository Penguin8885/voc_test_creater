import sys, os
import csv

if __name__ == '__main__':
    # csvファイル列挙 & 選択
    csv_dir = './voccsv/'
    for i, csv_file in enumerate(os.listdir(csv_dir)):
        if csv_file[-4:] == '.csv':
            print(i, csv_file)
    csvfile_index = int(input('choose number: '))
    csv_file = csv_dir + os.listdir(csv_dir)[csvfile_index]

    # csv読み込み
    data = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            data.append(row)
            print(i+1, row)

    # モード選択
    print('\n')
    print(' 0: regist complete data')
    print(' 1: regist incomplete data')
    print(' 9: fill up the incomplete data in each column')
    mode = int(input('choose the mode: '))

    # 新規データ入力
    if mode == 0 or mode == 1: #### 完全/不完全データ入力 ####
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
            else:
                word = str_.replace('　', ' ').split(' ') # スペース区切りで分割
                word[0] = word[0].replace('_', ' ')       # アンダースコアは空白に直す
                if len(word) > 3 or (mode == 0 and len(word) != 3):
                    print('-> invaild')
                    continue

                if len(word) == 1:
                    word = [word[0], '', '']      # 不完全データなら足りないところを補完
                elif len(word) == 2:
                    word = [word[0], word[1], ''] # 不完全データなら足りないところを補完

                indata.append(word)
                print('-> add', word)

        data.extend(indata) # 結合

    elif mode == 9: #### データ補完 ####
        break_ = False  # breakフラグ
        for column in range(3):
            i = 0
            while i < len(data) and break_ == False:
                if data[i][column] != '':
                    i += 1  # 補完しなくて良ければ次に行く
                    continue

                print(data[i], '\t\t(input about coulmn', column+1, ')')
                str_ = input()
                if str_ == 'exit':
                    break_ = True
                    break
                if str_ == 'rm':
                    if i == 0:
                        print('sorry, we cannot amend it')
                        print('please amend csv file directly')
                        break_ = True
                        break
                    data[i-1][column] = ''
                    i -= 1
                    continue
                if str_ == '':
                    i += 1 # データ入力されなかったときはそのまま次に行く
                    continue
                else:
                    data[i][column] = str_
                    print('-> updated', data[i])
                    i += 1

    else: #### 不適切な入力 ####
        print('your input is not proper')
        sys.exit(-1)

    # csv書き込み
    with open(csv_file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    print('---- complete ----')

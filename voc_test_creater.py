import sys, os
import subprocess
import random
from time import sleep
import datetime
import csv
import numpy as np

## ファイルの読み込み関数
def inputWordData(csv_file):
    # CSVデータ読み込み，データリストの作成
    data = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row) # レコードを取り出して登録
    for datum in data:
        print(datum)
    return data

## texの文字サイズを修飾
def addModifierOfSize(w):
    if len(w) >= 17:
        return r'{\scriptsize ' + w + r'}'
    elif len(w) >= 15:
        return r'{\small ' + w + r'}'
    else:
        return w

## texのテーブルの1行を生成
def createTexSytleOneLine(w1,w2,w3):
    line = r'    \bf ' + w1 \
         + r' & \BS & \bf ' + w2 \
         + r' & \BS & \bf ' + w3 \
         + r' & \BS\\' + '\n'
    return line

## 単語データからtexスタイルの文章を生成
def convertWotdData2TexStyle(data):
    # 単語を3個のずつ分けてTexの様式の文字列を作成
    line_list = []

    for i in range(0, len(data)-3, 3):
        # 最初は普通に3個ずつ分割して1行を生成
        w1 = addModifierOfSize(data[i+0][0])    # 単語データだけ読み出す
        w2 = addModifierOfSize(data[i+1][0])
        w3 = addModifierOfSize(data[i+2][0])
        line = createTexSytleOneLine(w1, w2, w3)
        line_list.append(line)
    else:
        # 最後は3個の足りない分を補って1行を生成
        last_num = len(data) % 3 if len(data) % 3 != 0 else 3 # 最後のデータの個数
        last_word = data[-last_num:]                    # 最後のデータ
        lack = 3 - last_num                             # 足りていない個数
        for j in range(lack):
            last_word.append(['','',''])                # 空の問題を付け足す
        w1 = addModifierOfSize(last_word[0][0])
        w2 = addModifierOfSize(last_word[1][0])
        w3 = addModifierOfSize(last_word[2][0])
        line = createTexSytleOneLine(w1, w2, w3)
        line_list.append(line)

    return line_list # 作成したtex形式の文のリストを返却

## texファイルとして出力
def outputTeX(data, tex_template_file):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') # 現在時刻
    out_filename = './test' + now + '.tex'                  # 出力ファイル名
    tmp_filename = tex_template_file                        # テンプレートのファイル名

    # テンプレートを読み込んで，表のところだけ問題で置換する
    with open(out_filename, mode='w',encoding="utf-8") as outf:
        with open(tmp_filename, mode='r',encoding="utf-8") as tmpf:
            for line in tmpf:
                if not r'%%%' in line:      # テンプレートの表部分の目印が'%%%'となっています
                    outf.write(line)        # テンプレートの行をそのまま出力
                else:
                    for datum in data[:20]:
                        outf.write(datum)   # 問題データを出力
    return out_filename

def main():
    #csvファイル列挙 & 選択
    csv_dir = './voccsv/'
    for i, csv_file in enumerate(os.listdir(csv_dir)):
        if csv_file[-4:] == '.csv':
            print(i, csv_file)
    csvfile_index = int(input('choose number: '))
    csv_filename = csv_dir + os.listdir(csv_dir)[csvfile_index]

    data = inputWordData(csv_filename) # 選択された英単語ファイル読み込み

    print('\n\n============ Input test info ============')
    top_index = int(input("単語先頭番号 : "))
    num       = int(input("問題数       : "))
    data = data[top_index:(top_index+num)]      # 英単語を選択
    # random.shuffle(data)                        # シャッフル

    print('\n\n============ Create PDF files ============')
    out_filename_list = []  # 出力したファイル名のリスト
    template_file = './tex_template/voc_test_template1.tex' # texテンプレートファイル
    compile_sh_file = './tex_template/cc.sh'                # コンパイル用シェルスクリプト
    for i in range(0, len(data), 60):
        page_data = data[i:(i+60)]                        # 1ページ分の問題を取り出す
        tex_data = convertWotdData2TexStyle(page_data)    # 英単語をtex形式のレコードに変換
        out_filename = outputTeX(tex_data, template_file) # 英単語テストのtexファイルを生成
        compile_cmd = 'sh ' + compile_sh_file + ' ' + out_filename # コンパイルコマンド
        rc = subprocess.call(compile_cmd)                 # コンパイル，PDF作成
        out_filename_list.append(out_filename)            # texファイル名を登録
        sleep(1)                                          # ファイル名が重複しないように1秒停止

    # 最後にファイル名を出力
    print('\n\n============ Created files ============')
    for name in out_filename_list:
        print(name)

if __name__ == '__main__':
    main()

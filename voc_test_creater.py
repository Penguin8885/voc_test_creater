import sys, os
import subprocess
import random
import datetime
import csv
import numpy as np

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

def convertWotdData2TexStyle(data):
    # 3単語ずつ分けてTexの様式の文字列を作成
    line_list = []
    for i in range(0, len(data), 3):
        w1 = data[i  ][0]
        w2 = data[i+1][0]
        w3 = data[i+2][0]
        if len(w1) >= 17:
            w1 = r'{\scriptsize ' + w1 + r'}'
        elif len(w1) >= 15:
            w1 = r'{\small ' + w1 + r'}'
        if len(w2) >= 17:
            w2 = r'{\scriptsize ' + w2 + r'}'
        elif len(w2) >= 15:
            w2 = r'{\small ' + w2 + r'}'
        if len(w3) >= 17:
            w3 = r'{\scriptsize ' + w3 + r'}'
        elif len(w3) >= 15:
            w3 = r'{\small ' + w3 + r'}'
        line = r'    \bf ' + w1 \
             + r' & \BS & \bf ' + w2 \
             + r' & \BS & \bf ' + w3 \
             + r' & \BS\\' + '\n'
        line_list.append(line)
    return line_list

def outputTeX(data):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_filename = './test' + now + '.tex'                  # 出力ファイル名
    tmp_filename = './tex_template/voc_test_template1.tex'  # テンプレートのファイル名

    with open(out_filename, mode='w',encoding="utf-8") as outf:
        with open(tmp_filename, mode='r',encoding="utf-8") as tmpf:
            for line in tmpf:
                if not r'%%%' in line:
                    outf.write(line)        # テンプレートの行をそのまま出力
                else:
                    for datum in data[:20]:
                        outf.write(datum)   # 問題データを出力
    return out_filename

def main(csv_filename, number):
    data = inputWordData(csv_filename)      # 英単語ファイル読み込み
    data = data[number:number+60]           # 英単語を選択
    random.shuffle(data)                    # シャッフル
    data = convertWotdData2TexStyle(data)   # 英単語をtex形式のレコードに変換
    out_filename = outputTeX(data)          # 英単語テストのtexファイルを生成
    rc = subprocess.call('sh ./tex_template/cc.sh ' + out_filename) # コンパイル，PDF作成

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))

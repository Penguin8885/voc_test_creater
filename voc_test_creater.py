import sys, os
import subprocess
import random
from time import sleep
import datetime
import csv
import numpy as np

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
    for datum in data:
        print(datum)
    return data

## texの文字サイズを修飾をする関数
def addModifierOfSize(w):
    if len(w) >= 17:
        return r'{\scriptsize ' + w + r'}'
    elif len(w) >= 15:
        return r'{\small ' + w + r'}'
    else:
        return w

## 単語データからtexスタイルの文章を生成する関数
def convertWotdData2TexStyle(data, ans):
    # 単語を3個のずつ分けてTexの様式の文字列を作成
    line_list = []

    if ans == False: # 問題文生成
        for i in range(0, len(data)-3, 3):
            # 最初は普通に3個ずつ分割して1行を生成
            w1 = addModifierOfSize(data[i+0][0])    # 単語データだけ読み出す
            w2 = addModifierOfSize(data[i+1][0])
            w3 = addModifierOfSize(data[i+2][0])
            line = r'    \bf ' + w1 \
                + r' & \BS & \bf ' + w2 \
                + r' & \BS & \bf ' + w3 \
                + r' & \BS\\' + '\n'
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
            line = r'    \bf ' + w1 \
                + r' & \BS & \bf ' + w2 \
                + r' & \BS & \bf ' + w3 \
                + r' & \BS\\' + '\n'
            line_list.append(line)
    else: # 答え生成
        print('not implemented')
        return None

    return line_list # 作成したtex形式の文のリストを返却

## 単語データをtexファイルとして出力するための関数
def createTeX(data, tex_template_file):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') # 現在時刻
    out_filename = './test' + now + '.tex'                  # 出力ファイル名
    tmp_filename = tex_template_file                        # テンプレートのファイル名

    # テンプレートを読み込んで，表のところだけ問題で置換する
    with open(out_filename, mode='w', encoding="utf-8") as outf:
        with open(tmp_filename, mode='r', encoding="utf-8") as tmpf:
            for line in tmpf:
                if not r'%%%' in line:      # テンプレートの表部分の目印が'%%%'となっています
                    outf.write(line)        # テンプレートの行をそのまま出力
                else:
                    for datum in data[:20]:
                        outf.write(datum)   # 問題データを出力
    return out_filename

## テストのPDFを生成
def createVoctestPDFs(data, dir_, ans=False):
    print('\n\n============ Creating PDF files ============')
    tex_filename_list = []  # 出力したファイル名のリスト
    template_file = './tex_template/voc_test_template1.tex' # texテンプレートファイル
    compile_sh_file = './tex_template/cc.sh'                # コンパイル用シェルスクリプト

    for i in range(0, len(data), 60):
        page_data = data[i:(i+60)]                          # 1ページ分の問題を取り出す
        tex_data = convertWotdData2TexStyle(page_data, ans) # 英単語をtex形式のレコードに変換
        tex_filename = createTeX(tex_data, template_file)   # 英単語テストtexファイル生成
        compile_cmd = 'sh ' + compile_sh_file + ' ' + tex_filename # コンパイルコマンド
        subprocess.call(compile_cmd)                        # コンパイル，PDF作成
        tex_filename_list.append(tex_filename)              # texファイル名を登録
        sleep(1)                                            # ファイル名重複防止用の1秒停止

    # 生成したPDFのファイル名のリストを生成
    pdf_filename_list = []    # 生成したpdfファイルのリスト
    for name in tex_filename_list:
        # ./abcde.tex から abcde を取り出してpdfファイル名に変更
        pdf_filename = dir_ + name[2:-4] + '.pdf'
        pdf_filename_list.append(pdf_filename)

    return pdf_filename_list # pdfファイル名のリストを返却

## pdf結合のための関数
def mergePDFs(pdf_filename_list, dir_):
    if len(pdf_filename_list) == 1:
        return  # マージする必要性が無いときはそのまま終了

    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')     # 現在時刻
    pdf_newname = dir_ + 'test' + now + '-merged.pdf'    # pdfファイル名
    # pdf_newname = dir_ + 'test' + now + 'ans-merged.pdf' # pdfファイル名(答え)

    try:
        from PyPDF2 import PdfFileMerger # ここでしか使用しないため，ここでインポート
        merger = PdfFileMerger()  # マージ機を立ち上げる
        for file_ in pdf_filename_list:
            merger.append(file_)  # PDFファイルを連結
        merger.write(pdf_newname) # 保存
        merger.close()            # マージ機を終了させる

        for pdf_filename in pdf_filename_list:
            subprocess.call('rm ' + pdf_filename) # 不必要なファイルを削除
        print('\nMerged -> ' + pdf_newname)         # 結果を表示

    except:
        # 結合に失敗したとき，全PDFを表示して終了
        print('Sorry, cloudn\'t merge')
        for file_ in pdf_filename_list:
            print(file_)


def main():
    csv_filename = printCsvSelectionScreen('./voccsv/') # CSV選択画面表示
    data = inputWordData(csv_filename)                  # 選択された英単語ファイル読み込み

    print('\nInput test info')
    top_index = int(input("単語先頭番号 : "))
    num       = int(input("問題数       : "))
    data = data[top_index:(top_index+num)]      # 英単語を選択
    # random.shuffle(data)                        # シャッフル

    pdf_files = createVoctestPDFs(data, './voctest/', ans=False)
    mergePDFs(pdf_files, './voctest/')

if __name__ == '__main__':
    main()

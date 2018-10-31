import sys, os
import csv

if __name__ == '__main__':
    # #csvファイル確認
    # csv_file = sys.argv[1]
    # if os.path.exists(csv_file) is False:
    #     if os.path.exitts('./' + csv_file) is False:
    #         print(sys.argv[1], 'does not exist')
    #         sys.exit(0)
    #     else:
    #         csv_file = './' + csv_file
    # else:
    #     pass

    # #csv読み込み
    # data = []
    # with open(csv_file) as f:
    #     reader = csv.reader(f)
    #     for i, row in enumerate(reader):
    #         data.append(row)
    #         print(i+1, row)

    data = []
    for csv_file in os.listdir('./'):
        if csv_file[-4:] == '.csv':
            print(csv_file)
            #csv読み込み
            with open(csv_file) as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    data.append(row)
                    print(i+1, row)
    print('total', len(data), 'words')



    while True:
        print('---- input word ----')
        str_ = input()
        if str_ == 'exit':
            break
        for datum in data:
            if str_ == datum[0]:
                print(datum)
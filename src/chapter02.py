from pathlib import Path
import argparse
import math
import numpy as np
from collections import Counter

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_data():
    path = DATA_DIR / 'hightemp.txt'
    with open(path, 'r') as rf:
        src = rf.read()
    return src


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=7)
    return parser.parse_args()


def task10():
    """10. 行数のカウント
    """
    src = load_data()
    dst = [s for s in src.split('\n') if s]
    print(len(dst))


def task11():
    """11. タブをスペースに置換
    """
    src = load_data()
    print(src.replace('\t', ' '))


def task12():
    """12. 1列目をcol1.txtに，2列目をcol2.txtに保存
    """
    src = load_data()
    col1 = '\n'.join([col.split('\t')[0] for col in src.split('\n') if col])
    col2 = '\n'.join([col.split('\t')[1] for col in src.split('\n') if col])
    output = Path(__file__).parent / 'output'
    col1txt = output / 'col1.txt'
    col2txt = output / 'col2.txt'
    with col1txt.open('w') as wf:
        wf.write(col1)
    with col2txt.open('w') as wf:
        wf.write(col2)
    with col1txt.open('r') as rf:
        print('col1:')
        print(rf.read())
    print()
    with col2txt.open('r') as rf:
        print('col2:')
        print(rf.read())


def task13():
    """13. col1.txtとcol2.txtをマージ
    """
    output = Path(__file__).parent / 'output'
    with open(output / 'col1.txt', 'r') as rf:
        col1 = rf.read().split('\n')
    with open(output / 'col2.txt', 'r') as rf:
        col2 = rf.read().split('\n')
    dst = '\n'.join(['\t'.join([word1, word2]) for word1, word2 in zip(col1, col2)])
    print(dst)


def task14():
    """14. 先頭からN行を出力
    """
    src = load_data()
    args = parse()
    dst = '\n'.join(src.split('\n')[:args.n])
    print(dst)


def task15():
    """15. 末尾のN行を出力
    """
    src = load_data()
    args = parse()
    dst = '\n'.join([col for col in src.split('\n') if col][-args.n:])
    print(dst)


def task16():
    """16. ファイルをN分割する
    """
    src = load_data()
    args = parse()
    src = [col for col in src.split('\n') if col]
    length = math.ceil(len(src) / args.n)
    for i in range(0, len(src), length):
        dst = '\n'.join(src[i:i + length])
        print(dst)
        print()


def task17():
    """17. １列目の文字列の異なり
    """
    src = load_data()
    col1 = [col.split('\t')[0] for col in src.split('\n') if col]
    dst = set(col1)
    print(dst)
    print('num of set:', len(dst))


def task18():
    """18. 各行を3コラム目の数値の降順にソート
    """
    src = load_data().split('\n')
    col3 = [float(col.split('\t')[2]) for col in src if col]
    dst = '\n'.join([src[i] for i in np.argsort(col3)])
    print(dst)


def task19():
    """19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
    """
    src = load_data().split('\n')
    col1 = [col.split('\t')[0] for col in src if col]
    hist = Counter(col1)
    # order = [word for word, _ in hist.most_common()]
    # dst = []
    # for word in order:
    #     [dst.append(col) for col in src if word in col]
    # dst = '\n'.join(dst)
    # print(dst)
    dst = [word for word, _ in hist.most_common()]
    print(dst)


if __name__ == '__main__':
    task19()

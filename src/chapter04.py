from pathlib import Path
import os
import MeCab
import re

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_data():
    src = DATA_DIR / 'neko.txt'
    if not src.exists():
        command = 'wget -O {} http://www.cl.ecei.tohoku.ac.jp/nlp100/data/neko.txt'.format(src)
        os.system(command)
    with open(src, 'r') as rf:
        data = rf.read()
    return data


def load_neko():
    src = DATA_DIR / 'neko.txt.mecab'
    if not src.exists():
        mecab = MeCab.Tagger("-Ochasen")
        data = mecab.parse(load_data())
        with open(src, 'w') as wf:
            wf.write(data)
        return data
    with open(src, 'r') as rf:
        data = rf.read()
    return data


def load_map():
    src = re.split('。.*\n', load_neko())
    src = [re.sub('、.*\n', '', line) for line in src]
    doc = []
    for sentence in src[:-1]:
        line_list = []
        for line in [line for line in sentence.split('\n') if line]:
            neko_map = {}
            line = re.split('\t', line)
            neko_map['surface'] = line[0]
            neko_map['base'] = line[2]
            neko_map['pos'] = line[3].split('-')[0]
            if len(line[3].split('-')) >= 2:
                neko_map['pos1'] = line[3].split('-')[1]
            else:
                neko_map['pos1'] = ''
            line_list.append(neko_map)
        doc.append(line_list)
    return doc


def task30():
    """30. 形態素解析結果の読み込み
    """
    dst = load_map()
    print(dst)


def task31():
    """31. 動詞
    """
    src = load_map()
    verbs = []
    for sentence in src:
        [verbs.append(word['surface']) for word in sentence if word['pos'] == '動詞']
    dst = set(verbs)
    print(dst)


def task32():
    """32. 動詞の原形
    """
    src = load_map()
    verbs = []
    for sentence in src:
        [verbs.append(word['base']) for word in sentence if word['pos'] == '動詞']
    dst = set(verbs)
    print(dst)


def task33():
    """33. サ変名詞
    """
    src = load_map()
    nouns = []
    for sentence in src:
        [nouns.append(word['base']) for word in sentence if word['pos1'] == 'サ変接続']
    dst = set(nouns)
    print(dst)


def task34():
    """34. 「AのB」
    """
    src = load_map()
    nphrases = []
    for sentence in src:
        [nphrases.append(''.join([word['base'], sentence[i + 1]['base'], sentence[i + 2]['base']]))
         for i, word in enumerate(sentence[:-2])
         if word['pos'] == '名詞' and sentence[i + 1]['base'] == 'の' and sentence[i + 2]['pos'] == '名詞']
    dst = set(nphrases)
    print(dst)


def task35():
    """35. 名詞の連接
    """
    src = load_map()
    nstream = []
    for sentence in src:
        block = []
        for word in sentence:
            if word['pos'] != '名詞':
                word['base'] = ' '
            block.append(word['base'])
        nstream.append(''.join(block).split(' '))
    dst = []
    for sentence in nstream:
        [dst.append(nouns) for nouns in sentence if nouns]
    dst = set(dst)
    print(dst)


if __name__ == '__main__':
    task35()

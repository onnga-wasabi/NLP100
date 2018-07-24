from pathlib import Path
import os
import re
from nltk.stem.porter import PorterStemmer
import xml.etree.ElementTree as ET
import pydot
import numpy as np

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_data():
    src = DATA_DIR / 'nlp.txt'
    if not src.exists():
        command = 'wget -O {} http://www.cl.ecei.tohoku.ac.jp/nlp100/data/nlp.txt'.format(src)
        os.system(command)
    with open(src, 'r') as rf:
        data = rf.read()
    return data


def load_xml(path=True):
    src = DATA_DIR / 'nlp.txt.xml'
    if path:
        return src
    with open(src, 'r') as rf:
        data = rf.read()
    return data


def task50(main=False):
    """50. 文区切り
    """
    src = load_data()
    lines = re.findall('[A-Z].+?[.;:?!]\s', re.sub('\n', '', src))
    dst = '\n'.join(lines)
    if main:
        print(dst)
    return dst


def task51(main=False):
    """51. 単語の切り出し
    """
    src = task50()
    words = []
    append = words.append
    for line in src.split('\n'):
        append('\n'.join([w for w in line.split(' ')]))
    dst = '\n'.join(words)
    if main:
        print(dst)
    return dst


def task52():
    """52. ステミング
    """
    src = task51()
    st = PorterStemmer()
    for word in src.split('\n'):
        word = re.sub('[.,()]', '', word)
        line = word + '\t' + st.stem(word)
        print(line)


def task53():
    """53. Tokenization
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    words = [word.text for word in root.iter('word') if word.text not in [',', '.']]
    for word in words[:30]:
        print(word)


def task54():
    """54. 品詞タグ付け
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    words = []
    append = words.append
    for token in root.iter('token'):
        for w, l, p in zip(token.iter('word'), token.iter('lemma'), token.iter('POS')):
            append({
                'word': w.text,
                'lemma': l.text,
                'pos': p.text,
            })
    for word in words[:30]:
        print('\t'.join([word['word'], word['lemma'], word['pos']]))


def task55():
    """55. 固有表現抽出
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    persons = []
    append = persons.append
    for t in root.iter('token'):
        for w, n in zip(t.iter('word'), t.iter('NER')):
            if n.text == 'PERSON':
                append(w.text)
    for p in persons:
        print(p)


def task56():
    """56. 共参照解析
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    coreferences = root.find('document').find('coreference')
    coreference = []
    append = coreference.append
    for c in coreferences.findall('coreference'):
        for m in [m for m in c.iter('mention') if not m.get('representative')]:
            append((m, c.find('mention')))
    lines = []
    append = lines.append
    for s in [s for s in root.iter('sentence') if s.get('id')]:
        append([t.find('word').text for t in s.find('tokens').findall('token')])

    document = []
    append = document.append
    for i, s in enumerate([s for s in root.iter('sentence') if s.get('id')]):
        replace = [c for c in coreference if i + 1 == int(c[0].find('sentence').text)]
        if replace:
            for c in replace:
                # 代表表現
                ref_sentence = lines[int(c[1].find('sentence').text) - 1]
                ref_start = int(c[1].find('start').text) - 1
                ref_end = int(c[1].find('end').text) - 1

                # 元表現
                org_start = int(c[0].find('start').text) - 1
                org_end = int(c[0].find('end').text) - 1
                line = '[' + ' '.join(ref_sentence[ref_start:ref_end]) + ']' + ' ' +\
                    '(' + ' '.join(lines[i][org_start:org_end]) + ')'
                lines[i][org_start] = line
        line = ' '.join(lines[i])
        append(line)

    for d in document:
        print(d)


def task57():
    """57. 係り受け解析
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    i = 0
    for d in root.iter('dependencies'):
        if d.get('type') == 'collapsed-dependencies':
            g = pydot.Dot(graph_type='digraph')
            for c in d.findall('dep'):
                g.add_node(pydot.Node(c.find('governor').get('idx'), label=c.find('governor').text))
                g.add_node(pydot.Node(c.find('dependent').get('idx'), label=c.find('dependent').text))
                g.add_edge(pydot.Edge(c.find('governor').get('idx'), c.find('dependent').get('idx')))
            g.write_png('output/snc/{}.png'.format(i))
            i += 1


def task58():
    """58. タプルの抽出
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    dst = []
    for d in root.iter('dependencies'):
        if d.get('type') == 'collapsed-dependencies':
            predicates = {c.find('governor').text: {} for c in d.findall('dep')}
            for c in d.findall('dep'):
                key = c.find('governor').text
                if c.get('type') == 'nsubj':
                    predicates[key]['sub'] = c.find('dependent').text
                elif c.get('type') == 'dobj':
                    predicates[key]['obj'] = c.find('dependent').text
            blocks = [(k, v) for k, v in predicates.items() if 'sub' in v.keys() and 'obj' in v.keys()]
            if blocks:
                for b in blocks:
                    dst.append('\t'.join([b[1]['sub'], b[0], b[1]['obj']]))
    for d in dst:
        print(d)


def getNP(p):
    NP = []
    words = []
    state = 0
    for idx, s in enumerate(p[:-2]):
        if s + p[idx + 1] + p[idx + 2] != '(NP':
            continue
        for ss in p[idx:]:
            if ss == '(':
                state -= 1
                words.append(ss)
            elif ss == ')':
                state += 1
            else:
                words.append(ss)
            if state == 0:
                words = ''.join(words)
                words = [w for w in words.split(' ') if '(' not in w]
                break
        NP.append(' '.join(words))
        words = []
    return NP


def task59():
    """59. S式の解析
    """
    src = load_xml()
    tree = ET.parse(src)
    root = tree.getroot()
    NPs = []
    for s in root.find('document').find('sentences').findall('sentence'):
        p = s.find('parse').text
        NPs.append(getNP(p))

    for NP in NPs:
        for words in NP:
            print(words)


if __name__ == '__main__':
    # task50(True)
    # task51(True)
    task59()

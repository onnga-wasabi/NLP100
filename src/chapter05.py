from pathlib import Path
import os
import pydot

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
    src = DATA_DIR / 'neko.txt.cabocha'
    if not src.exists():
        command = 'cabocha {} -f1 > {}'.format(DATA_DIR / 'neko.txt', src)
        os.system(command)
    with open(src, 'r') as rf:
        data = rf.read()
    return data


class Morph(object):
    """形態素を表すクラスMorphを実装せよ．このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をメンバ変数に持つ
    """

    def __init__(self, word):
        self.word = word
        self.parse()

    def __str__(self):
        return 'surface:{} base:{} pos:{} pos1:{}'.format(self.surface, self.base, self.pos, self.pos1)

    def parse(self):
        self.surface = self.word.split('\t')[0]
        self.base = self.word.split(',')[-3]
        self.pos = self.word.split(',')[0].split('\t')[1]
        self.pos1 = self.word.split(',')[1]
        # self.pos1 = self.word.split(',')[1].split('／')[0].strip('*')


class Chunk(object):
    """形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つ
    """

    def __init__(self, phrase):
        self.phrase = [p for p in phrase.split('\n') if p]
        self.parse()
        self.chunk = ''.join([m.surface for m in self.morphs if m.pos != '記号'])

    def __str__(self):
        return '{}:{} srcs:{} dst:{}'.format(self.idx, ''.join([m.surface for m in self.morphs]), self.srcs, self.dst)

    def parse(self):
        self.idx = self.phrase[0].split(' ')[0]
        self.dst = self.phrase[0].split(' ')[1][:-1]
        self.morphs = [Morph(p) for p in self.phrase[1:]]

    def set_src(self, srcs):
        self.srcs = srcs


def task40():
    """40. 係り受け解析結果の読み込み（形態素）
    """
    src = load_neko()
    document = []
    for s in src.split('EOS'):
        if s is not '\n':
            sentence = []
            [[sentence.append(str(Morph(line))) for line in phrase.split('\n')[1:] if line]
             for phrase in s.split('* ')[1:]]
            document.append(sentence)
    print('\n'.join(document[2]))


def task41():
    """41. 係り受け解析結果の読み込み（文節・係り受け)
    """
    src = load_neko()
    document = []
    for s in src.split('EOS'):
        if s is not '\n':
            chunks = [Chunk(phrase) for phrase in s.split('* ')[1:]]
            for phrase in chunks:
                phrase.set_src([int(c.idx) for c in chunks if phrase.idx == c.dst])
            document.append(chunks)
    for chunk in document[5]:
        print(chunk)


def task42():
    """42. 係り元と係り先の文節の表示
    """
    src = load_neko()
    document = []
    for s in src.split('EOS'):
        if s is not '\n':
            chunks = [Chunk(phrase) for phrase in s.split('* ')[1:]]
            for phrase in chunks:
                phrase.set_src([int(c.idx) for c in chunks if phrase.idx == c.dst])
            document.append(chunks)
    lines = []
    for chunks in document:
        for chunk in chunks:
            srcs = [c for c in chunks if int(c.idx) in chunk.srcs]
            srcs = [''.join([m.surface for m in c.morphs if m.pos != '記号']) for c in srcs]
            dst = ''.join([m.surface for m in chunk.morphs if m.pos != '記号'])
            for src in [s for s in srcs if s]:
                lines.append('\t'.join([src, dst]))
    print(lines[:10])


def task43():
    """43. 名詞を含む文節が動詞を含む文節に係るものを抽出
    """
    src = load_neko()
    document = []
    for s in src.split('EOS'):
        if s is not '\n':
            chunks = [Chunk(phrase) for phrase in s.split('* ')[1:]]
            for phrase in chunks:
                phrase.set_src([int(c.idx) for c in chunks if phrase.idx == c.dst])
            document.append(chunks)
    lines = []
    for chunks in document:
        for chunk in chunks:
            srcs = [c for c in chunks if int(c.idx) in chunk.srcs]
            srcs = [''.join([m.surface for m in c.morphs if m.pos != '記号'])
                    for c in srcs if '名詞' in [m.pos for m in c.morphs]]
            dst = ''.join([m.surface for m in chunk.morphs if m.pos != '記号' and '動詞' in [m.pos for m in chunk.morphs]])
            if dst:
                for src in [s for s in srcs if s]:
                    lines.append('\t'.join([src, dst]))
    print('\n'.join(lines[:10]))


def task44():
    """44. 係り受け木の可視化
    """
    src = load_neko()
    s = src.split('EOS')[8]
    chunks = [Chunk(phrase) for phrase in s.split('* ')[1:]]
    for phrase in chunks:
        phrase.set_src([int(c.idx) for c in chunks if phrase.idx == c.dst])

    # graphviz ==========
    # lines = []
    # for chunk in chunks:
    #     srcs = [c for c in chunks if int(c.idx) in chunk.srcs]
    #     srcs = [''.join([m.surface for m in c.morphs if m.pos != '記号']) for c in srcs]
    #     dst = ''.join([m.surface for m in chunk.morphs if m.pos != '記号'])
    #     for src in [s for s in srcs if s]:
    #         lines.append(' -> '.join([src, dst]))
    # content = ';\n'.join(lines)
    # graph = 'digraph graphname {' + content + '}'
    # with open('output/out.dot', 'w') as wf:
    #     wf.write(graph)
    # command = 'dot -T png output/out.dot -o output/graphviz.png'
    # os.system(command)
    # end of graphviz ===

    # pydot ============
    edges = []
    for chunk in chunks:
        srcs = [c for c in chunks if int(c.idx) in chunk.srcs]
        srcs = [''.join([m.surface for m in c.morphs if m.pos != '記号']) for c in srcs]
        dst = ''.join([m.surface for m in chunk.morphs if m.pos != '記号'])
        for src in [s for s in srcs if s]:
            edges.append((src, dst))
    graph = pydot.graph_from_edges(edges, directed=True)
    graph.write_png('output/pydot.png')
    # end pydot ========


def task45():
    """45. 動詞の格パターンの抽出
    """
    src = load_neko()
    document = []
    for s in src.split('EOS'):
        if s is not '\n':
            chunks = [Chunk(phrase) for phrase in s.split('* ')[1:]]
            for phrase in chunks:
                phrase.set_src([int(c.idx) for c in chunks if phrase.idx == c.dst])
            document.append(chunks)
    lines = []
    for chunks in document:
        for chunk in chunks:
            if chunk.morphs[0].pos == '動詞':
                dst = chunk.morphs[0].base
                for c in [c for c in chunks if int(c.idx) in chunk.srcs]:
                    cases = [m.base for m in c.morphs if m.pos == '助詞']
                if cases:
                    lines.append('\t'.join([dst, ' '.join(cases)]))
    with open('output/case_pattern.txt', 'w') as wf:
        wf.write('\n'.join(lines))


if __name__ == '__main__':
    task45()

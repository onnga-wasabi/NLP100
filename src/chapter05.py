from pathlib import Path
import os
import pydot
import numpy as np

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
        self.idx = int(self.phrase[0].split(' ')[0])
        self.dst = int(self.phrase[0].split(' ')[1][:-1])
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
            verbs = [m for m in chunk.morphs if m.pos == '動詞']
            if verbs:
                dst = verbs[0].base
                srcs = []
                for c in [c for c in chunks if int(c.idx) in chunk.srcs]:
                    src = [m.base for m in c.morphs if m.pos == '助詞']
                    if src:
                        srcs.append(src[-1])
                if srcs:
                    lines.append('\t'.join([dst, ' '.join(sorted(srcs))]))
    with open('output/case_pattern.txt', 'w') as wf:
        wf.write('\n'.join(lines))


def task46():
    """46. 動詞の格フレーム情報の抽出
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
            verbs = [m for m in chunk.morphs if m.pos == '動詞']
            if verbs:
                dst = verbs[0].base
                srcs = []
                c_srcs = []
                for c in [c for c in chunks if int(c.idx) in chunk.srcs]:
                    src = [m.base for m in c.morphs if m.pos == '助詞']
                    if src:
                        srcs.append(src[-1])
                        c_srcs.append(''.join([m.base for m in c.morphs]))
                if srcs and c_srcs:
                    lines.append('\t'.join([dst, ' '.join(sorted(srcs)), ' '.join(sorted(c_srcs))]))
    with open('output/case_frame.txt', 'w') as wf:
        wf.write('\n'.join(lines))


def task47():
    """47. 機能動詞構文のマイニング
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
            verbs = [m for m in chunk.morphs if m.pos == '動詞']
            if verbs:
                for c in [c for c in chunks if int(c.idx) in chunk.srcs]:
                    morphs = c.morphs
                    sahen = [''.join([m.surface, morphs[i + 1].surface])
                             for i, m in enumerate(morphs[:-1])
                             if m.pos == '名詞' and m.pos1 == 'サ変接続' and
                             morphs[i + 1].surface == 'を' and morphs[i + 1].pos == '助詞']
                if sahen:
                    dst = sahen[0] + verbs[0].base
                    srcs = []
                    c_srcs = []
                    for c in [c for c in chunks if int(c.idx) in chunk.srcs]:
                        if not sahen[0] in ''.join([m.surface for m in c.morphs]):
                            src = [m.base for m in c.morphs if m.pos == '助詞']
                            if src:
                                srcs.append(src[-1])
                                c_srcs.append(''.join([m.surface for m in c.morphs]))
                    if srcs and c_srcs:
                        idx = np.argsort(srcs)
                        srcs = np.array(srcs)
                        c_srcs = np.array(c_srcs)
                        lines.append('\t'.join([dst, ' '.join(srcs[idx]), ' '.join(c_srcs[idx])]))
    with open('output/mining.txt', 'w') as wf:
        wf.write('\n'.join(lines))


def get_path_to_root(chunk, chunks, path=''):
    surface = ''.join([m.surface for m in chunk.morphs if m.pos != '記号'])
    if int(chunk.dst) == -1:
        return path + surface
    else:
        dst = [c for c in chunks if c.idx == chunk.dst]
        path = path + surface + ' -> '
        return get_path_to_root(dst[0], chunks, path=path)


def task48():
    """48. 名詞から根へのパスの抽出
    """
    src = load_neko()
    document = []
    for s in src.split('EOS'):
        if s is not '\n':
            chunks = [Chunk(phrase) for phrase in s.split('* ')[1:]]
            for phrase in chunks:
                phrase.set_src([int(c.idx) for c in chunks if phrase.idx == c.dst])
            document.append(chunks)
    paths_to_root = []
    for chunks in document:
        for chunk in [c for c in chunks if '名詞' in [m.pos for m in c.morphs]]:
            paths_to_root.append(get_path_to_root(chunk, chunks))

    for ptr in paths_to_root[:30]:
        print(ptr)


def get_path_before_root(chunk, chunks, val, path=''):
    if path == '':
        surface = [m.surface for m in chunk.morphs if m.pos != '記号']
        surface[0] = val
        surface = ''.join(surface)
    else:
        surface = ''.join([m.surface for m in chunk.morphs if m.pos != '記号'])
    if chunk.dst == -1:
        return path
    else:
        if chunks[chunk.dst].dst == -1:
            return path + surface + ' | '
        path = path + surface + ' -> '
        return get_path_before_root(chunks[chunk.dst], chunks, val, path=path)


def get_path_A_to_B(chunk, chunks, idx, path=''):
    if path == '':
        surface = [m.surface for m in chunk.morphs if m.pos != '記号']
        surface[0] = 'X'
        surface = ''.join(surface)
    else:
        surface = ''.join([m.surface for m in chunk.morphs if m.pos != '記号'])
    if chunk.idx == idx:
        return path + 'Y'
    else:
        path = path + surface + ' -> '
        return get_path_A_to_B(chunks[chunk.idx + 1], chunks, idx, path=path)


def task49():
    """49. 名詞間の係り受けパスの抽出
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
    append = lines.append
    for chunks in document[:8]:
        noun_chunks = [c for c in chunks if '名詞' in [m.pos for m in c.morphs]]
        for i, nc1 in enumerate(noun_chunks):
            for nc2 in noun_chunks[i + 1:]:
                # print(nc1.chunk, chunks[nc1.dst].chunk)
                if nc1.dst > nc2.idx:
                    append(get_path_before_root(nc1, chunks, 'X') +
                           get_path_before_root(nc2, chunks, 'Y') +
                           chunks[nc1.dst].chunk)
                else:
                    append(get_path_A_to_B(nc1, chunks, nc2.idx))

    for line in lines[: 30]:
        print(line)


if __name__ == '__main__':
    task49()

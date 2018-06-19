import argparse
import random


def task00():
    src = 'stressed'
    dst = src[::-1]
    print(dst)


def task01():
    src = 'パタトクカシーー'
    dst = src[1::2]
    print(dst)


def task02():
    src1 = 'パトカー'
    src2 = 'タクシー'
    dst = ''
    for p, t in zip(src1, src2):
        dst += p
        dst += t
    print(dst)


def task03():
    src = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
    word_list = src.replace(',', '').replace('.', '').split()
    dst = [len(word) for word in word_list]
    print(dst)


def task04():
    src = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. \
        New Nations Might Also Sign Peace Security Clause. Arthur King Can.'
    idx = [1, 5, 6, 7, 8, 9, 15, 16, 19]
    word_list = src.replace(',', '').replace('.', '').split()
    dst_dict = {}
    for i, word in enumerate(word_list):
        num = i + 1
        if num in idx:
            dst_dict[word[:1]] = num
        else:
            dst_dict[word[:2]] = num

    print(dst_dict.items())


def task05():
    src = 'I am an NLPer'
    word_list = src.split()
    word_bigram = [''.join([word_list[idx], word_list[idx + 1]]) for idx, _ in enumerate(word_list[:-1])]
    print('Word biragram:', word_bigram)

    char_stream = ''.join(src.split())
    char_bigram = [''.join([char_stream[idx], char_stream[idx + 1]]) for idx, _ in enumerate(char_stream[:-1])]
    print('Charactor biragram:', char_bigram)


def task06():
    src1 = 'paraparaparadise'
    src2 = 'paragraph'
    X = [''.join([src1[idx], src1[idx + 1]]) for idx, _ in enumerate(src1[:-1])]
    Y = [''.join([src2[idx], src2[idx + 1]]) for idx, _ in enumerate(src2[:-1])]
    print('X:', X)
    print('Y:', Y)
    print('Union X,Y:', set(X) | set(Y))
    print('Intersection X,Y:', set(X) & set(Y))
    print('Difference X,Y:', set(X) - set(Y))

    msg = 'X dosen\'t have se'
    if 'se' in X:
        msg = 'X has se'
    print(msg)

    msg = 'Y dosen\'t have se'
    if 'se' in Y:
        msg = 'Y has se'
    print(msg)


def task07():
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('--x', type=float, default=12)
        parser.add_argument('--y', default='気温')
        parser.add_argument('--z', type=float, default=22.4)
        return parser.parse_args()

    args = parse()
    dst = '{}時の{}は{}'.format(args.x, args.y, args.z)
    print(dst)


def task08():
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('--src', default='I am a student, 21 years old!')
        return parser.parse_args()

    def code(src):
        encoded = []
        for s in src:
            if s.islower():
                s = chr(219 - ord(s))
            encoded.append(s)
        return ''.join(encoded)

    args = parse()
    dst = code(args.src)
    print('Encoded:', dst)
    dst = code(dst)
    print('Decoded:', dst)


def task09():
    src = 'I couldn\'t believe that I could actually understand\
        what I was reading : the phenomenal power of the human mind .'
    dst = []
    for word in src.split():
        if len(word) >= 4:
            tmp = word
            word = []
            word.append(tmp[0])
            word.append(''.join(random.sample(tmp[1:-1], len(tmp[1:-1]))))
            word.append(tmp[-1])
            word = ''.join(word)
        dst.append(word)
    dst = ' '.join(dst)
    print(dst)


if __name__ == '__main__':
    task09()

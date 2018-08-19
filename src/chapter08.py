from pathlib import Path
import os
import random
import re
from nltk.stem import PorterStemmer
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_data():
    src = DATA_DIR / 'rt-polaritydata'
    if not src.exists():
        archive = DATA_DIR / 'rt-polaritydata.tar.gz'
        command = 'wget -O {} http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz; \
        tar -zxvf {} -C {}'.format(archive, archive, src.resolve().parent)
        os.system(command)

    data = {}
    with open(src / 'rt-polarity.pos', 'rb') as rf:
        data['pos'] = rf.read()
    with open(src / 'rt-polarity.neg', 'rb') as rf:
        data['neg'] = rf.read()
    return data


def load_stop_words():
    src = DATA_DIR / 'ranksnl_oldgoogle.txt'
    if not src.exists():
        command = 'wget -O {} https://raw.githubusercontent.com/igorbrigadir/stopwords/master/en/ranksnl_oldgoogle.txt'.format(
            src)
        os.system(command)
    stop_words = []
    with open(src, 'r') as rf:
        for line in rf:
            stop_words.append(line.strip())
    return stop_words


def is_stop_word(word):
    return word in load_stop_words()


def load_txt():
    src = DATA_DIR / 'sentiment.txt'
    if not src.exists():
        task70()
    with open(src, 'r') as rf:
        sentiment = rf.read()
    return sentiment


class LogisticRegression(object):
    def __init__(self, data, seed=1):
        self.X, self.Y = self.preprocess(data)
        self.init_wait()

    def init_wait(self):
        self.w = np.random.randn(len(self.X[0]) + 1)

    def fit(self, X, Y, epoch=3, init=False):
        self.X = X
        self.Y = Y
        if init:
            self.init_wait()
        for _ in range(epoch):
            idx = np.random.permutation(len(self.X))
            loss = 0
            for x, y in zip(self.X[idx], self.Y[idx]):
                y_pred = self.predict(x)
                loss = y - y_pred
                self.update_weights(loss, x)

    def update_weights(self, loss, x, alpha=1):
        self.w += alpha * loss * np.insert(x, 0, 1)

    def predict(self, x):
        x = np.insert(x, 0, 1)
        return self.sigmoid(np.dot(self.w, x))

    def predict_label(self, x, threshold=0.5):
        return "+1" if self.predict(x) >= threshold else "-1"

    @classmethod
    def preprocess(self, data):
        all_words = []
        [[all_words.append(word) for word in line[0]] for line in data]
        self.all_words = sorted(list(set(all_words)))
        X, Y = [], []
        for line in data:
            Y.append(1 if int(line[1]) > 0 else 0)
            cnt = Counter(line[0])
            x = [cnt[key] if key in cnt.keys() else 0 for key in self.all_words]
            X.append(x)
        return np.array(X), np.array(Y)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))


def task70():
    """70. データの入手・整形
    """
    src = DATA_DIR / 'sentiment.txt'
    if not src.exists():
        data = load_data()
        sentiments = []
        append = sentiments.append
        for line in [l for l in data['pos'].decode(errors='replace').split('\n') if l]:
            append('+1 ' + line)
        for line in [l for l in data['neg'].decode(errors='replace').split('\n') if l]:
            append('-1 ' + line)
        random.shuffle(sentiments)
        with open(src, 'w') as wf:
            wf.write('\n'.join(sentiments))

    with open(src, 'r') as rf:
        sentiment = rf.read()
    pos = list(filter(lambda x: x.split(' ')[0] == '+1', sentiment.split('\n')))
    neg = list(filter(lambda x: x.split(' ')[0] == '-1', sentiment.split('\n')))
    print('pos: {}, neg: {}'.format(len(pos), len(neg)))


def task71():
    """71. ストップワード
    """
    print('about:', is_stop_word('about'))
    print('good:', is_stop_word('good'))


def task72(main=False):
    """72. 素性抽出
    """
    stemmer = PorterStemmer()
    src = load_txt()
    data = []
    append = data.append
    for line in src.split('\n'):
        line = re.sub('[,.() /]', ' ', line)
        polarity = [stemmer.stem(word).lower() for word in line.split(' ')[1:] if not is_stop_word(word) and word]
        label = line.split(' ')[0]
        append((polarity, label))

    if main:
        print(data)
    else:
        return data


def task73():
    """73.学習
    """
    data = task72()
    lr = LogisticRegression(data)
    lr.fit()


def task74():
    """74.予測
    """
    data = task72()
    lr = LogisticRegression(data)
    lr.fit()
    for i in range(10):
        print(lr.Y[i], lr.predict_label(lr.X[i]))


def task75():
    """75. 素性の重み
    """
    data = task72()
    lr = LogisticRegression(data)
    lr.fit()
    high = np.argsort(np.abs(lr.w[1:]))[:10]
    low = np.argsort(np.abs(lr.w[1:]))[-10:]
    print([(lr.all_words[i], lr.w[i + 1].round(4)) for i in high])
    print()
    print([(lr.all_words[i], lr.w[i + 1].round(4)) for i in low])


def task76():
    """76. ラベル付け
    """
    data = task72()
    lr = LogisticRegression(data)
    lr.fit()
    result = []
    for x, y in zip(lr.X, lr.Y):
        y = '+1' if y > 0.5 else '-1'
        line = '{}\t{}\t{}'.format(y, lr.predict_label(x), lr.predict(x))
        result.append(line)
    return result


def task77():
    """77. 正解率の計測
    """
    result = task76()
    p = '+1'
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for line in result:
        y = line.split('\t')[0]
        y_pred = line.split('\t')[1]
        if y == p:
            if y_pred == p:
                tp += 1
            else:
                fp += 1
        else:
            if y_pred == p:
                fn += 1
            else:
                tn += 1
    acc = (tp + tn) / len(result)
    pre = tp / (tp + fp)
    rec = tp / (tp + fn)
    f_1 = 2 / ((1 / pre) + (1 / rec))
    print('accuracy:', acc)
    print('precision:', pre)
    print('recall:', rec)
    print('F1-score:', f_1)


def task78():
    """78. 5分割交差検定
    """
    data = task72()
    lr = LogisticRegression(data)
    X, Y = lr.X, lr.Y
    pxs = np.array(np.array_split(X, 5))
    pys = np.array(np.array_split(Y, 5))
    acc_all = 0
    for i in range(5):
        idx = np.ones(5, dtype=bool)
        idx[i] = False
        lr.fit(np.concatenate(pxs[idx], axis=0), np.concatenate(pys[idx], axis=0), init=True)
        acc = 0
        for x, y in zip(pxs[i], pys[i]):
            y_pred = 1 if lr.predict(x) > 0.5 else 0
            if y == y_pred:
                acc += 1
        print('acc', acc / len(pxs[i]))
        acc_all += acc
    print('acc all', acc_all / len(X))


def task79():
    """79. 適合率-再現率グラフの描画
    """
    accs = []
    pres = []
    recs = []
    data = task72()
    lr = LogisticRegression(data)
    X, Y = lr.X, lr.Y
    pxs = np.array(np.array_split(X, 5))
    pys = np.array(np.array_split(Y, 5))
    lr.fit(np.concatenate(pxs[:-1], axis=0), np.concatenate(pys[:-1], axis=0))
    for threshold in np.linspace(0, 1, 100):
        result = []
        for x, y in zip(pxs[-1], pys[-1]):
            y = '+1' if y > 0 else '-1'
            line = '{}\t{}\t{}'.format(y, lr.predict_label(x, threshold), lr.predict(x))
            result.append(line)
        p = '+1'
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for line in result:
            y = line.split('\t')[0]
            y_pred = line.split('\t')[1]
            if y == p:
                if y_pred == p:
                    tp += 1
                else:
                    fp += 1
            else:
                if y_pred == p:
                    fn += 1
                else:
                    tn += 1
        accs.append((tp + tn) / len(result))
        pres.append(tp / (tp + fp))
        recs.append(tp / (tp + fn))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(np.linspace(0, 1, 100), pres, label='Precision')
    ax.plot(np.linspace(0, 1, 100), recs, label='Recall')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    task79()

from pathlib import Path
import os
import gzip
import json
import pickle
import redis
from pymongo import MongoClient

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_artist():
    src1 = DATA_DIR / 'artist.pkl'
    if not src1.exists():
        src2 = DATA_DIR / 'artist.json.gz'
        if not src2.exists():
            command = 'wget -O {} http://www.cl.ecei.tohoku.ac.jp/nlp100/data/artist.json.gz'.format(src2)
            os.system(command)
        data = []
        append = data.append
        with gzip.open(src2, 'r') as rf:
            for line in rf:
                append(json.loads(line))
        with open(src1, 'wb') as wf:
            pickle.dump(data, wf)
    else:
        with open(src1, 'rb') as rf:
            data = pickle.load(rf)
    return data


def task60(init=False):
    """60. KVSの構築

    redis-server　起動しておいてねー
    """
    src = load_artist()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    if init:
        for line in src:
            if not line.get('area'):
                area = None
            else:
                area = line['area']
            r.set(line['name'], area)
    return r


def task61():
    """61. KVSの検索
    """
    r = task60()
    print(r.get('Oasis'))


def task62():
    """62. KVS内の反復処理
    """
    r = task60()
    dst = len([k for k in r.keys() if r.get(k) == b'Japan'])
    print(dst)


def task63(init=False):
    """63. オブジェクトを値に格納したKVS
    """
    src = load_artist()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
    r = redis.StrictRedis(connection_pool=pool)
    if init:
        r.flushall()
        for line in src:
            if not line.get('tags'):
                tags = []
            else:
                tags = line['tags']
            [r.set(line['name'], tag) for tag in tags]
    q = 'Rod Jones'
    tags = [eval(r.get(q).decode())]
    dst = 'アーティスト名: {}\ntags:'.format(q)
    for tag in tags:
        dst += '\n  {}:\t{}'.format(tag['value'], tag['count'])
    print(dst)


def task64(init=False):
    """64. MongoDBの構築
    server 起動しておいてね
    """
    client = MongoClient()
    db = client.nlp
    co = db.artists
    if init:
        db.artists.drop()
        src = load_artist()
        co.insert(src)
        co.create_index('name')
        co.create_index('aliases.name')
        co.create_index('tags.value')
        co.create_index('rating.value')


def task65():
    """65. MongoDBの検索
    """
    client = MongoClient()
    db = client.nlp
    co = db.artists
    dst = co.find({'name': 'Queen'})
    for d in dst:
        print(d)


def task66():
    """66. 検索件数の取得
    """
    client = MongoClient()
    db = client.nlp
    co = db.artists
    dst = co.find({'area': 'Japan'}).count()
    print(dst)


def task67():
    """67. 複数のドキュメントの取得
    """
    client = MongoClient()
    db = client.nlp
    co = db.artists
    dst = co.find({'aliases.name': '女王'})
    for d in dst:
        print(d)


def task68():
    """68. ソート
    """
    client = MongoClient()
    db = client.nlp
    co = db.artists
    dances = co.find({'tags.value': 'dance'})
    dst = sorted([d for d in dances if d.get('rating')], key=lambda x: x['rating']['count'], reverse=True)[:10]
    for d in dst:
        print(d['name'])


# web app #
from flask import (
    Flask,
    render_template,
    request,
)
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def artists():
    if request.method == 'POST':
        query = {
            'name': request.form['name'],
            'aliases.name': request.form['alias'],
            'tags.value': request.form['tag'],

        }
        if not query.values():
            return render_template('index.html')
        content = {
            'msg': '検索結果よー',
            'artists': [],
        }
        client = MongoClient()
        db = client.nlp
        co = db.artists
        query = {k: v for k, v in query.items() if v}
        results = co.find(query)
        tmp = []
        append = tmp.append
        for data in results:
            if not data.get('rating'):
                data['rating'] = {}
                data['rating']['count'] = 0
            append(data)
        results = tmp
        content['artists'] = sorted([d for d in results], key=lambda x: x['rating']['count'], reverse=True)
        return render_template('index.html', content=content)
    return render_template('index.html')


def task69():
    """69. Webアプリケーションの作成
    """
    app.run()


if __name__ == '__main__':
    task69()

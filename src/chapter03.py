from pathlib import Path
import os
import gzip
import json
import re
import requests

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_data():
    src = DATA_DIR / 'jawiki-country.json.gz'
    if not src.exists():
        command = 'wget -O {} http://www.cl.ecei.tohoku.ac.jp/nlp100/data/jawiki-country.json.gz'.format(src)
        os.system(command)
    with gzip.open(src, 'r') as rf:
        data = [json.loads(line) for line in rf]
    return data


def load_uk():
    src = load_data()
    dst = [line for line in src if 'イギリス' in line['title']]
    return dst[0]['text']


def json_search(data, key):
    """jsonデータを再帰的に目的のkeyを検索する
    """
    content = None
    for k in data:
        if k == key:
            return data[key]
        elif isinstance(data[k], list):
            for d in data[k]:
                content = json_search(d, key)
        elif isinstance(data[k], dict):
            content = json_search(data[k], key)
        if content is not None:
            break
    return content


def task20():
    """20. JSONデータの読み込み
    """
    dst = load_uk()
    print(dst)


def task21():
    """21. カテゴリ名を含む行を抽出
    """
    src = load_uk().split('\n')
    dst = [line for line in src if 'Category' in line]
    print(dst)


def task22():
    """22. カテゴリ名の抽出
    """
    src = load_uk().split('\n')
    lines = [line for line in src if 'Category' in line]
    dst = [re.sub('Category:', '', line.strip('[').strip(']')) for line in lines]
    print(dst)


def task23():
    """23. セクション構造
    """
    src = load_uk().split('\n')
    dst = {}
    for line in src:
        if '==' in line:
            name = line.strip('=')
            level = line.count('=') // 2 - 1
            dst[name] = level
    print(dst)


def task24():
    """24. ファイル参照の抽出
    """
    src = load_uk().split('\n')
    dst = []
    for line in src:
        if 'File' in line or 'ファイル' in line:
            line = re.sub('.*File:', '', line)
            line = re.sub('.*ファイル:', '', line)
            dst.append(re.sub('\|.*', '', line))
    print(dst)


def task25():
    """25. テンプレートの抽出
    """
    src = load_uk()
    # 複数行最短一致
    base = re.findall('{{基礎情報 (.*?)}}\n', src, flags=re.DOTALL)[0]
    templates = re.findall('\n\|.*', base, flags=re.DOTALL)[0].split('\n|')
    dst = {}
    for template in templates[1:]:
        field, value = template.split(' = ')
        dst[field] = value
    for k, v in dst.items():
        print(k, ':', v)


def task26():
    """26. 強調マークアップの除去
    """
    src = load_uk()
    # 複数行最短一致
    base = re.findall('{{基礎情報 (.*?)}}\n', src, flags=re.DOTALL)[0]
    templates = re.findall('\n\|.*', base, flags=re.DOTALL)[0].split('\n|')
    dst = {}
    for template in templates[1:]:
        field, value = template.split(' = ')
        value = re.sub('\'+', '', value)
        dst[field] = value
    for k, v in dst.items():
        print(k, ':', v)


def task27():
    """27. 内部リンクの除去
    """
    src = load_uk()
    # 複数行最短一致
    base = re.findall('{{基礎情報 (.*?)}}\n', src, flags=re.DOTALL)[0]
    templates = re.findall('\n\|.*', base, flags=re.DOTALL)[0].split('\n|')
    dst = {}
    for template in templates[1:]:
        field, value = template.split(' = ')
        value = re.sub('\'+', '', value)
        value = re.sub('\[[^\[]*\|', '', value)
        value = re.sub('\[+', '', value)
        value = re.sub('\]+', '', value)
        dst[field] = value
    for k, v in dst.items():
        print(k, ':', v)


def task28():
    """28. MediaWikiマークアップの除去
    """
    src = load_uk()
    # 複数行最短一致
    base = re.findall('{{基礎情報 (.*?)}}\n', src, flags=re.DOTALL)[0]
    templates = re.findall('\n\|.*', base, flags=re.DOTALL)[0].split('\n|')
    dst = {}
    for template in templates[1:]:
        field, value = template.split(' = ')
        value = re.sub('\'+', '', value)
        value = re.sub('\[[^\[]*\|', '', value)
        value = re.sub('\[+', '', value)
        value = re.sub('\]+', '', value)
        value = re.sub('<br\s*>', '\n', value)
        value = re.sub('<.*?>', '', value)
        value = re.sub('.*[^\{]*\|', '', value)
        value = re.sub('\}+', '', value)
        value = re.sub('https*://.*?\s', ' ', value)
        dst[field] = value
    for k, v in dst.items():
        print(k, ':', v)


def task29():
    """29. 国旗画像のURLを取得する
    """
    src = load_uk()
    base = re.findall('{{基礎情報 (.*?)}}\n', src, flags=re.DOTALL)[0]
    templates = re.findall('\n\|.*', base, flags=re.DOTALL)[0].split('\n|')
    base_info = {}
    for template in templates[1:]:
        field, value = template.split(' = ')
        value = re.sub('\'+', '', value)
        value = re.sub('\[[^\[]*\|', '', value)
        value = re.sub('\[+', '', value)
        value = re.sub('\]+', '', value)
        value = re.sub('<br\s*>', '\n', value)
        value = re.sub('<.*?>', '', value)
        value = re.sub('.*[^\{]*\|', '', value)
        value = re.sub('\}+', '', value)
        value = re.sub('https*://.*?\s', ' ', value)
        base_info[field] = value
    prefix = 'File:'
    ref = prefix + base_info['国旗画像']
    api_url = 'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=imageinfo&iiprop=url'
    url = api_url + '&titles={}'.format(ref)
    r = json.loads(requests.get(url).content)
    dst = json_search(r, 'url')
    print(dst)


if __name__ == '__main__':
    task29()

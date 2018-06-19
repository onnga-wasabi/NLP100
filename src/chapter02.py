from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def load_data():
    path = DATA_DIR / 'hightemp.txt'
    with open(path, 'r') as rf:
        src = rf.read()
    return src


def task10():
    src = load_data()
    dst = [s for s in src.split('\n') if s]
    print(len(dst))


def task11():
    src = load_data()
    print(src.replace('\t', ' '))


if __name__ == '__main__':
    task11()

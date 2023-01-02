import yaml
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(CUR_PATH, "config.yaml")
with open(CONFIG_PATH, 'r', encoding='utf-8') as _fp:
    config = yaml.safe_load(_fp)

if __name__ == '__main__':
    pass

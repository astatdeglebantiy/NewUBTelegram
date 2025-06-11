import json
import os
import yaml

CONFIGS_PATH = 'configs/'
DATA_PATH = 'data/'
TEMP_PATH = 'temp/'
HANDLERS_PATH = 'handlers/'
FUNCTIONS_PATH = 'functions/'
MAIN_CONFIG_PATH = f'{CONFIGS_PATH}config.json'
API_KEYS_PATH = f'{CONFIGS_PATH}api_keys.json'
LEVEL_OF_ADMISSION_PATH = f'{DATA_PATH}levels_of_admission.json'
WHITELIST_PATH = f'{DATA_PATH}whitelist.json'
HANDLERS_YAML_PATH = f'{HANDLERS_PATH}handlers.yaml'
FUNCTIONS_YAML_PATH = f'{FUNCTIONS_PATH}functions.yaml'


def load(path: str, dir_path: str | None = None):
    if dir_path:
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass
    with open(path) as f:
        return json.load(f)


def save(obj, path: str, dir_path: str | None = None):
    if dir_path:
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass
    with open(path, 'w') as f:
        return json.dump(obj, f)


def load_yaml(path: str):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_whitelist() -> list[str]:
    try:
        os.mkdir(DATA_PATH)
    except FileExistsError:
        pass
    try:
        with open(WHITELIST_PATH) as f:
            return json.load(f)
    except FileExistsError:
        return []

def save_whitelist(obj):
    try:
        os.mkdir(DATA_PATH)
    except FileExistsError:
        pass
    with open(WHITELIST_PATH, 'w') as f:
        return json.dump(obj, f)

def clear_temp():
    try:
        os.mkdir(TEMP_PATH)
    except FileExistsError:
        pass
    for root, dirs, files in os.walk(TEMP_PATH, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for _dir in dirs:
            os.rmdir(os.path.join(root, _dir))

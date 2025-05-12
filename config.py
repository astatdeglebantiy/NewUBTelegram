import json
import os

CONFIGS_PATH = 'configs/'
DATA_PATH = 'data/'
TEMP_PATH = 'temp/'
MAIN_CONFIG_PATH = f'{CONFIGS_PATH}config.json'
API_KEYS_PATH = f'{CONFIGS_PATH}api_keys.json'
LEVEL_OF_ADMISSION_PATH = f'{DATA_PATH}levels_of_admission.json'
WHITELIST_PATH = f'{DATA_PATH}whitelist.json'


def load_main_config() -> dict:
    try:
        os.mkdir(CONFIGS_PATH)
    except FileExistsError:
        pass
    with open(MAIN_CONFIG_PATH) as f:
        return json.load(f)

def load_api_keys() -> dict:
    try:
        os.mkdir(CONFIGS_PATH)
    except FileExistsError:
        pass
    with open(API_KEYS_PATH) as f:
        return json.load(f)

def load_levels_of_admission() -> dict[str, int]:
    try:
        os.mkdir(DATA_PATH)
    except FileExistsError:
        pass
    with open(LEVEL_OF_ADMISSION_PATH) as f:
        return json.load(f)

def load_whitelist() -> list[str]:
    try:
        os.mkdir(DATA_PATH)
    except FileExistsError:
        pass
    try:
        with open(WHITELIST_PATH) as f:
            return json.load(f)
    except Exception:
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
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

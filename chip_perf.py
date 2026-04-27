CHIP_DB = {
    "Apple M4": {"multi": 14000},
    "Snapdragon 8 Gen 3": {"multi": 7200},
    "Dimensity 9300": {"multi": 7500},
}

def find_chip(name):
    for k in CHIP_DB:
        if k.lower() in name.lower():
            return CHIP_DB[k]
    return None

def compare(base, target):
    if not base or not target:
        return "-"
    return int((target["multi"] / base["multi"]) * 100)

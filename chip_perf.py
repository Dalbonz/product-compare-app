CHIP_DB = {
    "Apple M4": {"single": 4000, "multi": 14000, "gpu": 9000, "npu": 38},
    "Snapdragon 8 Gen 3": {"single": 2200, "multi": 7200, "gpu": 6000, "npu": 45},
    "Dimensity 9300": {"single": 2300, "multi": 7500, "gpu": 6200, "npu": 40},
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

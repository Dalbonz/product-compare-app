# chip_perf.py - 새 버전 (nanoreview.net 기반)

CHIP_DB = {
    "Apple M4": {
        "single": 3800,
        "multi": 14500,
        "gpu": 9500,      # GFXBench / 3DMark 기준 상대 점수
        "npu": 38000,     # TOPS 기준으로 환산
        "antutu": 2800000,
        "tops": 38.0
    },
    "Apple M3": {
        "single": 3200,
        "multi": 12500,
        "gpu": 8200,
        "npu": 31000,
        "antutu": 2200000,
        "tops": 31.0
    },
    "Apple M2": {
        "single": 2600,
        "multi": 10500,
        "gpu": 6500,
        "npu": 15700,
        "antutu": 1800000,
        "tops": 15.7
    },
    "Snapdragon 8 Gen 3": {
        "single": 2300,
        "multi": 7200,
        "gpu": 9200,
        "npu": 45000,
        "antutu": 2100000,
        "tops": 45.0
    },
    "Snapdragon 8 Elite": {
        "single": 2800,
        "multi": 10500,
        "gpu": 14500,
        "npu": 48000,
        "antutu": 3200000,
        "tops": 48.0
    },
    "Dimensity 9300": {
        "single": 2200,
        "multi": 7500,
        "gpu": 8800,
        "npu": 42000,
        "antutu": 2200000,
        "tops": 42.0
    },
    # 더 많은 칩셋은 필요할 때 추가
}

def find_chip(name: str):
    """칩셋 이름으로 DB에서 찾기 (부분 매칭)"""
    if not name:
        return None
    name_lower = name.lower()
    for key in CHIP_DB:
        if key.lower() in name_lower or name_lower in key.lower():
            return CHIP_DB[key]
    return None


def compare_chips(base_chip: dict, target_chip: dict) -> dict:
    """base 대비 target의 성능을 %로 반환"""
    if not base_chip or not target_chip:
        return {}

    result = {}
    for key in ["single", "multi", "gpu", "npu", "antutu"]:
        if key in base_chip and key in target_chip:
            result[key] = round((target_chip[key] / base_chip[key]) * 100)
    
    if "tops" in base_chip and "tops" in target_chip:
        result["tops"] = round((target_chip["tops"] / base_chip["tops"]) * 100, 1)
    
    return result

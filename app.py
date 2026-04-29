import streamlit as st

st.set_page_config(layout="wide")

# -----------------------------
# 더미 데이터 (UI 검증용)
# -----------------------------
DUMMY = {
    "iPad Pro M4": {
        "image": "https://fdn2.gsmarena.com/vv/bigpic/apple-ipad-pro-11-2024.jpg",
        "release": "2024",
        "price": "150만원",
        "size": "444g",
        "display": "11 OLED 120Hz",
        "chipset": "Apple M4",
        "perf": 100,
        "memory": "16GB"
    },
    "Galaxy Tab S10": {
        "image": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-tab-s9.jpg",
        "release": "2023",
        "price": "130만원",
        "size": "500g",
        "display": "11 AMOLED 120Hz",
        "chipset": "Snapdragon 8 Gen3",
        "perf": 85,
        "memory": "12GB"
    },
    "Xiaomi Pad 7": {
        "image": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-pad-6.jpg",
        "release": "2022",
        "price": "90만원",
        "size": "480g",
        "display": "LCD 144Hz",
        "chipset": "Dimensity",
        "perf": 70,
        "memory": "8GB"
    }
}

# -----------------------------
# UI 상태
# -----------------------------
if "devices" not in st.session_state:
    st.session_state.devices = []

# -----------------------------
# 타이틀
# -----------------------------
st.title("Tablet Compare Pro")

# -----------------------------
# 제품 선택 UI
# -----------------------------
cols = st.columns(len(st.session_state.devices) + 1)

# 기존 카드
for i, dev in enumerate(st.session_state.devices):
    with cols[i]:
        st.image(DUMMY[dev]["image"], use_container_width=True)
        st.markdown(f"**{dev}**")

# + 버튼
with cols[-1]:
    if st.button("+"):
        if len(st.session_state.devices) < 5:
            st.session_state.devices.append("iPad Pro M4")

# -----------------------------
# 제품 선택 드롭다운
# -----------------------------
for i in range(len(st.session_state.devices)):
    st.session_state.devices[i] = st.selectbox(
        f"제품 {i+1}",
        list(DUMMY.keys()),
        index=list(DUMMY.keys()).index(st.session_state.devices[i]),
        key=f"select_{i}"
    )

# -----------------------------
# GO 버튼
# -----------------------------
if st.button("GO"):
    st.session_state.show_table = True

# -----------------------------
# 테이블
# -----------------------------
if st.session_state.get("show_table"):

    st.markdown("## 비교 결과")

    headers = ["항목"] + st.session_state.devices

    rows = [
        ["출시일"] + [DUMMY[d]["release"] for d in st.session_state.devices],
        ["가격"] + [DUMMY[d]["price"] for d in st.session_state.devices],
        ["크기"] + [DUMMY[d]["size"] for d in st.session_state.devices],
        ["디스플레이"] + [DUMMY[d]["display"] for d in st.session_state.devices],
        ["AP"] + [DUMMY[d]["chipset"] for d in st.session_state.devices],
        ["성능비교"] + [DUMMY[d]["perf"] for d in st.session_state.devices],
        ["메모리"] + [DUMMY[d]["memory"] for d in st.session_state.devices],
    ]

    # 스타일 테이블
    html = "<table style='width:100%; border-collapse:collapse;'>"

    # header
    html += "<tr>" + "".join([f"<th style='padding:10px; background:#eee'>{h}</th>" for h in headers]) + "</tr>"

    for row in rows:
        html += "<tr>"
        for i, cell in enumerate(row):
            if row[0] == "성능비교" and i > 0:
                color = "green" if cell >= 100 else "orange" if cell >= 80 else "red"
                html += f"<td style='padding:8px; text-align:center; color:{color}'><b>{cell}%</b></td>"
            else:
                html += f"<td style='padding:8px; text-align:center'>{cell}</td>"
        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

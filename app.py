import streamlit as st
from scraper import get_device
from chip_perf import find_chip, compare

st.set_page_config(layout="wide")

# =========================
# STYLE (애플 느낌)
# =========================
st.markdown("""
<style>
body {
    background-color: #f5f5f7;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    text-align: center;
}
.title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 20px;
}
.spec-table {
    width: 100%;
    border-collapse: collapse;
}
.spec-table th {
    text-align: left;
    padding: 12px;
    background: #fafafa;
    font-size: 14px;
}
.spec-table td {
    padding: 12px;
    border-bottom: 1px solid #eee;
    font-size: 14px;
}
.win {
    color: green;
    font-weight: 600;
}
.lose {
    color: red;
}
.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Tablet Compare Pro</div>', unsafe_allow_html=True)

# =========================
# 상태
# =========================
if "devices" not in st.session_state:
    st.session_state.devices = ["", ""]

# =========================
# 제품 입력 영역
# =========================
cols = st.columns(len(st.session_state.devices))

device_data = []

for i, col in enumerate(cols):
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        name = st.text_input("모델명 입력", value=st.session_state.devices[i], key=f"input{i}")
        st.session_state.devices[i] = name

        if name:
            data = get_device(name)
            device_data.append(data)

            if data.get("image"):
                st.image(data["image"], use_container_width=True)

            st.markdown(f"**{data.get('name', name)}**")

        else:
            device_data.append({})

        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# + 버튼
# =========================
if st.button("+"):
    if len(st.session_state.devices) < 5:
        st.session_state.devices.append("")
        st.rerun()

# =========================
# 비교 버튼
# =========================
if st.button("COMPARE"):

    st.markdown("## 📊 비교 결과")

    keys = [
        ("출시", "Launch::Announced"),
        ("가격", "Misc::Price"),
        ("디멘젼", "Body::Dimensions"),
        ("디스플레이", "Display::Size"),
        ("주사율", "Display::Refresh rate"),
        ("칩셋", "Platform::Chipset"),
        ("메모리", "Memory::Internal"),
        ("카메라", "Main Camera::Single"),
        ("배터리", "Battery::Type"),
    ]

    # AP 기준
    base_chip = find_chip(device_data[0].get("Platform::Chipset", ""))

    html = "<table class='spec-table'>"

    # 헤더
    html += "<tr><th>항목</th>"
    for d in device_data:
        html += f"<th class='center'>{d.get('name','-')}</th>"
    html += "</tr>"

    # 데이터
    for label, key in keys:
        html += f"<tr><td>{label}</td>"

        values = [d.get(key, "-") for d in device_data]

        for v in values:
            html += f"<td class='center'>{v}</td>"

        html += "</tr>"

    # AP 성능 비교
    html += "<tr><td>AP 성능</td>"

    for d in device_data:
        chip = find_chip(d.get("Platform::Chipset", ""))
        val = compare(base_chip, chip)

        if val == "-":
            html += "<td class='center'>-</td>"
        else:
            cls = "win" if val >= 100 else "lose"
            html += f"<td class='center {cls}'>{val}%</td>"

    html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

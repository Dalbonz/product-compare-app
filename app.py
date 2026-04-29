import streamlit as st
from scraper import get_device
from chip_perf import find_chip, compare_chips

st.set_page_config(page_title="Tablet Compare Pro", layout="wide")

# ====================== 스타일 ======================
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .title {
        font-size: 32px;
        font-weight: 700;
        color: #1d1d1f;
        margin-bottom: 24px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
        text-align: center;
        height: 100%;
    }
    .spec-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    .spec-table th {
        background: #f1f3f5;
        padding: 14px 10px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #ddd;
    }
    .spec-table td {
        padding: 14px 10px;
        border-bottom: 1px solid #eee;
        text-align: center;
    }
    .win { color: #00c853; font-weight: 600; }
    .lose { color: #ff3b30; font-weight: 600; }
    .center { text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">Tablet Compare Pro</h1>', unsafe_allow_html=True)

# ====================== 세션 상태 ======================
if "devices" not in st.session_state:
    st.session_state.devices = ["", "", ""]

# ====================== 제품 입력 영역 ======================
cols = st.columns(len(st.session_state.devices))

device_data = []

for i, col in enumerate(cols):
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.subheader(f"제품 {i+1}")
        
        name = st.text_input(
            "모델명 입력", 
            value=st.session_state.devices[i], 
            key=f"input_{i}",
            placeholder="예: iPad Pro 11 M4"
        )
        st.session_state.devices[i] = name

        if name.strip():
            with st.spinner("스펙을 불러오는 중입니다..."):
                data = get_device(name.strip())
                device_data.append(data)
                
                if data.get("image"):
                    st.image(data["image"], use_container_width=True)
                
                display_name = data.get("name", name)
                st.markdown(f"**{display_name}**")
        else:
            device_data.append({})
            st.info("모델명을 입력하세요")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ====================== 버튼 영역 ======================
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    if st.button("＋ 제품 추가", use_container_width=True):
        if len(st.session_state.devices) < 5:
            st.session_state.devices.append("")
            st.rerun()

with col2:
    if st.button("초기화", use_container_width=True):
        st.session_state.devices = ["", "", ""]
        st.rerun()

with col3:
    compare_btn = st.button("비교 시작", type="primary", use_container_width=True)

# ====================== 비교 결과 ======================
if compare_btn:
    valid_devices = [d for d in device_data if d and d.get("name")]
    
    if len(valid_devices) < 2:
        st.error("최소 2개 이상의 제품을 입력해주세요.")
    else:
        st.markdown("### 비교 결과")
        
        base_data = valid_devices[0]
        base_chip = find_chip(base_data.get("Platform::Chipset") or base_data.get("chipset", ""))

        # 비교 테이블
        keys = [
            ("출시일", "Launch::Announced"),
            ("가격", "Misc::Price"),
            ("크기 (mm)", "Body::Dimensions"),
            ("디스플레이", "Display::Size"),
            ("주사율", "Display::Refresh rate"),
            ("메모리", "Memory::Internal"),
            ("배터리", "Battery::Type"),
        ]

        html = """
        <table class="spec-table">
            <tr>
                <th style="width:180px">항목</th>
        """
        for d in valid_devices:
            html += f"<th class='center'>{d.get('name', 'Unknown')}</th>"
        html += "</tr>"

        for label, key in keys:
            html += f"<tr><td><b>{label}</b></td>"
            for d in valid_devices:
                value = d.get(key, "-")
                html += f"<td class='center'>{value}</td>"
            html += "</tr>"

        # AP 성능 비교
        if base_chip:
            html += "<tr><td><b>AP 성능 비교</b><br><small>(기준 기기 대비 %)</small></td>"
            for d in valid_devices:
                target_chip = find_chip(d.get("Platform::Chipset") or d.get("chipset", ""))
                if not target_chip:
                    html += "<td class='center'>데이터 없음</td>"
                    continue
                
                comp = compare_chips(base_chip, target_chip)
                
                html += "<td class='center'>"
                for k, v in comp.items():
                    cls = "win" if v >= 100 else "lose"
                    html += f"<span class='{cls}'>{k.upper()}: {v}%</span><br>"
                html += "</td>"
            html += "</tr>"

        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

else:
    st.info("제품을 입력한 후 '비교 시작' 버튼을 눌러주세요.")

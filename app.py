import streamlit as st
from scraper import get_device
from chip_perf import find_chip, compare

st.set_page_config(layout="wide")

st.title("Tablet Compare Pro")

if "devices" not in st.session_state:
    st.session_state.devices = ["", ""]

# ➕ 버튼
if st.button("+ Add Device"):
    if len(st.session_state.devices) < 5:
        st.session_state.devices.append("")

cols = st.columns(len(st.session_state.devices))
device_data = []

# 입력
for i, col in enumerate(cols):
    with col:
        name = st.text_input(f"Device {i+1}", value=st.session_state.devices[i])
        st.session_state.devices[i] = name

        if name:
            data = get_device(name)
            device_data.append(data)

            if data.get("image"):
                st.image(data["image"], width=150)

            st.write(data.get("name", name))
        else:
            device_data.append({})

# 실행 버튼
if st.button("COMPARE"):

    st.subheader("Result")

    keys = [
        "Launch::Announced",
        "Misc::Price",
        "Body::Dimensions",
        "Display::Type",
        "Display::Size",
        "Platform::Chipset",
        "Memory::Internal",
        "Battery::Type"
    ]

    rows = []

    for k in keys:
        row = [k.split("::")[1]]
        for d in device_data:
            row.append(d.get(k, "-"))
        rows.append(row)

    # AP 성능 비교
    perf_row = ["Performance"]

    base_chip = find_chip(device_data[0].get("Platform::Chipset", ""))

    for d in device_data:
        chip = find_chip(d.get("Platform::Chipset", ""))
        val = compare(base_chip, chip)
        perf_row.append(f"{val}%" if val != "-" else "-")

    rows.append(perf_row)

    st.table(rows)

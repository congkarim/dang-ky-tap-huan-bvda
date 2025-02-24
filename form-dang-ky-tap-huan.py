import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Định nghĩa tệp lưu trữ dữ liệu
DATA_FILE = "dang_ky.xlsx"
KHOAPHONG_FILE = "dsKhoaPhong.csv"
LOGO_URL = "https://benhviendonganh.com/DATA/INFO/2023/2/17/benh-vien-da-khoa-dong-anh-9937e.png"
FAVICON_URL = "https://benhviendonganh.com/Statics/shared/ico/apple-touch-icon-144-precomposed.png"

def load_khoaphong():
    """Tải danh sách khoa phòng từ tệp CSV"""
    if os.path.exists(KHOAPHONG_FILE):
        df = pd.read_csv(KHOAPHONG_FILE)
        return df.iloc[:, 0].tolist()  # Lấy danh sách khoa phòng từ cột đầu tiên
    return []

def load_data():
    """Tải dữ liệu đã đăng ký từ tệp Excel"""
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)
    return pd.DataFrame(columns=["ID", "Họ và tên", "Ngày sinh", "Chức vụ", "Đối tượng", "Khoa/Phòng", "Trình độ chuyên môn", "Cấp CME", "Số điện thoại", "Email", "Thời gian"])

def save_data(data):
    """Lưu dữ liệu đăng ký vào tệp Excel"""
    data.to_excel(DATA_FILE, index=False)

def main():
    st.set_page_config(page_title="Đăng ký tập huấn", page_icon=FAVICON_URL)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <img src="{LOGO_URL}" width="250">
    </div>
""", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center;">
        <h1>ĐĂNG KÝ THAM DỰ TẬP HUẤN</h1>
        <h2>Ứng dụng của nội soi phế quản ống mềm trong chẩn đoán và điều trị</h2>
        <hr>
    </div>
    """, unsafe_allow_html=True)
    data = load_data()
    menu = ["Đăng ký", "Thống kê"]
    choice = st.sidebar.selectbox("Chọn chức năng", menu)

    if choice == "Đăng ký":
        st.header("Form đăng ký")
        khoa_phong_list = load_khoaphong()
        
        hoten = st.text_input("Họ và tên")
        ngaysinh = st.date_input("Ngày sinh", value=None, format="DD/MM/YYYY")
        chucvu = st.text_input("Chức vụ")
        doituong = st.selectbox("Đối tượng", ["Bác sĩ"])
        st.info("Thời điểm này CME chỉ đăng ký cấp cho đối tượng Bác sĩ")
        khoa = st.selectbox("Khoa/Phòng", khoa_phong_list) if khoa_phong_list else st.text_input("Khoa/Phòng")
        trinhdo = st.selectbox("Trình độ chuyên môn", ["CKII", "CKI", "TS", "ThS", "Đại học", "Cao đẳng"])
        cap_cme = st.radio("Cấp CME", ["Có", "Không"])
        sdt = st.text_input("Số điện thoại")
        email = st.text_input("Email")

        if st.button("Đăng ký"):
            if not hoten.strip():
                st.error("Họ và tên là bắt buộc.")
            elif not doituong.strip():
                st.error("Đối tượng là bắt buộc.")
            elif not khoa.strip():
                st.error("Khoa/Phòng là bắt buộc.")
            elif not sdt.strip():
                st.error("Số điện thoại là bắt buộc.")
            else:
                data = load_data()
                new_id = len(data) + 1
                new_entry = pd.DataFrame({
                    "ID": [new_id],
                    "Họ và tên": [hoten],
                    "Ngày sinh": [ngaysinh.strftime("%d/%m/%Y")],
                    "Chức vụ": [chucvu],
                    "Đối tượng": [doituong],
                    "Khoa/Phòng": [khoa],
                    "Trình độ chuyên môn": [trinhdo],
                    "Cấp CME": [cap_cme],
                    "Số điện thoại": [sdt],
                    "Email": [email],
                    "Thời gian": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })
                data = pd.concat([data, new_entry], ignore_index=True)
                save_data(data)
                st.success("Đăng ký thành công!")
    elif choice == "Thống kê":
        st.sidebar.header("Thống kê đăng ký")
        st.sidebar.write(f"Tổng số đăng ký: {len(data)}")
        
        if not data.empty:
            khoa_counts = data["Khoa/Phòng"].value_counts().reset_index()
            khoa_counts.columns = ["Khoa/Phòng", "Số lượng"]
            st.sidebar.dataframe(khoa_counts)

            if st.sidebar.checkbox("Hiển thị thống kê chi tiết"):
                st.header("Thống kê đăng ký chi tiết")
                st.write(f"Tổng số đăng ký: {len(data)}")
                st.dataframe(khoa_counts)
    st.markdown(f"""
    <div style="text-align: center; margin-top: 50px;">
        <hr>
        <p><strong>Đã đăng ký: {len(data)}</strong></p>
    </div>
    """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()

import streamlit as st
import requests

# 1. Cấu hình trang
st.set_page_config(page_title="Sàng lọc Tiểu đường AI", layout="wide")

# 2. CSS Tùy chỉnh (Đã chỉnh sửa tiêu đề và khoảng cách)
st.markdown("""
    <style>
    /* Làm trong suốt thanh Header mặc định của Streamlit ở góc trên */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Hình nền mảng màu */
    .stApp {
        background-color: #eaf1ed;
        background-image: 
            radial-gradient(circle at 0% 0%, #ecd384 25%, transparent 50%),
            radial-gradient(circle at 100% 100%, #83b6a7 25%, transparent 50%);
    }
    
    /* KHỐI TRẮNG TRUNG TÂM: Tăng khoảng cách cách đỉnh màn hình */
    .block-container {
        background-color: #ffffff;
        border-radius: 25px;
        box-shadow: 0px 15px 40px rgba(0, 0, 0, 0.08);
        padding: 4rem 4rem 3rem 4rem !important; 
        margin-top: 5rem !important; /* Đẩy khối trắng tụt xuống cách xa header */
        margin-bottom: 3rem;
        max-width: 1000px;
    }

    /* TIÊU ĐỀ CHÍNH: Căn giữa và In hoa */
    h1 {
        color: #1a4a38 !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        line-height: 1.2 !important;
        text-align: center !important; /* Căn giữa */
        text-transform: uppercase !important; /* Ép in hoa */
        margin-bottom: 10px !important;
    }
    
    h2, h3, h4 {
        color: #1a4a38 !important;
        font-weight: 700 !important;
    }
    
    /* Chữ phụ, Label và Căn giữa đoạn mô tả */
    p, label {
        color: #5d6d67 !important;
        font-weight: 500 !important;
    }
    .subtitle-text {
        text-align: center !important; /* Căn giữa đoạn mô tả */
        margin-bottom: 40px !important;
        font-size: 1.1rem;
    }

    /* Các thẻ bo góc chứa tham số nhập liệu */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        background-color: #f8fbfb !important;
        border: 1.5px solid #e1e8e5 !important;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Nút bấm vàng bo tròn */
    [data-testid="stFormSubmitButton"] > button {
        background-color: #dbad46 !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 0.6rem 0 !important;
        transition: 0.3s;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #c4993a !important;
        box-shadow: 0 5px 15px rgba(219, 173, 70, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Tiêu đề và Mô tả (Đã bỏ thẻ <br> để chữ tự động dàn đều và căn giữa)
st.markdown("<h1>SÀNG LỌC RỦI RO TIỂU ĐƯỜNG</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Hệ thống hỗ trợ quyết định lâm sàng ứng dụng Trí tuệ nhân tạo (AI), phân tích trực tiếp từ các chỉ số y tế của bạn.</p>", unsafe_allow_html=True)

# 4. Form nhập liệu với các thẻ bo góc (Cards)
with st.form("patient_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("#### Thể chất & Sinh tồn")
            bmi = st.number_input("Chỉ số BMI", 10.0, 60.0, 24.5)
            age = st.slider("Nhóm tuổi (1: Trẻ - 13: Già)", 1, 13, 5)
            sex = st.radio("Giới tính", [(1.0, "Nam"), (0.0, "Nữ")], format_func=lambda x: x[1], horizontal=True)
            high_bp = st.selectbox("Cao huyết áp", [(0.0, "Không"), (1.0, "Có")], format_func=lambda x: x[1])
            high_chol = st.selectbox("Cholesterol cao", [(0.0, "Không"), (1.0, "Có")], format_func=lambda x: x[1])
            
    with col2:
        with st.container(border=True):
            st.markdown("#### Bệnh lý & Thói quen")
            heart_disease = st.selectbox("Tiền sử bệnh tim", [(0.0, "Không"), (1.0, "Có")], format_func=lambda x: x[1])
            gen_hlth = st.select_slider("Sức khỏe chung (1: Tốt - 5: Kém)", [1, 2, 3, 4, 5], 2)
            phys_hlth = st.number_input("Ngày thể chất kém (trong 30 ngày)", 0, 30, 0)
            ment_hlth = st.number_input("Ngày tinh thần kém (trong 30 ngày)", 0, 30, 0)
            smoker = st.selectbox("Tiền sử hút thuốc", [(0.0, "Không"), (1.0, "Có")], format_func=lambda x: x[1])

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("BẮT ĐẦU PHÂN TÍCH BẰNG AI", use_container_width=True)

# 5. Khối xử lý kết quả
if submitted:
    payload = {
        "HighBP": high_bp[0], "HighChol": high_chol[0], "CholCheck": 1.0, "BMI": bmi, 
        "Smoker": smoker[0], "Stroke": 0.0, "HeartDiseaseorAttack": heart_disease[0], 
        "PhysActivity": 1.0, "Fruits": 1.0, "Veggies": 1.0, "HvyAlcoholConsump": 0.0, 
        "AnyHealthcare": 1.0, "NoDocbcCost": 0.0, "GenHlth": float(gen_hlth), 
        "MentHlth": float(ment_hlth), "PhysHlth": float(phys_hlth), "DiffWalk": 0.0, 
        "Sex": sex[0], "Age": float(age), "Education": 5.0, "Income": 6.0
    }
    
    with st.spinner("Hệ thống đang nội suy dữ liệu..."):
        try:
            res = requests.post("http://127.0.0.1:8000/predict", json=payload).json()
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(border=True):
                status_color = "#e55a5a" if res['result_code'] == 1 else "#3eb489"
                status_text = "PHÁT HIỆN RỦI RO" if res['result_code'] == 1 else "SỨC KHỎE AN TOÀN"
                
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <p style="font-size: 1.1rem; color: #5d6d67; margin-bottom: 0;">Kết luận từ Mô hình Học máy</p>
                    <h2 style="color: {status_color}; font-size: 2.5rem; margin-top: 5px;">{status_text}</h2>
                    <p style="font-size: 1.2rem;">Tỷ lệ dự báo: <b style="color: {status_color};">{res['risk_probability']}%</b></p>
                    <hr style="border-top: 1px dashed #e1e8e5;">
                    <p><b>Khuyến nghị lâm sàng:</b> {res['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.error("Lỗi kết nối Server. Vui lòng kiểm tra lại Backend (FastAPI).")
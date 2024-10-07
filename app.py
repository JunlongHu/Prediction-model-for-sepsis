import streamlit as st
import joblib


if "Model" not in st.session_state:
    with st.spinner("Page resource initialization..."):
        st.session_state["Model"] = joblib.load('XGboost_Model.m')


def set_background():
    page_bg_img = '''
    <style>
    h3 {padding: 0.75rem 0px 0.75rem;margin-top: 2rem;box-shadow: 0px 3px 5px gray;}
    MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    .st-emotion-cache-13ln4jf {padding: 1rem 1rem 4rem}
    button:hover {background: #00800033}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background()
st.markdown("<h3 style='text-align: center'>Prediction model of pediatric sepsis</h3>", unsafe_allow_html=True)
st.write("")
with st.form("my_form"):
    map_dic = {"Yes": 1, "No": 0}
    col1, col2 = st.columns([5, 5])
    with col1:
        CRP = st.text_input("CRP", None)
        Platelet = st.text_input("Platelet", None)
        INR = st.text_input("INR", None)
        D_dimer = st.text_input("D-dimer", None)  # 注意变量名不能有空格，改为D_dimer
    with col2:
        P_F = st.text_input("P/F", None)  # 同样注意变量名
        GCS = st.text_input("GCS", None)
        IMV = st.selectbox("IMV", ("Yes", "No"))
        Vasoactive_drug = st.selectbox("Vasoactive drug", ("Yes", "No"))
    if st.form_submit_button("Predict"):
        try:
            # 将输入数据转换为浮点数，并确保数量为8
            inputs = [
                float(CRP),
                float(Platelet),
                float(INR),
                float(D_dimer),
                float(P_F),
                float(GCS),
                map_dic[IMV],
                map_dic[Vasoactive_drug]
            ]

            if len(inputs) != 8:
                st.error("输入特征数量不正确，请提供8个特征值！")
            else:
                # 进行预测
                res = st.session_state["Model"].predict_proba([inputs])[0][1] * 100
                if res >= 49.3:
                    st.markdown(
                        "#### Based on feature values, predicted :blue-background[possibility of sepsis] is :red["
                        "{:.2f}%] :worried:.".format(res))
                else:
                    st.markdown("#### Based on feature values, predicted :blue-background[possibility of sepsis] is "
                                ":green[{:.2f}%] :smile:.".format(res))
        except ValueError as e:
            st.error("输入参数不正确，请确保所有输入都是数字格式！错误信息: {}".format(e))
        except Exception as e:
            st.error("出现错误，请稍后再试！错误信息: {}".format(e))
            st.warning("The input parameter is incorrect, please try again!")

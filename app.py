import streamlit as st
import joblib


if "Model" not in st.session_state:
    with st.spinner("Page resource initialization..."):
        st.session_state["Model"] = joblib.load('RFModel.m')


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
st.markdown("<h3 style='text-align: center'>Prediction model of sepsis</h3>", unsafe_allow_html=True)
st.write("")
with st.form("my_form"):
    map_dic = {"Yes": 1, "No": 0}
    col1, col2 = st.columns([5, 5])
    with col1:
        PRISM = st.slider("Pediatric Risk of Mortality III", 0, 80, 4)
        CRP = st.text_input("C-reactive protein", None)
    with col2:
        PLT = st.slider("Platelet", 1, 1500, 270)
        MV = st.selectbox(
            "Mechanical ventilation",
            ("Yes", "No"),
        )
    INR = st.text_input("International normalized ratio", None)
    PaO2_FiO2 = st.text_input("Partial pressure of oxygen/fraction of inspiration oxygen", None)
    if st.form_submit_button("Predict"):
        try:
            res = st.session_state["Model"].predict_proba([[PRISM, PLT, float(INR), float(PaO2_FiO2), float(CRP), map_dic[MV]]])[0][1]*100
            if res >= 40.3:
                st.markdown("#### Based on feature values, predicted :blue-background[possibility of sepsis] is :red[{:.2f}%] :worried:.".format(res))
            else:
                st.markdown("#### Based on feature values, predicted :blue-background[possibility of sepsis] is :green[{:.2f}%] :smile:.".format(res))
        except:
            st.warning("The input parameter is incorrect, please try again!")

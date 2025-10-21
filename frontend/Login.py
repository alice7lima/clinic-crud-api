import streamlit as st
from api_functions import do_login

st.set_page_config(
    page_title="a clínica - Login",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    hide_sidebar = """
        <style>
            [data-testid="stSidebar"] {visibility: hidden; width: 0;}
            [data-testid="collapsedControl"] {display: none;}
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

st.title("a clínica - Área de Gestão")
st.subheader("Entre com uma conta de administrador")

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar"):
    response = do_login(user=username, password=password)
    
    if isinstance(response, str):
        st.session_state["logged_in"] = True
        st.session_state["api_token"] = response
        st.success("Login realizado com sucesso!")
        st.switch_page("pages/Consultas.py")
    elif response.get("status_code") == 401:
        st.error("Credenciais incorretas, verifique e tente novamente!")
    else:
        st.error("Erro ao tentar realizar login.")

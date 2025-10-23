import streamlit as st
import requests
import datetime
from api_functions import create_patient

st.set_page_config(page_title="Pacientes", page_icon="🧍‍♀️")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.switch_page("Login.py")

st.sidebar.title("Menu")
st.sidebar.page_link("pages/Consultas.py", label="Consultas")
st.sidebar.page_link("pages/Pacientes.py", label="Pacientes")
st.sidebar.page_link("pages/Profissionais.py", label="Profissionais")

if st.sidebar.button("🚪 Sair"):
    st.session_state["logged_in"] = False
    st.session_state["api_token"] = None
    st.switch_page("Login.py")

GENDER_MAP = {
    'Feminino': 'female',
    'Masculino': 'male',
    'Outros': 'other',
    'Prefiro não informar': 'not_announced'
}

INSURANCE_PROVIDERS = {
    "Unimed": "unimed",
    "Amil": "amil",
    "Porto": "porto",
    "Particular / Sem plano": "particular"
}

st.markdown("### 🧍‍♀️ Gestão pacientes")

with st.expander("Cadastrar novo paciente", expanded=True):
    with st.form("new_patient_form"):
        # Dados pessoais
        name = st.text_input("Nome completo")
        birth_date = st.date_input(
            "Data de Nascimento",
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today()
        )
        document = st.text_input("CPF (somente números)", max_chars=11, placeholder="Ex: 12345678901")
        if document and (not document.isdigit() or len(document) != 11):
            st.warning("⚠️ CPF inválido — informe exatamente 11 dígitos numéricos.")
        gender = st.selectbox("Gênero", list(GENDER_MAP.keys()))
        phone_number = st.text_input("Telefone / Celular", placeholder="(11) 99999-9999")
        email = st.text_input("E-mail", placeholder="seu@email.com")

        # Dados do plano de saúde
        insurance_provider = st.selectbox("Convênio", list(INSURANCE_PROVIDERS.keys()))
        insurance_number = st.text_input("Número do convênio (opcional)")

        # Contato de emergência
        emergency_contact = st.text_input("Contato de emergência (opcional)")
        emergency_phone = st.text_input("Telefone do contato de emergência (opcional)")

        # Dados adicionais
        blood_type = st.selectbox(
            "Tipo sanguíneo (opcional)",
            ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )
        organ_donor = st.checkbox("Doador de órgãos?")

        submitted = st.form_submit_button("Cadastrar Paciente")

        if submitted:
            if not name or not document:
                st.warning("⚠️ Campos obrigatórios: Nome e CPF.")
            else:
                payload = {
                    "name": name,
                    "birth_date": str(birth_date),
                    "document": document,
                    "gender": GENDER_MAP[gender],
                    "phone_number": phone_number,
                    "email": email,
                    "insurance_provider": INSURANCE_PROVIDERS[insurance_provider],
                    "insurance_number": insurance_number or None,
                    "emergency_contact": emergency_contact or None,
                    "emergency_phone": emergency_phone or None,
                    "blood_type": blood_type or None,
                    "organ_donor": organ_donor
                }

                try:
                    response = create_patient(payload)
                    if response.status_code in (200, 201):
                        st.success("Paciente cadastrado com sucesso!")
                    else:
                        data = response.json()
                        if "detail" in data:
                            if isinstance(data["detail"], list):
                                errors = "\n".join([error.get("msg", "Erro desconhecido") for error in data["detail"]])
                                st.error(f"Erro:\n{errors}")
                            else:
                                st.error(f"Erro: {data['detail']}")
                        else:
                            st.error(f"Erro inesperado ({response.status_code}).")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão com o servidor: {e}")
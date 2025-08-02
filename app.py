import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Autenticação com Google Sheets ---
try:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])
    worksheet = spreadsheet.worksheet("Tabela Gemini")

except Exception as e:
    st.error("🔴 ERRO DE CONEXÃO: Não foi possível conectar à Planilha Google.")
    st.error("Por favor, verifique se o ficheiro 'secrets.toml' está correto e se as permissões da planilha foram concedidas.")
    st.stop()

# --- Interface da Aplicação ---
st.title("Questionário Simples e Funcional")
st.write("Responda às perguntas abaixo. As respostas serão salvas na sua planilha.")

with st.form(key='evaluation_form', clear_on_submit=True):
    q1 = st.radio(
        "Pergunta 1: Qual o seu nível de satisfação hoje?",
        ["Muito Satisfeito", "Satisfeito", "Neutro", "Insatisfeito", "Muito Insatisfeito"]
    )
    q2 = st.select_slider(
        "Pergunta 2: De 1 a 5, como avalia a clareza deste formulário?",
        options=[1, 2, 3, 4, 5]
    )
    q3 = st.text_area("Pergunta 3: Deixe um comentário ou sugestão.")
    submit_button = st.form_submit_button(label='Enviar Respostas')

if submit_button:
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, q1, str(q2), q3]
        worksheet.append_row(new_row)
        st.success("✅ Respostas enviadas com sucesso! Obrigado.")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao tentar salvar os dados: {e}")

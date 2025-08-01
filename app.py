import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Autenticação com Google Sheets ---
# Tenta conectar e avisa sobre o erro específico
try:
    creds_dict = st.secrets["gcp_service_account"]
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])
    worksheet = spreadsheet.worksheet("Tabela Gemini")

except Exception as e:
    st.error("🔴 ERRO DE CONEXÃO: Não foi possível conectar à Planilha Google.")
    st.error("Por favor, verifique se o ficheiro 'secrets.toml' está correto e se as permissões da planilha foram concedidas.")
    # Linha abaixo é ótima para depurar o erro exato.
    # st.error(f"Detalhes técnicos do erro: {e}") 
    st.stop()


# --- Interface da Aplicação ---
st.title("Questionário Simples e Funcional")
st.write("Responda às perguntas abaixo. As respostas serão salvas na sua planilha.")

# Usar um formulário para que os botões só funcionem ao submeter
with st.form(key='evaluation_form', clear_on_submit=True):
    # Perguntas
    q1 = st.radio(
        "Pergunta 1: Qual o seu nível de satisfação hoje?",
        ["Muito Satisfeito", "Satisfeito", "Neutro", "Insatisfeito", "Muito Insatisfeito"],
        key="q1"
    )
    
    q2 = st.select_slider(
        "Pergunta 2: De 1 a 5, como avalia a clareza deste formulário?",
        options=[1, 2, 3, 4, 5],
        key="q2"
    )
    
    q3 = st.text_area(
        "Pergunta 3: Deixe um comentário ou sugestão.",
        key="q3"
    )

    # Botão de submissão
    submit_button = st.form_submit_button(label='Enviar Respostas')


# Lógica para salvar os dados quando o botão é pressionado
if submit_button:
    try:
        # Preparar a linha de dados para adicionar na planilha
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, q1, str(q2), q3]
        
        # Adicionar a nova linha
        worksheet.append_row(new_row)
        
        st.success("✅ Respostas enviadas com sucesso! Obrigado.")
        st.balloons() # Celebração!
        
    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao tentar salvar os dados: {e}")

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback
import os

# ========== VERIFICAÇÃO DE SECRETS ==========
st.sidebar.title("🔍 Diagnóstico de Configuração")

# Verificar se estamos no Streamlit Cloud
if os.environ.get('STREAMLIT_SERVER_RUNNING'):
    st.sidebar.info("Ambiente: Streamlit Cloud")
else:
    st.sidebar.info("Ambiente: Local")

# Carregar secrets de forma alternativa
try:
    # Tentar carregar secrets diretamente para debug
    all_secrets = dict(st.secrets)
    st.sidebar.write("Chaves disponíveis:", list(all_secrets.keys()))
    
    # Verificar chaves críticas
    if "spreadsheet_id" in all_secrets:
        SPREADSHEET_ID = all_secrets["spreadsheet_id"]
        st.sidebar.success(f"✅ ID da Planilha: {SPREADSHEET_ID}")
    else:
        st.sidebar.error("❌ spreadsheet_id NÃO encontrado!")
        st.error("ERRO CRÍTICO: spreadsheet_id não configurado")
        st.stop()
    
    if "gcp_service_account" in all_secrets:
        creds_info = all_secrets["gcp_service_account"]
        st.sidebar.success("✅ Conta de serviço encontrada")
    else:
        st.sidebar.error("❌ gcp_service_account NÃO encontrado!")
        st.error("ERRO CRÍTICO: Credenciais do Google não configuradas")
        st.stop()

except Exception as e:
    st.sidebar.error(f"❌ ERRO: {str(e)}")
    st.error("Falha ao carregar configurações")
    st.stop()

# ========== CONEXÃO COM GOOGLE SHEETS ==========
try:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Criar credenciais
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Abrir planilha
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet("Tabela Gemini")
    
    st.sidebar.success("✅ Conexão com Google Sheets estabelecida!")
    st.sidebar.info(f"Planilha: {spreadsheet.title}")
    st.sidebar.info(f"Aba: 'Tabela Gemini'")

except Exception as e:
    st.sidebar.error(f"❌ ERRO DE CONEXÃO: {str(e)}")
    st.error("Falha na conexão com o Google Sheets")
    st.code(traceback.format_exc())
    st.stop()

# ========== FORMULÁRIO ==========
st.title("📋 Questionário de Satisfação")
st.write("Preencha o formulário abaixo. Suas respostas serão salvas na planilha.")

with st.form(key='formulario', clear_on_submit=True):
    nome = st.text_input("Nome Completo*")
    email = st.text_input("Email*")
    avaliacao = st.slider("Avaliação (0-10):", 0, 10, 5)
    comentario = st.text_area("Comentários")
    enviado = st.form_submit_button("Enviar Respostas")

if enviado:
    if not nome or not email:
        st.error("Por favor, preencha nome e email!")
    else:
        with st.spinner("Salvando..."):
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = [timestamp, nome, email, avaliacao, comentario]
                worksheet.append_row(new_row)
                
                st.success("✅ Salvo com sucesso! Obrigado.")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")

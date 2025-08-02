import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback

# --- Autenticação com Google Sheets ---
try:
    # Scopes atualizados e corrigidos
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])
    
    # Acessando a aba específica pelo nome
    worksheet = spreadsheet.worksheet("Tabela Gemini")
    
    # Verificação adicional de permissões
    try:
        test_row = ["Teste de Conexão", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        worksheet.append_row(test_row)
        worksheet.delete_rows(worksheet.row_count)  # Remove a linha de teste
    except:
        pass
        
except gspread.exceptions.APIError as e:
    error_msg = e.response.json().get('error', {}).get('message', 'Erro desconhecido')
    st.error(f"🔴 ERRO DE API: {error_msg}")
    st.error("Verifique: 1) Permissões da planilha 2) Limites de cota")
    st.error(f"Detalhes técnicos: {str(e)}")
    st.stop()
    
except gspread.exceptions.WorksheetNotFound:
    st.error("🔴 ABA NÃO ENCONTRADA: Não existe uma aba chamada 'Tabela Gemini'")
    st.error("Por favor, verifique o nome exato da aba na planilha.")
    st.stop()
    
except Exception as e:
    st.error(f"🔴 ERRO DE CONEXÃO: {str(e)}")
    st.error(traceback.format_exc())
    st.error("Verifique o arquivo 'secrets.toml' e as permissões")
    st.stop()

# --- Interface da Aplicação ---
st.title("Questionário Simples e Funcional")
st.write("Responda às perguntas abaixo. As respostas serão salvas automaticamente na planilha.")

with st.form(key='evaluation_form', clear_on_submit=True):
    q1 = st.radio(
        "Pergunta 1: Qual o seu nível de satisfação hoje?",
        ["Muito Satisfeito", "Satisfeito", "Neutro", "Insatisfeito", "Muito Insatisfeito"],
        index=2
    )
    q2 = st.select_slider(
        "Pergunta 2: De 1 a 5, como avalia a clareza deste formulário?",
        options=[1, 2, 3, 4, 5],
        value=3
    )
    q3 = st.text_area("Pergunta 3: Deixe um comentário ou sugestão.")
    submit_button = st.form_submit_button(label='Enviar Respostas')

# Sidebar com informações de diagnóstico
st.sidebar.header("Diagnóstico de Conexão")
st.sidebar.success("✅ Conectado à Planilha Google!")
st.sidebar.info(f"Planilha: {spreadsheet.title}")
st.sidebar.info(f"Aba: 'Tabela Gemini'")
st.sidebar.info(f"Total de respostas: {worksheet.row_count - 1}")

if submit_button:
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, q1, str(q2), q3]
        worksheet.append_row(new_row)
        st.success("✅ Respostas enviadas com sucesso! Obrigado.")
        st.balloons()
        
        # Atualiza contador na sidebar
        st.sidebar.info(f"Total de respostas: {worksheet.row_count - 1}")
        
    except gspread.exceptions.APIError as e:
        error_json = e.response.json()
        error_msg = error_json.get('error', {}).get('message', 'Erro desconhecido da API')
        st.error(f"❌ ERRO AO SALVAR: {error_msg}")
        
        if "quota" in error_msg.lower():
            st.error("Limite de cota excedido. Tente novamente mais tarde.")
        else:
            st.error("Possíveis causas: Problemas de permissão ou conexão")
            
    except Exception as e:
        st.error(f"❌ ERRO INESPERADO: {str(e)}")
        st.code(traceback.format_exc())

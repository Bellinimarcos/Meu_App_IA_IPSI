import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback

# ========== CONFIGURAÇÃO MANUAL DOS SECRETS ==========
# (Para contornar problemas do Streamlit Cloud)

# Dados da conta de serviço (cole os valores do secrets.toml aqui)
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "ipsi-questionario",
    "private_key_id": "8dff3072ce600f724d7fdf895291e37dae40c0b9",
    "private_key": """
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC1ArtlhWyjt00P
9QCI4h84Pk+3v6f15nk9o43pDXYTgbWgesrN7uuSRtEx7KgDx2HC37X+NgGjZx2O
KvoUfzJc1l9SF9nk7RWqxUbfHIMSmpvHt/9YQVD2Tmksdr0OesvzNmiVGJ2gFiwM
w2N1VbTNcsIQIUQMvJP4UnkCYz20jQBp3oYOy4RO44HWy5FHS3SsW+Z69rrJ8J6G
1Wqk4KcDasGM1ULNpvxYDCGergVgKl2IP3Kfz4DWmmZyz1B4qotlr21kjA+ureub
Qr7xh+bqtManmU9GvAHocfsCKgZ+9aduhkw9KUy5DuNRdN2Vd8JjJNzikQ2cDs8P
LFEBPjJvAgMBAAECggEAG3DHwPBfqQKzmNzZpmav40JgVROlyPDrZgKX6QHZ6cN1
qdeY9sF8Doepf18y6f5oCHdf6yL7z5jlEaAxRjncLtfEHo6wFnTcnoVb+kcjwFvA
4Z+NWFnv208awZtZ4MqRMD80zo7V7Sa/VHYAa2bBSziqSRtfP2u30OLhJmauEY3h
arOm4AHkL5ULC8ASM84GnwtPO0iBxUUDDMXMcrtt1Ti6LQBnZTv1ohRtFWURkiLm
zwxSwwwW7Jil8AQdFPJYXPMYkVhvOVSPuTC7i9IketUqXRBf5bMnfma75IzIt0dE
NyzHdywBNL1BN5ALNOyZQaAHlB6DvbUbqacLOI02zQKBgQD2VxyAh5mBiBEEPXfm
BcaZNUgd6tU2WiXlTFJPqiJHN1/VrtR8dcTGQqtuCDnZNICLt/kvqNL7JMpd2Glp
Ec8xioJTS4Byy41dVG3IOX0Oxo3owoFdakoOcEpagWzMmlRJt3OZIlCzmU5gCZqh
gTcoaKCLhZsiV7YKKjZDBLHBOwKBgQC8G88Xk/+/SgN6pTTr54WKwbI3zSHw6/gM
VB2YPJPNEj05wDXADXWQR7MDs70J0nRIBolWj0cgkAweAcuvgL3h96MPDLCj9S65
7IPj4/HO4x7g05DYRKm27aAPFEXBL4o4BPm/y+EhU6KOMYTDQQB5usmeC91wipZc
KoJ761EAXQKBgQCChT1QzIgFHbcGbBsvAThszNJdJ6O4nKMfjwS9uQNYgHqCmZN0
LmIIOiLitfEQqMTDQsMBAY5oCuI+Pv/677i8IwtSXtq7+CX6oVVZlTwxq/pcrVIl
0L9UTyLWOWUQM2UdedoB9TCVOFFSiUQo9nHnMyh9RFkiJR8K27rMX5xfKQKBgDCM
NMxvA+hIn9E9ZgUkQZDoIKjKJmJZZDE6XFD4AWVBuc93zed9EcRk3MytzLIGQMB9
/1/5pm++/YGZEQqAfYEeOlUd/1CxbJfLdNaR88xjTYrUz2MhhXOSrGZ34vDS5idD
EXnwkm/Zd/Ce0xbZZdgE3xgNE9+BxQCQcBCvUL55AoGBAOvh3TVrJ5Uilfj8L5Sl
g76S8LszvN5s/R/SybCpadDadX0jpvAIFtZWvgfLTB9yyv4ulQhgngoYTOfYG7V+
Q/eFB1cfcNp7X9Mn3ts51zpJWMb+tAL8TdJgxJdMpv5NFKykIM23T8Oc3DA7H/+N
JsLpbJ+WP3twngZGYBKaMs0s
-----END PRIVATE KEY-----
""",
    "client_email": "planilha-ia-ipsi@ipsi-questionario.iam.gserviceaccount.com",
    "client_id": "107276742723863349608",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/planilha-ia-ipsi%40ipsi-questionario.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# ID da planilha (cole o valor do secrets.toml aqui)
SPREADSHEET_ID = "1V2S5zWmcK8FkKIajZU5SrpSpbUp1gVO-RzQnxTAuLlg"

# ========== CONEXÃO COM GOOGLE SHEETS ==========
try:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Criar credenciais a partir do dicionário fixo
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Abrir planilha usando o ID fixo
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
                st.sidebar.info(f"Total de respostas: {len(worksheet.get_all_values()) - 1}")
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")

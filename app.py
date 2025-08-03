import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback

# ========== CONFIGURAÇÃO MANUAL DAS CREDENCIAIS ==========
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

SPREADSHEET_ID = "1V2S5zWmcK8FkKIajZU5SrpSpbUp1gVO-RzQnxTAuLlg"

# ========== CONEXÃO COM GOOGLE SHEETS ==========
try:
    # Configurar escopos
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Criar credenciais
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Abrir planilha
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet("Tabela Gemini")
    
    # Mensagem de sucesso na sidebar
    st.sidebar.success("✅ Conectado ao Google Sheets!")
    st.sidebar.info(f"Planilha: {spreadsheet.title}")
    st.sidebar.info(f"Aba: {worksheet.title}")
    st.sidebar.info(f"Total de respostas: {len(worksheet.get_all_values()) - 1}")

except Exception as e:
    st.sidebar.error("🔴 Erro de conexão!")
    st.error(f"Falha ao conectar com o Google Sheets: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()

# ========== DESIGN DO QUESTIONÁRIO ==========
# Configuração da página
st.set_page_config(
    page_title="Questionário de Satisfação",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Cabeçalho com imagem
st.image("https://cdn.pixabay.com/photo/2016/11/30/20/44/survey-1874664_1280.png", 
         width=100, caption="Sua opinião é importante!")
st.title("📋 Questionário de Satisfação")
st.markdown("""
    <style>
        .css-18e3th9 {padding: 2rem 1rem 10rem;}
        .st-b7 {background-color: #f0f2f6;}
        .st-c0 {background-color: white;}
        .css-1v3fvcr {margin-top: -50px;}
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            font-size: 16px;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 5px;
            border: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    **Preencha este breve questionário para nos ajudar a melhorar nossos serviços.**
    Sua opinião é valiosa e será mantida em sigilo.
""")

# Formulário organizado em seções
with st.form("questionario_form", clear_on_submit=True):
    # Seção 1: Informações Pessoais
    st.subheader("🔒 Informações Pessoais")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome completo*", placeholder="Seu nome completo")
    with col2:
        email = st.text_input("Email*", placeholder="seu@email.com")
    
    # Seção 2: Avaliação
    st.subheader("⭐ Avaliação do Serviço")
    st.markdown("Como você avalia nossa prestação de serviço?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        atendimento = st.slider("Atendimento", 1, 5, 3)
    with col2:
        qualidade = st.slider("Qualidade", 1, 5, 3)
    with col3:
        tempo_resposta = st.slider("Tempo de resposta", 1, 5, 3)
    
    # Seção 3: Comentários
    st.subheader("💬 Comentários e Sugestões")
    comentario = st.text_area(
        "Tem alguma sugestão ou observação? Nos conte!",
        placeholder="O que podemos fazer para melhorar?",
        height=150
    )
    
    # Termos e condições
    st.markdown("---")
    aceito = st.checkbox("Declaro que as informações fornecidas são verdadeiras*")
    
    # Notas
    st.caption("\* Campos obrigatórios")
    
    # Botão de envio centralizado
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    enviado = st.form_submit_button("Enviar Minhas Respostas", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Processar envio
if enviado:
    # Validar campos obrigatórios
    erros = []
    if not nome: erros.append("Nome completo")
    if not email: erros.append("Email")
    if not aceito: erros.append("Aceite dos termos")
    
    if erros:
        st.error(f"Por favor, preencha os campos obrigatórios: {', '.join(erros)}")
    else:
        with st.spinner("Salvando suas respostas..."):
            try:
                # Preparar dados
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nova_linha = [
                    timestamp, 
                    nome, 
                    email, 
                    atendimento, 
                    qualidade, 
                    tempo_resposta, 
                    comentario
                ]
                
                # Salvar na planilha
                worksheet.append_row(nova_linha)
                
                # Mensagem de sucesso
                st.success("✅ Respostas salvas com sucesso! Obrigado pela sua contribuição.")
                st.balloons()
                
                # Atualizar sidebar
                st.sidebar.info(f"Total de respostas: {len(worksheet.get_all_values()) - 1}")
                
                # Mensagem adicional
                st.markdown("""
                    <div style="background-color:#e6f7ff; padding:20px; border-radius:10px; margin-top:20px;">
                        <h3>🎁 Agradecimento Especial!</h3>
                        <p>Como forma de agradecimento, gostaríamos de oferecer:</p>
                        <ul>
                            <li>Desconto de 10% em seu próximo serviço</li>
                            <li>Acesso antecipado a novos recursos</li>
                        </ul>
                        <p>Enviaremos os detalhes para o email fornecido.</p>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar respostas: {str(e)}")
                st.code(traceback.format_exc())

# Rodapé
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9em;">
        <p>© 2023 IPSI Questionário | Todos os direitos reservados</p>
        <p>As informações fornecidas serão usadas apenas para melhorar nossos serviços</p>
    </div>
""", unsafe_allow_html=True)

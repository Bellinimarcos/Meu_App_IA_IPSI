import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import traceback
import base64

# --- DEFINIÇÃO DO QUESTIONÁRIO E DA ESCALA DE LIKERT ---
questionario = [
    {
        "id": "q1",
        "pergunta": "Com que frequência você se sente ansioso(a) ou preocupado(a) em relação às suas responsabilidades, prazos ou tarefas no trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q2",
        "pergunta": "Você se sente sobrecarregado(a) pela pressão ou volume de tarefas que precisa realizar no trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q3",
        "pergunta": "Você tem dificuldade em gerenciar suas tarefas ou tempo devido à ansiedade?",
        "tipo": "likert"
    },
    {
        "id": "q4",
        "pergunta": "Você se preocupa com a possibilidade de cometer erros no trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q5",
        "pergunta": "Você costuma levar trabalho para casa (física ou mentalmente) devido à ansiedade ou preocupações?",
        "tipo": "likert"
    },
    {
        "id": "q6",
        "pergunta": "Quando você sente ansiedade, ela costuma ser muito intensa?",
        "tipo": "likert"
    },
    {
        "id": "q7",
        "pergunta": "Você experimenta sintomas físicos de ansiedade, como batimentos cardíacos acelerados, sudorese, tremores, tensão muscular ou dores?",
        "tipo": "likert"
    },
    {
        "id": "q8",
        "pergunta": "Você tem dificuldade em se concentrar devido à ansiedade?",
        "tipo": "likert"
    },
    {
        "id": "q9",
        "pergunta": "Você se sente irritado(a) ou impaciente quando está ansioso(a)?",
        "tipo": "likert"
    },
    {
        "id": "q10",
        "pergunta": "Você tem dificuldade em controlar seus pensamentos ansiosos ou preocupações?",
        "tipo": "likert"
    },
    {
        "id": "q11",
        "pergunta": "Você tem dificuldade para dormir ou manter o sono devido a preocupações (gerais ou relacionadas ao trabalho)?",
        "tipo": "likert"
    },
    {
        "id": "q12",
        "pergunta": "Você se sente ansioso(a) ao interagir com colegas, superiores ou antes de reuniões/apresentações no trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q13",
        "pergunta": "Você evita situações sociais no trabalho devido à ansiedade?",
        "tipo": "likert"
    },
    {
        "id": "q14",
        "pergunta": "Você se sente ansioso(a) durante mudanças, novas tarefas ou quando recebe feedback sobre seu desempenho no trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q15",
        "pergunta": "Você se sente angustiado(a) por não conseguir cumprir suas obrigações ou preocupado(a) excessivamente com o que os outros pensam sobre você no ambiente de trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q16",
        "pergunta": "Você sente que sua saúde mental está sendo afetada pelas demandas do trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q17",
        "pergunta": "Você se sente desmotivado(a), sem esperança ou que seu trabalho não tem significado/propósito?",
        "tipo": "likert"
    },
    {
        "id": "q18",
        "pergunta": "Você se sente isolado(a) ou desconectado(a) dos seus colegas no trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q19",
        "pergunta": "Você questiona seu valor ou competência no ambiente de trabalho?",
        "tipo": "likert"
    },
    {
        "id": "q20",
        "pergunta": "Você sente que suas necessidades emocionais não são atendidas no trabalho?",
        "tipo": "likert"
    }
]

escala_likert_opcoes = {
    0: "Nunca",
    1: "Raramente",
    2: "Às vezes",
    3: "Frequentemente",
    4: "Sempre"
}

# --- FUNÇÃO PARA ANALISAR AS RESPOSTAS E DAR FEEDBACK ---
def analisar_respostas(respostas_do_usuario, questionario):
    pontuacao_total = sum(respostas_do_usuario.values())
    pontuacao_maxima = len(questionario) * 4

    st.subheader("Análise Inicial das Suas Respostas")
    st.write(f"Sua pontuação total é: {pontuacao_total} (de um máximo de {pontuacao_maxima})")

    if pontuacao_total <= 20:
        st.success("As suas respostas indicam que raramente ou nunca sente ansiedade ou angústia relacionadas com o trabalho. Isso é um bom sinal de bem-estar!")
        st.info("Continue atento(a) ao seu equilíbrio e procure manter hábitos saudáveis.")
    elif pontuacao_total <= 45:
        st.warning("As suas respostas sugerem que ocasionalmente experiencia ansiedade ou angústia no trabalho.")
        st.info("É importante observar esses sentimentos e considerar algumas estratégias para gerir o stress, como exercícios físicos, técnicas de relaxamento ou pausas no trabalho.")
    elif pontuacao_total <= 65:
        st.error("As suas respostas indicam que frequentemente sente ansiedade ou angústia no trabalho, com algum impacto na sua rotina.")
        st.info("Recomendamos que preste mais atenção a esses sinais. Conversar com um amigo de confiança, um familiar ou um líder no trabalho pode ser um bom primeiro passo. **Considerar o apoio de um profissional de saúde mental também seria muito benéfico.**")
    else:
        st.error("As suas respostas indicam um nível significativo e frequente de ansiedade e angústia relacionadas com o trabalho, impactando diversas áreas da sua vida.")
        st.info("**Recomendamos vivamente que procure um profissional de saúde mental** para uma avaliação mais aprofundada e apoio adequado. Não hesite em procurar ajuda.")

    st.markdown("---")
    st.subheader("Observações com base em respostas específicas:")
    if respostas_do_usuario.get('q6', 0) >= 3:
        st.write("- A intensidade da sua ansiedade é um ponto de atenção importante.")
    if respostas_do_usuario.get('q7', 0) >= 3:
        st.write("- Os sintomas físicos que descreveu são comuns na ansiedade e merecem atenção.")
    if respostas_do_usuario.get('q11', 0) >= 3:
        st.write("- A dificuldade em dormir é um sinal significativo e pode estar relacionada com as suas preocupações.")
    if respostas_do_usuario.get('q16', 0) >= 3:
        st.write("- Sentir que a saúde mental é afetada pelas exigências do trabalho é um sinal claro de que algo precisa ser ajustado.")
    if respostas_do_usuario.get('q17', 0) >= 3:
        st.write("- A desmotivação ou a sensação de falta de propósito no trabalho podem indicar burnout ou esgotamento.")

    st.markdown("---")
    st.info("Lembre-se: Esta é uma análise inicial baseada nas suas respostas e não substitui uma avaliação profissional. Se estiver a passar por dificuldades, procure sempre um especialista.")

    return pontuacao_total

# --- FUNÇÃO PARA GUARDAR AS RESPOSTAS NO GOOGLE SHEETS ---
def salvar_respostas_no_sheets(respostas_do_usuario, pontuacao_total):
    try:
        # CORREÇÃO APLICADA AQUI:
        # Este bloco agora lê cada segredo individualmente,
        # que é o formato correto do seu ficheiro secrets.toml.
        gcp_service_account_info = {
            "type": st.secrets["GCP_TYPE"],
            "project_id": st.secrets["GCP_PROJECT_ID"],
            "private_key_id": st.secrets["GCP_PRIVATE_KEY_ID"],
            "private_key": base64.b64decode(st.secrets["GCP_PRIVATE_KEY_BASE64"]).decode('utf-8'),
            "client_email": st.secrets["GCP_CLIENT_EMAIL"],
            "client_id": st.secrets["GCP_CLIENT_ID"],
            "auth_uri": st.secrets["GCP_AUTH_URI"],
            "token_uri": st.secrets["GCP_TOKEN_URI"],
            "auth_provider_x509_cert_url": st.secrets["GCP_AUTH_PROVIDER_X509_CERT_URL"],
            "client_x509_cert_url": st.secrets["GCP_CLIENT_X509_CERT_URL"],
            "universe_domain": st.secrets["GCP_UNIVERSE_DOMAIN"]
        }
        
        creds = Credentials.from_service_account_info(
            gcp_service_account_info,
            scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
        
        try:
            # Apontando para a aba correta "Tabela Gemini"
            sheet = spreadsheet.worksheet("Tabela Gemini")

        except gspread.exceptions.WorksheetNotFound:
            st.error("ERRO: Não foi possível encontrar a aba chamada 'Tabela Gemini'. Verifique se o nome está exatamente correto.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_dados = [timestamp]
        
        for i in range(1, 21):
            key = f'q{i}'
            linha_dados.append(respostas_do_usuario.get(key, ''))
        
        linha_dados.append(pontuacao_total)

        # Usando a linha de dados original do questionário
        sheet.append_row(linha_dados)
        st.success("Respostas guardadas com sucesso para análise interna!")
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("ERRO: A planilha não foi encontrada. Verifique se o ID da planilha está correto e se você partilhou a planilha com o email do service account.")
    except Exception as e:
        st.error("Ocorreu um erro inesperado ao guardar as suas respostas.")
        st.error(f"Detalhes do erro: {e}")
        traceback.print_exc()

# --- LÓGICA DO APLICATIVO STREAMLIT ---
st.title("Questionário Inicial de Avaliação de Ansiedade e Angústia")
st.write("Por favor, responda às seguintes perguntas de acordo com a sua experiência nas **últimas duas semanas**.")
st.markdown("---")
st.write("**Utilize a escala de 0 a 4, onde:**")
for valor, texto in escala_likert_opcoes.items():
    st.write(f"- **{valor}** = {texto}")
st.markdown("---")

if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

for i, item_pergunta in enumerate(questionario):
    pergunta_id = item_pergunta["id"]
    pergunta_texto = item_pergunta["pergunta"]
    
    resposta_selecionada = st.radio(
        f"{i+1}. {pergunta_texto}",
        options=list(escala_likert_opcoes.keys()),
        format_func=lambda x: escala_likert_opcoes[x],
        key=f"q_{pergunta_id}",
        horizontal=True
    )
    st.session_state.respostas[pergunta_id] = resposta_selecionada

if st.button("Obter Análise e Guardar Respostas"):
    pontuacao = analisar_respostas(st.session_state.respostas, questionario)
    if pontuacao is not None:
        salvar_respostas_no_sheets(st.session_state.respostas, pontuacao)

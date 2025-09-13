import streamlit as st
import datetime
from streamlit_autorefresh import st_autorefresh

# --- Configuração da Página ---
st.set_page_config(
    page_title="Checklist do Casamento | Daniela & Thiago",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS Customizado para um Visual Elegante ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;700&display=swap');

body {
    background-color: #f0f2f6;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.stApp {
    font-family: 'Inter', sans-serif;
}

.main-title {
    text-align: center;
    color: #333;
}

.countdown-container {
    display: flex;
    justify-content: center;
    gap: 2rem;
    text-align: center;
    padding: 2rem;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.countdown-box {
    display: flex;
    flex-direction: column;
}

.countdown-number {
    font-size: 3rem;
    font-weight: bold;
    color: #d81b60; /* Um tom de rosa */
}

.countdown-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    color: #666;
}

.stProgress > div > div > div > div {
    background-image: linear-gradient(to right, #f48fb1, #d81b60);
}

.stExpander {
    border: 1px solid #e0e0e0 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

</style>
""", unsafe_allow_html=True)


# --- Dados do Checklist ---
checklist_data = {
    "Fase 1: 8 a 7 Meses Antes (Set/25 a Out/25) - Planejamento Inicial": [
        {'id': 'definir-orcamento', 'text': 'Definir o Orçamento Geral do Casamento.'},
        {'id': 'lista-convidados-preliminar', 'text': 'Criar a Lista Preliminar de Convidados.'},
        {'id': 'escolher-padrinhos', 'text': 'Convidar Padrinhos e Madrinhas (máx. 3 casais por noivo, católicos e casados na igreja).'},
        {'id': 'contato-paroquia', 'text': 'Contato Inicial com a Paróquia: Agendar a nova data (02/05/2026).'},
        {'id': 'ponto-atencao-padre', 'text': '⚠️ Agendar conversa com o Padre Carlos para confirmar o religioso com efeito civil e tirar dúvidas sobre a viuvez.', 'is_note': True},
        {'id': 'agendar-curso-noivos', 'text': 'Pesquisar e se inscrever no Curso de Noivos (fazer em outra paróquia).'},
        {'id': 'confirmar-salao', 'text': 'Confirmar a reserva do salão anexo da igreja para a recepção.'},
        {'id': 'iniciar-docs', 'text': 'Começar a solicitar os documentos com calma (Batistérios atualizados, etc.).'},
    ],
    "Fase 2: 6 a 5 Meses Antes (Nov/25 a Dez/25) - Fornecedores e Viagem": [
        {'id': 'foto-video', 'text': 'Conversar e fechar com a amiga fotógrafa (repassar regras da igreja).'},
        {'id': 'musica-cerimonia', 'text': 'Conversar e fechar com os amigos músicos (repertório apenas religioso).'},
        {'id': 'decoracao', 'text': 'Contratar florista/decoração (repassar regras: 4 arranjos, sem arcos, etc.).'},
        {'id': 'bolo-doces', 'text': 'Pesquisar e agendar degustações de bolo e doces.'},
        {'id': 'definir-lua-de-mel', 'text': 'Lua de Mel: Definir o Destino (Nacional).'},
        {'id': 'reservar-lua-de-mel', 'text': 'Lua de Mel: Reservar Passagens e Hotéis para garantir o preço.'},
    ],
    "Fase 3: 4 a 3 Meses Antes (Jan/26 a Fev/26) - Trajes, Convites e Detalhes": [
        {'id': 'vestido-noiva', 'text': 'Vestido da Noiva: Iniciar pesquisa e provas (lembrar regras da paróquia).'},
        {'id': 'traje-noivo', 'text': 'Traje do Noivo: Iniciar pesquisa.'},
        {'id': 'dia-noiva-profissional', 'text': 'Pesquisar e contratar profissional para o Dia da Noiva em casa.'},
        {'id': 'criar-site', 'text': 'Criar e configurar o Site dos Noivos (Lejour).'},
        {'id': 'design-convites', 'text': 'Definir o design dos convites.'},
        {'id': 'lista-convidados-final', 'text': 'Finalizar a Lista de Convidados.'},
        {'id': 'encomendar-bolo-doces', 'text': 'Encomendar Bolo e Docinhos.'},
        {'id': 'encomendar-tercos-ns', 'text': 'Encomendar os terços de Nossa Senhora das Lágrimas.'},
        {'id': 'material-tercos-proprios', 'text': 'Comprar material para a produção dos terços da Sagrada Face e Sto. Antônio.'},
    ],
    "Fase 4: 2 Meses Antes (Março/2026) - Burocracia Final": [
        {'id': 'habilitacao-cartorio', 'text': 'Dar Entrada no Processo de Habilitação no Cartório (Levar todos os documentos).'},
        {'id': 'docs-noiva-cartorio', 'text': 'Daniela: levar Certidão de Casamento anterior com averbação do óbito, Certidão de Óbito e andamento do inventário.', 'is_note': True},
        {'id': 'publicacao-proclamas', 'text': 'Aguardar a publicação dos proclamas no cartório (15 dias).'},
        {'id': 'retirar-habilitacao', 'text': 'Retirar a Certidão de Habilitação no Cartório.'},
        {'id': 'marcar-entrevista-padre', 'text': 'Marcar Entrevista com o Padre (Processo Matrimonial - 70 dias antes).'},
        {'id': 'entregar-habilitacao-paroquia', 'text': 'Entregar a Certidão de Habilitação do Cartório na Paróquia.'},
        {'id': 'imprimir-enviar-convites', 'text': 'Imprimir e começar a enviar/entregar os convites.'},
    ],
    "Fase 5: 1 Mês Antes (Abril/2026) - Reta Final": [
        {'id': 'confirmar-presenca-rsvp', 'text': 'Confirmar Presença (RSVP) e fechar número de convidados.'},
        {'id': 'reuniao-final-fornecedores', 'text': 'Reunião Final com todos os fornecedores.'},
        {'id': 'prova-final-trajes', 'text': 'Prova Final do Vestido e Terno.'},
        {'id': 'definir-leituras-musicas', 'text': 'Definir com o Padre as leituras e músicas da cerimônia.'},
        {'id': 'ensaio-igreja', 'text': 'Agendar e realizar ensaio na igreja com pais e padrinhos (se necessário).'},
        {'id': 'prova-cabelo-maquiagem', 'text': 'Fazer teste final de cabelo e maquiagem.'},
    ],
    "Na Semana do Casamento": [
        {'id': 'buscar-trajes', 'text': 'Buscar o Vestido e o Terno.'},
        {'id': 'confirmar-horarios-todos', 'text': 'Confirmar horário com TODOS os profissionais (foto, make, bolo, etc).'},
        {'id': 'finalizar-tercos', 'text': 'Finalizar a produção e embalagem dos terços.'},
        {'id': 'organizar-malas-lua-de-mel', 'text': 'Organizar as Malas da Lua de Mel.'},
        {'id': 'separar-documentos-aliancas', 'text': 'Separar em uma pasta todos os documentos e as alianças.'},
        {'id': 'relaxar', 'text': 'Descansar e relaxar! Delegar as últimas tarefas.'},
    ],
    "No Grande Dia: 02/05/2026": [
        {'id': 'cafe-reforcado', 'text': 'Tomar um café da manhã reforçado e se hidratar.'},
        {'id': 'chegar-pontualmente', 'text': 'Chegar Pontualmente na Igreja.'},
        {'id': 'aproveitar', 'text': 'Aproveitar, celebrar e viver cada segundo!'},
    ],
    "Pós-Casamento": [
        {'id': 'pegar-termo-igreja', 'text': 'Pegar o Termo do Casamento Religioso com Efeito Civil na Igreja.'},
        {'id': 'prazo-90-dias', 'text': '✅ REGISTRAR NO CARTÓRIO (PRAZO DE 90 DIAS!): Levar o Termo ao cartório para emitir a Certidão de Casamento definitiva.', 'is_note': True},
        {'id': 'alterar-documentos', 'text': 'Providenciar alteração de documentos (se houver mudança de nome).'},
        {'id': 'agradecimentos', 'text': 'Enviar cartões ou mensagens de agradecimento.'},
    ]
}

# --- Inicialização do Estado da Sessão ---
if 'tasks_status' not in st.session_state:
    st.session_state.tasks_status = {task['id']: False for phase in checklist_data.values() for task in phase if not task.get('is_note')}

# --- Cabeçalho ---
st.markdown('<h1 class="main-title">Daniela & Thiago</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #555;">Nosso caminho até 02 de Maio de 2026</p>', unsafe_allow_html=True)
st.markdown("---")


# --- Barra de Progresso ---
total_tasks = len(st.session_state.tasks_status)
completed_tasks = sum(1 for status in st.session_state.tasks_status.values() if status)
progress = completed_tasks / total_tasks if total_tasks > 0 else 0

st.subheader("Progresso do Planejamento")
st.progress(progress)
st.markdown(f"<p style='text-align: right; color: #555;'>{completed_tasks} de {total_tasks} tarefas concluídas ({progress:.0%})</p>", unsafe_allow_html=True)


# --- Contagem Regressiva ---
st.subheader("Contagem Regressiva para o Grande Dia")
wedding_date = datetime.datetime(2026, 5, 2, 16, 0, 0)

# Usamos st.empty para criar um container que pode ser atualizado dinamicamente
countdown_placeholder = st.empty()

# --- Layout do Checklist ---
st.subheader("Nosso Checklist Detalhado")

for phase, tasks in checklist_data.items():
    with st.expander(f"🗓️ {phase}", expanded=(phase == "Fase 1: 8 a 7 Meses Antes (Set/25 a Out/25) - Planejamento Inicial")):
        for task in tasks:
            if task.get('is_note'):
                st.info(task['text'])
            else:
                st.session_state.tasks_status[task['id']] = st.checkbox(
                    task['text'], 
                    value=st.session_state.tasks_status.get(task['id'], False),
                    key=task['id']
                )

# --- Lógica da Contagem Regressiva (Corrigida) ---
# Roda a cada segundo para atualizar o contador sem usar 'while True'
st_autorefresh(interval=1000, key="countdownrefresh")

now = datetime.datetime.now()
remaining = wedding_date - now

if remaining.total_seconds() < 0:
    with countdown_placeholder.container():
        st.markdown(
            '<div class="countdown-container"><span style="font-size: 2rem; font-weight: bold; color: #d81b60;">Feliz Casamento!</span></div>',
            unsafe_allow_html=True
        )
else:
    days, seconds = remaining.days, remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    with countdown_placeholder.container():
        st.markdown(
            f"""
            <div class="countdown-container">
                <div class="countdown-box">
                    <span class="countdown-number">{days}</span>
                    <span class="countdown-label">Dias</span>
                </div>
                <div class="countdown-box">
                    <span class="countdown-number">{hours}</span>
                    <span class="countdown-label">Horas</span>
                </div>
                <div class="countdown-box">
                    <span class="countdown-number">{minutes}</span>
                    <span class="countdown-label">Minutos</span>
                </div>
                <div class="countdown-box">
                    <span class="countdown-number">{seconds}</span>
                    <span class="countdown-label">Segundos</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

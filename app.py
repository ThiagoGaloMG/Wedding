# Lembre-se de criar o arquivo requirements.txt para que esta linha funcione!
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
/* Importando as fontes do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Edwardian+Script+ITC&family=Inter:wght@400;500;700&display=swap');

body {
    background-color: #f0f2f6;
}

.stApp {
    font-family: 'Inter', sans-serif;
}

/* --- ESTILOS DO CABEÇALHO --- */

.wedding-names {
    font-family: 'Edwardian Script ITC', cursive; /* Fonte elegante e sofisticada */
    font-size: 6rem; /* Ajuste no tamanho para a nova fonte */
    font-weight: 400;
    text-align: center;
    color: #c2185b; /* Um tom de rosa mais escuro e sofisticado */
    margin-bottom: -15px; /* Ajuste para aproximar do texto abaixo */
}

.wedding-date {
    font-family: 'Inter', sans-serif;
    text-align: center;
    font-size: 1.2rem;
    color: #555;
    letter-spacing: 1px; /* Espaçamento sutil entre as letras */
}

/* --- DEMAIS ESTILOS --- */

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
    color: #d81b60;
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


# --- Dados do Checklist (ATUALIZADOS COM DATAS ESPECÍFICAS) ---
checklist_data = {
    "Fase 1: 12 a 10 Meses Antes (Set/25 a Nov/25) - Planejamento Inicial": [
        {'id': 'definir-orcamento', 'text': 'Definir o Orçamento Geral do Casamento.'},
        {'id': 'lista-convidados-preliminar', 'text': 'Criar a Lista Preliminar de Convidados.'},
        {'id': 'escolher-padrinhos', 'text': 'Convidar Padrinhos e Madrinhas (máx. 3 casais por noivo, católicos e casados na igreja).'},
        {'id': 'contato-paroquia', 'text': 'Contato Inicial com a Paróquia: Agendar a data religiosa (12/09/2026).'},
        {'id': 'ponto-atencao-padre', 'text': '⚠️ Agendar conversa com o Padre Carlos para tirar dúvidas sobre a viuvez e o processo religioso.', 'is_note': True},
        {'id': 'agendar-curso-noivos', 'text': 'Pesquisar e se inscrever no Curso de Noivos (fazer em outra paróquia).'},
        {'id': 'confirmar-salao', 'text': 'Confirmar a reserva do salão anexo da igreja para a recepção.'},
        {'id': 'definir-lua-de-mel', 'text': 'Lua de Mel: Definir o Destino (Nacional).'},
    ],
    "Fase 2: 9 a 7 Meses Antes (Dez/25 a Fev/26) - Fornecedores Principais": [
        {'id': 'foto-video', 'text': 'Conversar e fechar com a amiga fotógrafa (repassar regras da igreja).'},
        {'id': 'musica-cerimonia', 'text': 'Conversar e fechar com os amigos músicos (repertório apenas religioso).'},
        {'id': 'decoracao', 'text': 'Contratar florista/decoração (repassar regras: 4 arranjos, sem arcos, etc.).'},
        {'id': 'bolo-doces', 'text': 'Pesquisar e agendar degustações de bolo e doces.'},
        {'id': 'reservar-lua-de-mel', 'text': 'Lua de Mel: Reservar Passagens e Hotéis para garantir o preço.'},
        {'id': 'pesquisar-vestido-noiva', 'text': 'Vestido da Noiva: Iniciar pesquisa e provas (lembrar regras da paróquia).'},
        {'id': 'pesquisar-traje-noivo', 'text': 'Traje do Noivo: Iniciar pesquisa.'},
        {'id': 'pesquisar-dia-noiva', 'text': 'Pesquisar profissional para o Dia da Noiva em casa.'},
    ],
    "Fase 3: 6 a 4 Meses Antes (Mar/26 a Mai/26) - Trajes, Convites e Detalhes": [
        {'id': 'contratar-vestido-noiva', 'text': 'Contratar/Comprar o Vestido da Noiva.'},
        {'id': 'contratar-traje-noivo', 'text': 'Contratar/Comprar o Traje do Noivo.'},
        {'id': 'contratar-dia-noiva-profissional', 'text': 'Contratar profissional para o Dia da Noiva em casa.'},
        {'id': 'criar-site', 'text': 'Criar e configurar o Site dos Noivos (Lejour).'},
        {'id': 'design-convites', 'text': 'Definir o design dos convites.'},
        {'id': 'lista-convidados-final', 'text': 'Finalizar a Lista de Convidados.'},
        {'id': 'encomendar-bolo-doces', 'text': 'Encomendar Bolo e Docinhos.'},
        {'id': 'encomendar-tercos-ns', 'text': 'Encomendar os terços de Nossa Senhora das Lágrimas.'},
        {'id': 'material-tercos-proprios', 'text': 'Comprar material para a produção dos terços da Sagrada Face e Sto. Antônio.'},
    ],
    "Fase 4: 3 a 2 Meses Antes (Jun/26 a Jul/26) - Burocracia Civil e Religiosa": [
        {'id': 'solicitar-batisterios', 'text': '⚠️ Solicitar os Batistérios ATUALIZADOS para fins matrimoniais (Prazo para solicitar: 14/06/2026).'},
        {'id': 'habilitacao-cartorio', 'text': 'Dar Entrada no Processo de Habilitação para o Casamento Civil no Cartório (Prazo: 14/06/2026).'},
        {'id': 'docs-noiva-cartorio', 'text': 'Daniela: levar Certidão de Casamento anterior com averbação do óbito, Certidão de Óbito e andamento do inventário.', 'is_note': True},
        {'id': 'agendar-civil', 'text': 'Agendar a data do Casamento Civil no Cartório.'},
        {'id': 'realizar-civil', 'text': 'Realizar o Casamento Civil e retirar a Certidão (Realizar antes de 10/09/2026).'},
        {'id': 'marcar-entrevista-padre', 'text': 'Marcar Entrevista com o Padre para o Processo Matrimonial (Prazo: 04/07/2026).'},
        {'id': 'entregar-docs-paroquia', 'text': 'Entregar os documentos do processo religioso na paróquia (durante a entrevista).'},
        {'id': 'imprimir-enviar-convites', 'text': 'Imprimir e começar a enviar/entregar os convites.'},
    ],
    "Fase 5: 1 Mês Antes (Agosto/2026) - Reta Final": [
        {'id': 'confirmar-presenca-rsvp', 'text': 'Confirmar Presença (RSVP) e fechar número de convidados (Prazo: 13/08/2026).'},
        {'id': 'reuniao-final-fornecedores', 'text': 'Reunião Final com todos os fornecedores.'},
        {'id': 'prova-final-trajes', 'text': 'Prova Final do Vestido e Terno.'},
        {'id': 'definir-leituras-musicas', 'text': 'Definir com o Padre as leituras e músicas da cerimônia.'},
        {'id': 'ensaio-igreja', 'text': 'Agendar e realizar ensaio na igreja com pais e padrinhos (se necessário).'},
        {'id': 'prova-cabelo-maquiagem', 'text': 'Fazer teste final de cabelo e maquiagem.'},
    ],
    "Na Semana do Casamento": [
        {'id': 'entregar-certidao-civil', 'text': '⚠️ ENTREGAR A XEROX DA CERTIDÃO CIVIL NA PARÓQUIA (Prazo: 10/09/2026).', 'is_note': True},
        {'id': 'buscar-trajes', 'text': 'Buscar o Vestido e o Terno.'},
        {'id': 'confirmar-horarios-todos', 'text': 'Confirmar horário com TODOS os profissionais (foto, make, bolo, etc).'},
        {'id': 'finalizar-tercos', 'text': 'Finalizar a produção e embalagem dos terços.'},
        {'id': 'organizar-malas-lua-de-mel', 'text': 'Organizar as Malas da Lua de Mel.'},
        {'id': 'separar-documentos-aliancas', 'text': 'Separar em uma pasta os documentos para o dia e as alianças.'},
        {'id': 'relaxar', 'text': 'Descansar e relaxar! Delegar as últimas tarefas.'},
    ],
    "No Grande Dia: 12/09/2026": [
        {'id': 'cafe-reforcado', 'text': 'Tomar um café da manhã reforçado e se hidratar.'},
        {'id': 'chegar-pontualmente', 'text': 'Chegar Pontualmente na Igreja.'},
        {'id': 'aproveitar', 'text': 'Aproveitar, celebrar e viver cada segundo!'},
    ],
    "Pós-Casamento": [
        {'id': 'alterar-documentos', 'text': 'Providenciar alteração de documentos (se houver mudança de nome).'},
        {'id': 'agradecimentos', 'text': 'Enviar cartões ou mensagens de agradecimento.'},
    ]
}

# --- Inicialização do Estado da Sessão ---
if 'tasks_status' not in st.session_state:
    st.session_state.tasks_status = {task['id']: False for phase in checklist_data.values() for task in phase if not task.get('is_note')}

# --- Cabeçalho ---
st.markdown('<h1 class="wedding-names">Daniela & Thiago</h1>', unsafe_allow_html=True)
st.markdown('<p class="wedding-date">Nosso caminho até 12 de Setembro de 2026</p>', unsafe_allow_html=True)
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
wedding_date = datetime.datetime(2026, 9, 12, 16, 0, 0)
countdown_placeholder = st.empty()

# --- Layout do Checklist ---
st.subheader("Nosso Checklist Detalhado")

# Determina qual expander deve abrir por padrão
current_date = datetime.datetime.now()
default_expanded_phase_key = next(iter(checklist_data)) # Padrão para o primeiro

# Lógica para expandir a fase atual
if wedding_date > current_date:
    time_to_wedding = wedding_date - current_date
    months_to_wedding = time_to_wedding.days / 30.44

    if months_to_wedding <= 1:
        default_expanded_phase_key = "Na Semana do Casamento"
    elif months_to_wedding <= 2:
        default_expanded_phase_key = "Fase 5: 1 Mês Antes (Agosto/2026) - Reta Final"
    elif months_to_wedding <= 4:
        default_expanded_phase_key = "Fase 4: 3 a 2 Meses Antes (Jun/26 a Jul/26) - Burocracia Civil e Religiosa"
    elif months_to_wedding <= 7:
        default_expanded_phase_key = "Fase 3: 6 a 4 Meses Antes (Mar/26 a Mai/26) - Trajes, Convites e Detalhes"
    elif months_to_wedding <= 10:
        default_expanded_phase_key = "Fase 2: 9 a 7 Meses Antes (Dez/25 a Fev/26) - Fornecedores Principais"
    else:
        default_expanded_phase_key = "Fase 1: 12 a 10 Meses Antes (Set/25 a Nov/25) - Planejamento Inicial"


for phase, tasks in checklist_data.items():
    # A fase atual ou a primeira fase será expandida por padrão
    is_expanded = phase == default_expanded_phase_key
    with st.expander(f"🗓️ {phase}", expanded=is_expanded):
        for task in tasks:
            if task.get('is_note'):
                st.info(task['text'])
            else:
                st.session_state.tasks_status[task['id']] = st.checkbox(
                    task['text'],
                    value=st.session_state.tasks_status.get(task['id'], False),
                    key=task['id']
                )

# --- Lógica da Contagem Regressiva ---
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
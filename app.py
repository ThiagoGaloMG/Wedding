# Lembre-se de criar o arquivo requirements.txt para que esta linha funcione!
import streamlit as st
import datetime
from streamlit_autorefresh import st_autorefresh

# --- Configuração da Página ---
st.set_page_config(
    page_title="Checklist do Casamento | Daniela & Thiago",
    page_icon="💖",
    layout="centered", # Mantido 'centered' para melhor legibilidade
    initial_sidebar_state="collapsed",
)

# --- CSS Customizado para um Visual Elegante ---
st.markdown("""
<style>
/* Importando as fontes do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Montserrat:wght@400;500;600&display=swap');

/* --- FUNDO E ESTILOS GERAIS --- */
body {
    background-color: #fff9fb;
}

.stApp {
    background-image: url('https://www.toptal.com/designers/subtlepatterns/uploads/watercolor.png');
    background-attachment: fixed;
    background-size: cover;
    font-family: 'Montserrat', sans-serif;
}

/* --- ESTILOS DO CABEÇALHO --- */
.wedding-names {
    font-family: 'Dancing Script', cursive;
    font-size: 4.5rem;
    font-weight: 700;
    text-align: center;
    color: #c2185b;
    margin-bottom: -10px;
}

.wedding-date {
    font-family: 'Montserrat', sans-serif;
    text-align: center;
    font-size: 1.1rem;
    color: #555;
    letter-spacing: 1px;
}

/* --- SEÇÃO DE PROGRESSO --- */
.progress-section {
    text-align: center;
    margin-bottom: 2rem;
}
.progress-text {
    font-size: 1.2rem;
    font-weight: 600;
    color: #c2185b;
}
.progress-subtext {
    color: #666;
}

/* --- CONTAGEM REGRESSIVA --- */
.countdown-section h2 {
    text-align: center;
    font-weight: 600;
    color: #333;
    font-size: 1.5rem;
}
.countdown-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #fff1f5, #ffe6ec); /* Fundo sólido */
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.9);
}
.countdown-box {
    background-color: rgba(255, 255, 255, 0.5);
    padding: 0.8rem;
    border-radius: 10px;
    width: 80px;
}
.countdown-number {
    font-size: 2rem;
    font-weight: bold;
    color: #d81b60;
}
.countdown-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    color: #666;
}

/* --- CHECKLIST --- */
.stExpander {
    background-color: #ffffff; /* CORREÇÃO: Fundo branco sólido para legibilidade */
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    margin-bottom: 1rem;
}

/* Estilo para o texto da tarefa */
.task-text {
    margin: 0;
    padding-top: 8px;
    font-size: 1rem;
    color: #333;
    transition: color 0.3s;
}

/* Estilo para o texto riscado */
.task-text.checked {
    text-decoration: line-through;
    color: #aaa;
}

div[data-testid="stCheckbox"] > label > div:first-of-type {
    border-radius: 50% !important;
    border: 2px solid #e19ab4 !important;
}
div[data-testid="stCheckbox"] > label > div:first-of-type[aria-checked="true"] {
    background-color: #e19ab4 !important;
}
.stAlert {
    background-color: #fffbe6 !important;
    border: 1px solid #ffe58f !important;
    border-radius: 10px !important;
}

/* --- RODAPÉ --- */
.footer {
    text-align: center;
    padding: 2rem;
    background-color: #ffffff; /* CORREÇÃO: Fundo branco sólido para legibilidade */
    border-radius: 10px;
    margin-top: 2rem;
}
.footer-text {
    font-size: 1.5rem;
    font-weight: 600;
    color: #c2185b;
}
.footer-subtext {
    color: #555;
}

/* Media Query para telas menores (celulares) */
@media (max-width: 640px) {
    .wedding-names {
        font-size: 3.5rem;
    }
    .countdown-box {
        width: 65px;
        padding: 0.5rem;
    }
    .countdown-number {
        font-size: 1.5rem;
    }
}

</style>
""", unsafe_allow_html=True)


# --- DADOS DO CHECKLIST ---
checklist_data = {
    "Fase 1: 11 a 9 Meses Antes (Out/25 a Dez/25) - Planejamento Inicial": [
        {'id': 'definir-orcamento', 'text': 'Definir o Orçamento Geral do Casamento.'},
        {'id': 'lista-convidados-preliminar', 'text': 'Criar a Lista Preliminar de Convidados.'},
        {'id': 'escolher-padrinhos', 'text': 'Convidar Padrinhos e Madrinhas (máx. 3 casais por noivo).'},
        {'id': 'ponto-atencao-padre', 'text': '❤️ ATENÇÃO ESPECIAL: Agendar conversa com Padre Carlos para alinhar detalhes sobre viuvez e o processo religioso.', 'is_note': True},
        {'id': 'agendar-curso-noivos', 'text': 'Pesquisar e se inscrever no Curso de Noivos (fazer em outra paróquia).'},
        {'id': 'confirmar-salao', 'text': 'Confirmar a reserva do salão anexo da igreja para a recepção.'},
    ],
    "Fase 2: 8 a 6 Meses Antes (Jan/26 a Mar/26) - Contratando Fornecedores": [
        {'id': 'contato-paroquia', 'text': 'Contato Inicial com a Paróquia: Agendar data religiosa (05/09/2026).'},
        {'id': 'foto-video', 'text': 'Conversar e fechar com a amiga fotógrafa (repassar regras da igreja).'},
        {'id': 'musica-cerimonia', 'text': 'Conversar e fechar com os amigos músicos (repertório apenas religioso).'},
        {'id': 'decoracao', 'text': 'Contratar florista/decoração (repassar regras: 4 arranjos, etc.).'},
        {'id': 'bolo-doces', 'text': 'Pesquisar e agendar degustações de bolo e doces.'},
        {'id': 'definir-lua-de-mel', 'text': 'Lua de Mel: Definir o Destino e reservar passagens/hotéis.'},
        {'id': 'pesquisar-vestido-noiva', 'text': 'Vestido da Noiva: Iniciar pesquisa e provas.'},
        {'id': 'pesquisar-traje-noivo', 'text': 'Traje do Noivo: Iniciar pesquisa.'},
        {'id': 'pesquisar-dia-noiva', 'text': 'Pesquisar profissional para o Dia da Noiva em casa.'},
    ],
    "Fase 3: 5 a 4 Meses Antes (Abr/26 a Mai/26) - Detalhes e Documentos": [
        {'id': 'contratar-vestido-noiva', 'text': 'Contratar/Comprar o Vestido da Noiva.'},
        {'id': 'contratar-traje-noivo', 'text': 'Contratar/Comprar o Traje do Noivo.'},
        {'id': 'contratar-dia-noiva-profissional', 'text': 'Contratar profissional para o Dia da Noiva em casa.'},
        {'id': 'criar-site', 'text': 'Criar e configurar o Site dos Noivos (Lejour).'},
        {'id': 'design-convites', 'text': 'Definir o design dos convites.'},
        {'id': 'lista-convidados-final', 'text': 'Finalizar a Lista de Convidados.'},
        {'id': 'encomendar-bolo-doces', 'text': 'Encomendar Bolo e Docinhos.'},
        {'id': 'encomendar-tercos-ns', 'text': 'Encomendar os terços de Nossa Senhora das Lágrimas.'},
        {'id': 'material-tercos-proprios', 'text': 'Comprar material para a produção dos terços.'},
        {'id': 'solicitar-certidoes-cartorio', 'text': '⚠️ BUROCRACIA: A partir de 05/06/2026, solicitar as certidões ATUALIZADAS para o civil (Nascimento, Casamento anterior, Óbito). Elas valem por 90 dias.', 'is_note': True},
    ],
    "Fase 4: 3 a 2 Meses Antes (Jun/26 a Jul/26) - Processos Oficiais": [
        {'id': 'marcar-entrevista-padre', 'text': '🗓️ PRAZO: Até 27/06/2026 - Marcar Entrevista com o Padre e iniciar o processo na Paróquia.'},
        {'id': 'entregar-docs-paroquia', 'text': 'Entregar os documentos do processo religioso na paróquia (Batistério, etc.).'},
        {'id': 'habilitacao-cartorio', 'text': '🗓️ PRAZO: Início de Julho - Dar Entrada no Processo de Habilitação do Casamento Civil com as testemunhas.'},
        {'id': 'imprimir-enviar-convites', 'text': 'Imprimir e começar a enviar/entregar os convites.'},
    ],
    "Fase 5: 1 Mês Antes (Agosto/2026) - Reta Final": [
        {'id': 'confirmar-presenca-rsvp', 'text': '🗓️ PRAZO: Até 22/08/2026 - Confirmar Presença (RSVP) e fechar número de convidados.'},
        {'id': 'reuniao-final-fornecedores', 'text': 'Reunião Final com todos os fornecedores.'},
        {'id': 'prova-final-trajes', 'text': 'Prova Final do Vestido e Terno.'},
        {'id': 'definir-leituras-musicas', 'text': 'Definir com o Padre as leituras e músicas da cerimônia.'},
        {'id': 'prova-cabelo-maquiagem', 'text': 'Fazer teste final de cabelo e maquiagem.'},
    ],
    "Na Semana do Casamento": [
        {'id': 'casamento-civil', 'text': '❤️ GRANDE PASSO: 03/09/2026 - Casamento Civil no Cartório!'},
        {'id': 'entregar-certidao-civil', 'text': '⚠️ URGENTE: 03/09/2026 - Entregar a Xerox da Certidão Civil na Paróquia (no mesmo dia do civil!).', 'is_note': True},
        {'id': 'buscar-trajes', 'text': 'Buscar o Vestido e o Terno.'},
        {'id': 'confirmar-horarios-todos', 'text': 'Confirmar horário com TODOS os profissionais.'},
        {'id': 'finalizar-tercos', 'text': 'Finalizar a produção e embalagem dos terços.'},
        {'id': 'organizar-malas-lua-de-mel', 'text': 'Organizar as Malas da Lua de Mel.'},
        {'id': 'relaxar', 'text': 'Descansar e relaxar! Delegar as últimas tarefas.'},
    ],
    "O Grande Dia: 05/09/2026": [
        {'id': 'cafe-reforcado', 'text': 'Tomar um café da manhã reforçado e se hidratar.'},
        {'id': 'aproveitar-preparacao', 'text': 'Curtir o Dia da Noiva e a preparação do noivo.'},
        {'id': 'chegar-pontualmente', 'text': 'Chegar Pontualmente na Igreja.'},
        {'id': 'celebrar', 'text': '❤️ ATENÇÃO ESPECIAL: Aproveitar, celebrar e viver cada segundo!', 'is_note': True},
    ],
}

# --- Inicialização do Estado da Sessão ---
if 'tasks_status' not in st.session_state:
    st.session_state.tasks_status = {task['id']: False for phase in checklist_data.values() for task in phase if not task.get('is_note')}

# --- Função para renderizar uma tarefa (com texto riscado) ---
def render_task(task):
    task_id = task['id']
    is_note = task.get('is_note', False)

    if is_note:
        st.warning(task['text'])
        return

    # Garante que a tarefa tenha um estado inicial
    if task_id not in st.session_state.tasks_status:
        st.session_state.tasks_status[task_id] = False
    
    # Usa colunas para alinhar checkbox e texto
    col1, col2 = st.columns([0.1, 2.5])

    with col1:
        # O st.checkbox atualiza o estado da sessão
        is_checked = st.checkbox("", value=st.session_state.tasks_status[task_id], key=f"cb_{task_id}")
        st.session_state.tasks_status[task_id] = is_checked

    with col2:
        # Aplica a classe CSS 'checked' se a caixa estiver marcada
        if is_checked:
            st.markdown(f"<p class='task-text checked'>{task['text']}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='task-text'>{task['text']}</p>", unsafe_allow_html=True)

# --- LAYOUT DA PÁGINA ---
# --- Cabeçalho ---
st.markdown('<h1 class="wedding-names">✨ Daniela & Thiago ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="wedding-date">❤️ Nosso caminho até 05 de Setembro de 2026 ❤️</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Barra de Progresso ---
total_tasks = len([task for phase in checklist_data.values() for task in phase if not task.get('is_note')])
completed_tasks = sum(1 for status in st.session_state.tasks_status.values() if status)
progress = completed_tasks / total_tasks if total_tasks > 0 else 0

st.markdown('<div class="progress-section">', unsafe_allow_html=True)
st.markdown(f'<p class="progress-text">Progresso do Planejamento</p>', unsafe_allow_html=True)
st.progress(progress)
st.markdown(f"<p class='progress-subtext'>{completed_tasks} de {total_tasks} tarefas concluídas ({progress:.0%})</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Contagem Regressiva ---
st.markdown('<div class="countdown-section"><h2>Contagem Regressiva para o Grande Dia</h2></div>', unsafe_allow_html=True)
wedding_date = datetime.datetime(2026, 9, 5, 16, 0, 0)
countdown_placeholder = st.empty()

# --- Layout do Checklist ---
st.subheader("Nosso Checklist Detalhado")

# Lógica para expandir a fase atual
current_date = datetime.datetime.now()
default_expanded_phase_key = next(iter(checklist_data))
if wedding_date > current_date:
    months_to_wedding = (wedding_date.year - current_date.year) * 12 + wedding_date.month - current_date.month
    if months_to_wedding <= 1: default_expanded_phase_key = "Na Semana do Casamento"
    elif months_to_wedding <= 3: default_expanded_phase_key = "Fase 5: 1 Mês Antes (Agosto/2026) - Reta Final"
    elif months_to_wedding <= 5: default_expanded_phase_key = "Fase 4: 3 a 2 Meses Antes (Jun/26 a Jul/26) - Processos Oficiais"
    elif months_to_wedding <= 8: default_expanded_phase_key = "Fase 3: 5 a 4 Meses Antes (Abr/26 a Mai/26) - Detalhes e Documentos"
    elif months_to_wedding <= 11: default_expanded_phase_key = "Fase 2: 8 a 6 Meses Antes (Jan/26 a Mar/26) - Contratando Fornecedores"
    else: default_expanded_phase_key = "Fase 1: 11 a 9 Meses Antes (Out/25 a Dez/25) - Planejamento Inicial"

for phase, tasks in checklist_data.items():
    is_expanded = phase == default_expanded_phase_key
    with st.expander(f"🗓️ {phase}", expanded=is_expanded):
        for task in tasks:
            render_task(task) # Usa a nova função para renderizar cada tarefa

# --- Rodapé ---
st.markdown("""
<div class="footer">
    <p class="footer-text">Juntos para Sempre</p>
    <p class="footer-subtext">Cada tarefa completada nos aproxima do nosso sonho realizado ❤️</p>
</div>
""", unsafe_allow_html=True)

# --- Lógica da Contagem Regressiva (DEVE FICAR NO FINAL) ---
st_autorefresh(interval=1000, key="countdownrefresh")
now = datetime.datetime.now()
remaining = wedding_date - now

if remaining.total_seconds() < 0:
    with countdown_placeholder.container():
        st.markdown(
            '<div class="countdown-container"><span style="font-size: 2rem; font-weight: bold; color: #d81b60;">Feliz Casamento!</span></div>',
            unsafe_allow_html=True)
else:
    days, r_seconds = remaining.days, remaining.seconds
    hours = r_seconds // 3600
    minutes = (r_seconds % 3600) // 60
    seconds = r_seconds % 60
    with countdown_placeholder.container():
        st.markdown(f"""
        <div class="countdown-container">
            <div class="countdown-box"><span class="countdown-number">{days}</span><span class="countdown-label">Dias</span></div>
            <div class="countdown-box"><span class="countdown-number">{hours}</span><span class="countdown-label">Horas</span></div>
            <div class="countdown-box"><span class="countdown-number">{minutes}</span><span class="countdown-label">Minutos</span></div>
            <div class="countdown-box"><span class="countdown-number">{seconds}</span><span class="countdown-label">Segundos</span></div>
        </div>
        """, unsafe_allow_html=True)
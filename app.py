# Lembre-se de criar o arquivo requirements.txt para que esta linha funcione!
import streamlit as st
import datetime
from streamlit_autorefresh import st_autorefresh
from streamlit_local_storage import LocalStorage

# --- Configuração da Página ---
st.set_page_config(
    page_title="Checklist do Casamento | Daniela & Thiago",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS Customizado ---
st.markdown("""
<style>
/* Importando as fontes do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Montserrat:wght@400;500;600&display=swap');

/* --- ESTILOS GERAIS --- */
body { background-color: #fff9fb; }
.stApp {
    background-image: url('https://www.toptal.com/designers/subtlepatterns/uploads/watercolor.png');
    background-attachment: fixed;
    background-size: cover;
    font-family: 'Montserrat', sans-serif;
}
/* Oculta o menu hamburguer e o footer do Streamlit */
#MainMenu, footer { display: none; }

/* --- CABEÇALHO --- */
.wedding-names {
    font-family: 'Dancing Script', cursive;
    font-size: 4.5rem; font-weight: 700; text-align: center; color: #c2185b; margin-bottom: -10px;
}
.wedding-date {
    font-family: 'Montserrat', sans-serif;
    text-align: center; font-size: 1.1rem; color: #555; letter-spacing: 1px;
}

/* --- PROGRESSO --- */
.progress-section { text-align: center; margin-bottom: 2rem; }
.progress-text { font-size: 1.2rem; font-weight: 600; color: #c2185b; }
.progress-subtext { color: #666; }

/* --- CONTAGEM REGRESSIVA --- */
.countdown-section h2 { text-align: center; font-weight: 600; color: #333; font-size: 1.5rem; }
.countdown-container {
    display: flex; justify-content: center; gap: 1rem; text-align: center; padding: 1.5rem;
    background: linear-gradient(135deg, #fff1f5, #ffe6ec); border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.9);
}
.countdown-box { background-color: rgba(255, 255, 255, 0.5); padding: 0.8rem; border-radius: 10px; width: 80px; }
.countdown-number { font-size: 2rem; font-weight: bold; color: #d81b60; }
.countdown-label { font-size: 0.7rem; text-transform: uppercase; color: #666; }

/* --- CHECKLIST --- */
.stExpander {
    background-color: #ffffff; border: none !important; border-radius: 10px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important; margin-bottom: 1rem;
}
.task-container { display: flex; align-items: center; justify-content: space-between; }
.task-text { margin: 0; padding-left: 10px; font-size: 1rem; color: #333; transition: color 0.3s; }
.task-text.checked { text-decoration: line-through; color: #aaa; }
.stButton>button {
    background-color: transparent; border: none; color: #aaa; padding: 0;
    font-size: 0.9rem;
}
.stButton>button:hover { color: #c2185b; }
.stAlert { background-color: #fffbe6 !important; border: 1px solid #ffe58f !important; border-radius: 10px !important; }

/* --- RODAPÉ --- */
.footer {
    text-align: center; padding: 2rem; background-color: #ffffff;
    border-radius: 10px; margin-top: 2rem;
}
.footer-text { font-size: 1.5rem; font-weight: 600; color: #c2185b; }
.footer-subtext { color: #555; }

@media (max-width: 640px) {
    .wedding-names { font-size: 3.5rem; }
    .countdown-box { width: 65px; padding: 0.5rem; }
    .countdown-number { font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# --- DADOS INICIAIS DO CHECKLIST ---
initial_checklist_data = {
    "Fase 1: Planejamento Inicial (até Dez/25)": [
        {'id': 'definir-orcamento', 'text': 'Definir o Orçamento Geral do Casamento.', 'checked': False},
        {'id': 'lista-convidados-preliminar', 'text': 'Criar a Lista Preliminar de Convidados.', 'checked': False},
        {'id': 'escolher-padrinhos', 'text': 'Convidar Padrinhos e Madrinhas (máx. 3 casais por noivo).', 'checked': False},
        {'id': 'ponto-atencao-padre', 'text': '❤️ ATENÇÃO ESPECIAL: Agendar conversa com Padre Carlos para alinhar detalhes sobre viuvez e o processo religioso.', 'is_note': True},
        {'id': 'agendar-curso-noivos', 'text': 'Pesquisar e se inscrever no Curso de Noivos.', 'checked': False},
        {'id': 'confirmar-salao', 'text': 'Confirmar a reserva do salão anexo da igreja para a recepção.', 'checked': False},
        {'id': 'design-convites', 'text': 'Definir o design dos convites.', 'checked': False},
    ],
    "Fase 2: Contratando Fornecedores (Jan/26 a Mar/26)": [
        {'id': 'contato-paroquia', 'text': 'Contato Inicial com a Paróquia: Agendar data religiosa (05/09/2026).', 'checked': False},
        {'id': 'foto-video', 'text': 'Conversar e fechar com a amiga fotógrafa (repassar regras).', 'checked': False},
        {'id': 'musica-cerimonia', 'text': 'Conversar e fechar com os amigos músicos (repertório religioso).', 'checked': False},
        {'id': 'decoracao', 'text': 'Contratar florista/decoração (repassar regras).', 'checked': False},
        {'id': 'bolo-doces', 'text': 'Pesquisar e agendar degustações de bolo e doces.', 'checked': False},
        {'id': 'definir-lua-de-mel', 'text': 'Lua de Mel: Definir Destino e reservar passagens/hotéis.', 'checked': False},
        {'id': 'pesquisar-vestido-noiva', 'text': 'Vestido da Noiva: Iniciar pesquisa e provas.', 'checked': False},
        {'id': 'pesquisar-traje-noivo', 'text': 'Traje do Noivo: Iniciar pesquisa.', 'checked': False},
        {'id': 'pesquisar-dia-noiva', 'text': 'Pesquisar profissional para o Dia da Noiva em casa.', 'checked': False},
    ],
    "Fase 3: Detalhes e Documentos (Abr/26 a Mai/26)": [
        {'id': 'contratar-vestido-noiva', 'text': 'Contratar/Comprar o Vestido da Noiva.', 'checked': False},
        {'id': 'contratar-traje-noivo', 'text': 'Contratar/Comprar o Traje do Noivo.', 'checked': False},
        {'id': 'contratar-dia-noiva-profissional', 'text': 'Contratar profissional para o Dia da Noiva.', 'checked': False},
        {'id': 'criar-site', 'text': 'Criar e configurar o Site dos Noivos (Lejour).', 'checked': False},
        {'id': 'lista-convidados-final', 'text': 'Finalizar a Lista de Convidados.', 'checked': False},
        {'id': 'encomendar-bolo-doces', 'text': 'Encomendar Bolo e Docinhos.', 'checked': False},
        {'id': 'encomendar-tercos-ns', 'text': 'Encomendar os terços de Nossa Sra. das Lágrimas.', 'checked': False},
        {'id': 'material-tercos-proprios', 'text': 'Comprar material para a produção dos terços.', 'checked': False},
        {'id': 'batismo-thiago', 'text': '🗓️ PRAZO: A partir de 05/03/26 - Thiago: Solicitar Certidão de Batismo para fins matrimoniais.', 'checked': False},
        {'id': 'batismo-daniela', 'text': '🗓️ PRAZO: A partir de 05/08/26 - Daniela: Solicitar Certidão de Batismo.', 'checked': False},
    ],
    "Fase 4: Processos Oficiais (Jun/26 a Jul/26)": [
        {'id': 'solicitar-docs-daniela', 'text': '🗓️ PRAZO: A partir de 04/06/2026 - Daniela: Solicitar certidões de Casamento Anterior, Óbito e Inventário (valem 90 dias).', 'checked': False},
        {'id': 'solicitar-docs-thiago', 'text': '🗓️ PRAZO: A partir de 04/06/2026 - Thiago: Solicitar certidão de Nascimento (vale 90 dias).', 'checked': False},
        {'id': 'marcar-entrevista-padre', 'text': '🗓️ PRAZO: Até 27/06/26 - Marcar Entrevista com o Padre e iniciar o processo na Paróquia.', 'checked': False},
        {'id': 'entregar-docs-paroquia', 'text': 'Entregar documentos do processo religioso na paróquia.', 'checked': False},
        {'id': 'habilitacao-cartorio', 'text': '🗓️ PRAZO: Início de Julho - Dar Entrada na Habilitação do Casamento Civil com as testemunhas.', 'checked': False},
        {'id': 'imprimir-enviar-convites', 'text': 'Imprimir e começar a enviar/entregar os convites.', 'checked': False},
    ],
    "Fase 5: Reta Final (Agosto/2026)": [
        {'id': 'confirmar-presenca-rsvp', 'text': '🗓️ PRAZO: Até 22/08/26 - Confirmar Presença (RSVP).', 'checked': False},
        {'id': 'reuniao-final-fornecedores', 'text': 'Reunião Final com todos os fornecedores.', 'checked': False},
        {'id': 'prova-final-trajes', 'text': 'Prova Final do Vestido e Terno.', 'checked': False},
        {'id': 'definir-leituras-musicas', 'text': 'Definir com o Padre as leituras e músicas.', 'checked': False},
        {'id': 'prova-cabelo-maquiagem', 'text': 'Fazer teste final de cabelo e maquiagem.', 'checked': False},
    ],
    "Na Semana do Casamento": [
        {'id': 'casamento-civil', 'text': '❤️ GRANDE PASSO: 03/09/2026 - Casamento Civil no Cartório!', 'checked': False},
        {'id': 'entregar-certidao-civil', 'text': '⚠️ URGENTE: 03/09/2026 - Entregar a Xerox da Certidão Civil na Paróquia!', 'is_note': True},
        {'id': 'buscar-trajes', 'text': 'Buscar o Vestido e o Terno.', 'checked': False},
        {'id': 'confirmar-horarios-todos', 'text': 'Confirmar horário com TODOS os profissionais.', 'checked': False},
        {'id': 'finalizar-tercos', 'text': 'Finalizar a produção e embalagem dos terços.', 'checked': False},
        {'id': 'organizar-malas-lua-de-mel', 'text': 'Organizar as Malas da Lua de Mel.', 'checked': False},
        {'id': 'relaxar', 'text': 'Descansar e relaxar! Delegar as últimas tarefas.', 'checked': False},
    ],
}

# --- INICIALIZAÇÃO DO ESTADO E PERSISTÊNCIA ---
storage = LocalStorage()

if 'checklist_loaded' not in st.session_state:
    saved_checklist = storage.getItem('wedding_checklist')
    st.session_state.checklist = saved_checklist if saved_checklist else initial_checklist_data
    st.session_state.checklist_loaded = True

if 'editing_task' not in st.session_state:
    st.session_state.editing_task = None


# --- FUNÇÕES DE MANIPULAÇÃO DO CHECKLIST ---
def add_task(phase, text):
    new_task = {'id': f'custom_{datetime.datetime.now().timestamp()}', 'text': text, 'checked': False}
    st.session_state.checklist[phase].append(new_task)

def delete_task(phase, task_id):
    st.session_state.checklist[phase] = [t for t in st.session_state.checklist[phase] if t['id'] != task_id]

def update_task_text(phase, task_id, new_text):
    for task in st.session_state.checklist[phase]:
        if task['id'] == task_id:
            task['text'] = new_text
            break
    st.session_state.editing_task = None


# --- FUNÇÃO PARA GERAR HTML PARA IMPRESSÃO ---
def generate_printable_html(checklist):
    html = f"""
    <html>
    <head>
        <title>Checklist Casamento - Daniela & Thiago</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Montserrat:wght@400;500;600&display=swap');
            body {{ font-family: 'Montserrat', sans-serif; padding: 20px; }}
            h1 {{ font-family: 'Dancing Script', cursive; font-size: 3rem; color: #c2185b; text-align: center; }}
            h2 {{ font-family: 'Montserrat', sans-serif; color: #333; border-bottom: 2px solid #f1f1f1; padding-bottom: 5px; }}
            ul {{ list-style-type: none; padding-left: 0; }}
            li {{ margin-bottom: 10px; font-size: 1.1rem; }}
            .checked {{ text-decoration: line-through; color: #aaa; }}
            .note {{ background-color: #fffbe6; border-left: 5px solid #ffe58f; padding: 10px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>✨ Daniela & Thiago ✨</h1>
        <hr>
    """
    for phase, tasks in checklist.items():
        html += f"<h2>{phase}</h2><ul>"
        for task in tasks:
            if task.get('is_note'):
                html += f"<li class='note'>{task['text']}</li>"
            else:
                checked_class = "checked" if task.get('checked') else ""
                checkbox = "☑" if task.get('checked') else "☐"
                html += f"<li class='{checked_class}'>{checkbox} {task['text']}</li>"
        html += "</ul>"
    html += "</body></html>"
    return html


# --- LAYOUT DA PÁGINA ---
st.markdown('<h1 class="wedding-names">✨ Daniela & Thiago ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="wedding-date">❤️ Nosso caminho até 05 de Setembro de 2026 ❤️</p>', unsafe_allow_html=True)

# --- BOTÕES DE AÇÃO ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Salvar Alterações 💾", use_container_width=True):
        storage.setItem('wedding_checklist', st.session_state.checklist)
        st.toast("Checklist salvo com sucesso!", icon="✅")

with col2:
    printable_html = generate_printable_html(st.session_state.checklist)
    st.download_button(
        label="Exportar para Impressão 🖨️",
        data=printable_html,
        file_name="checklist_casamento_daniela_thiago.html",
        mime="text/html",
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- Barra de Progresso Geral ---
total_tasks = sum(1 for phase_tasks in st.session_state.checklist.values() for task in phase_tasks if not task.get('is_note'))
completed_tasks = sum(1 for phase_tasks in st.session_state.checklist.values() for task in phase_tasks if task.get('checked'))
progress = completed_tasks / total_tasks if total_tasks > 0 else 0

st.markdown('<div class="progress-section">', unsafe_allow_html=True)
st.markdown(f'<p class="progress-text">Progresso Geral do Planejamento</p>', unsafe_allow_html=True)
st.progress(progress)
st.markdown(f"<p class='progress-subtext'>{completed_tasks} de {total_tasks} tarefas concluídas ({progress:.0%})</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Contagem Regressiva ---
st.markdown('<div class="countdown-section"><h2>Contagem Regressiva para o Grande Dia</h2></div>', unsafe_allow_html=True)
wedding_date = datetime.datetime(2026, 9, 5, 16, 0, 0)
countdown_placeholder = st.empty()

# --- Layout do Checklist ---
st.subheader("Nosso Checklist Detalhado")

for phase, tasks in st.session_state.checklist.items():
    with st.expander(f"🗓️ {phase}", expanded=False):
        phase_total = sum(1 for t in tasks if not t.get('is_note'))
        phase_completed = sum(1 for t in tasks if t.get('checked'))
        phase_progress = phase_completed / phase_total if phase_total > 0 else 0
        st.markdown(f"<p style='text-align: right; font-size: 0.9rem;'>{phase_completed}/{phase_total} ({phase_progress:.0%}) concluído</p>", unsafe_allow_html=True)
        st.progress(phase_progress)
        
        for i, task in enumerate(tasks):
            if task.get('is_note'):
                st.warning(task['text'])
                continue

            task_id = task['id']
            cols = st.columns([0.1, 1.8, 0.2, 0.2])
            
            with cols[0]:
                is_checked = st.checkbox("", value=task.get('checked', False), key=f"cb_{task_id}")
                if is_checked != task.get('checked', False):
                    task['checked'] = is_checked
                    st.rerun()

            with cols[1]:
                if st.session_state.editing_task == task_id:
                    new_text = st.text_input("Editar tarefa", value=task['text'], key=f"edit_{task_id}", label_visibility="collapsed")
                    if st.button("Salvar", key=f"save_{task_id}"):
                        update_task_text(phase, task_id, new_text)
                        st.rerun()
                else:
                    checked_class = "checked" if task.get('checked') else ""
                    st.markdown(f"<div class='task-container'><p class='task-text {checked_class}'>❤️ {task['text']}</p></div>", unsafe_allow_html=True)
            
            with cols[2]:
                if st.button("✏️", key=f"btn_edit_{task_id}", help="Editar tarefa"):
                    st.session_state.editing_task = task_id
                    st.rerun()
            with cols[3]:
                if st.button("🗑️", key=f"btn_del_{task_id}", help="Excluir tarefa"):
                    delete_task(phase, task_id)
                    st.rerun()
        
        st.markdown("---")
        new_task_text = st.text_input("Nova tarefa", key=f"new_task_{phase}", placeholder="Adicionar nova tarefa nesta fase...")
        if st.button("Adicionar Tarefa", key=f"add_btn_{phase}"):
            if new_task_text:
                add_task(phase, new_task_text)
                st.rerun()

# --- Rodapé ---
st.markdown("""
<div class="footer">
    <p class="footer-text">Juntos para Sempre</p>
    <p class="footer-subtext">Cada tarefa completada nos aproxima do nosso sonho realizado ❤️</p>
</div>
""", unsafe_allow_html=True)

# --- LÓGICA DA CONTAGEM REGRESSIVA (SUAVE) ---
if "countdown_values" not in st.session_state:
    st.session_state.countdown_values = {"d": 0, "h": 0, "m": 0, "s": 0}

now = datetime.datetime.now()
remaining = wedding_date - now

if remaining.total_seconds() > 0:
    days, r_seconds = remaining.days, remaining.seconds
    hours = r_seconds // 3600
    minutes = (r_seconds % 3600) // 60
    seconds = r_seconds % 60
    st.session_state.countdown_values = {"d": days, "h": hours, "m": minutes, "s": seconds}

with countdown_placeholder.container():
    cv = st.session_state.countdown_values
    if remaining.total_seconds() < 0:
        st.markdown('<div class="countdown-container"><span style="font-size: 2rem; font-weight: bold; color: #d81b60;">Feliz Casamento!</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="countdown-container">
            <div class="countdown-box"><span class="countdown-number">{cv['d']}</span><span class="countdown-label">Dias</span></div>
            <div class="countdown-box"><span class="countdown-number">{cv['h']}</span><span class="countdown-label">Horas</span></div>
            <div class="countdown-box"><span class="countdown-number">{cv['m']}</span><span class="countdown-label">Minutos</span></div>
            <div class="countdown-box"><span class="countdown-number">{cv['s']}</span><span class="countdown-label">Segundos</span></div>
        </div>
        """, unsafe_allow_html=True)
    st_autorefresh(interval=1000, key="countdownrefresh")


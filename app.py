# Lembre-se de atualizar o arquivo requirements.txt para que esta linha funcione!
import streamlit as st
import datetime
import streamlit.components.v1 as components
import json
from supabase import create_client, Client
import time

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

/* --- STATUS DE SINCRONIZAÇÃO --- */
.sync-status {
    position: fixed;
    top: 10px;
    right: 10px;
    padding: 0.5rem;
    border-radius: 5px;
    font-size: 0.8rem;
    z-index: 1000;
}
.sync-success { background-color: #d4edda; color: #155724; }
.sync-error { background-color: #f8d7da; color: #721c24; }
.sync-loading { background-color: #fff3cd; color: #856404; }

/* --- CONTAGEM REGRESSIVA (Estilos para o componente HTML) --- */
.countdown-section h2 { text-align: center; font-weight: 600; color: #333; font-size: 1.5rem; }
.countdown-container-js {
    display: flex; justify-content: center; gap: 1rem; text-align: center; padding: 1.5rem;
    background: linear-gradient(135deg, #fff1f5, #ffe6ec); border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.9);
}
.countdown-box-js { background-color: rgba(255, 255, 255, 0.5); padding: 0.8rem; border-radius: 10px; width: 80px; }
.countdown-number-js { font-size: 2rem; font-weight: bold; color: #d81b60; }
.countdown-label-js { font-size: 0.7rem; text-transform: uppercase; color: #666; }

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
    .countdown-box-js { width: 65px; padding: 0.5rem; }
    .countdown-number-js { font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO SUPABASE ---
@st.cache_resource
def init_supabase():
    """Inicializa a conexão com o Supabase"""
    try:
        if "supabase_url" in st.secrets and "supabase_key" in st.secrets:
            url = st.secrets["supabase_url"]
            key = st.secrets["supabase_key"]
            supabase_client = create_client(url, key)
            
            # Testa a conexão
            try:
                supabase_client.table("checklists").select("id").limit(1).execute()
                return supabase_client
            except Exception as e:
                st.error(f"Erro ao testar conexão com Supabase: {e}")
                return None
                
        else:
            st.error("⚠️ As credenciais do Supabase não foram encontradas nos segredos do Streamlit.")
            st.info("Configure as variáveis SUPABASE_URL e SUPABASE_KEY nos secrets do Streamlit.")
            return None
    except Exception as e:
        st.error(f"Falha ao conectar com o Supabase: {e}")
        return None

def show_sync_status(status, message=""):
    """Exibe o status de sincronização"""
    if status == "success":
        st.markdown(f'<div class="sync-status sync-success">✅ Sincronizado {message}</div>', unsafe_allow_html=True)
    elif status == "error":
        st.markdown(f'<div class="sync-status sync-error">❌ Erro na sincronização {message}</div>', unsafe_allow_html=True)
    elif status == "loading":
        st.markdown(f'<div class="sync-status sync-loading">⏳ Sincronizando... {message}</div>', unsafe_allow_html=True)

# Inicializa o Supabase
supabase = init_supabase()
CHECKLIST_ID = "daniela_thiago_2026"

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

# --- FUNÇÕES DE MANIPULAÇÃO DO CHECKLIST COM SUPABASE ---
def get_checklist_from_supabase():
    """Carrega o checklist do Supabase"""
    if not supabase:
        return initial_checklist_data
        
    try:
        response = supabase.table("checklists").select("data, updated_at").eq("id", CHECKLIST_ID).execute()
        
        if response.data:
            return response.data[0]["data"]
        else:
            # Se não encontrar, cria o registro inicial
            save_checklist_to_supabase(initial_checklist_data)
            return initial_checklist_data
            
    except Exception as e:
        st.error(f"Erro ao carregar dados do Supabase: {e}")
        return initial_checklist_data

def save_checklist_to_supabase(data):
    """Salva o checklist no Supabase"""
    if not supabase:
        return False
        
    try:
        # Limpa os dados para evitar problemas de serialização
        clean_data = json.loads(json.dumps(data))
        
        # Adiciona timestamp para controle de versão
        timestamp = datetime.datetime.now().isoformat()
        
        response = supabase.table("checklists").upsert({
            "id": CHECKLIST_ID,
            "data": clean_data,
            "updated_at": timestamp
        }).execute()
        
        return True
        
    except Exception as e:
        st.error(f"Erro ao salvar no Supabase: {e}")
        return False

def auto_refresh_data():
    """Verifica se há atualizações no Supabase e recarrega automaticamente"""
    if not supabase:
        return
        
    try:
        response = supabase.table("checklists").select("updated_at").eq("id", CHECKLIST_ID).execute()
        
        if response.data:
            server_timestamp = response.data[0]["updated_at"]
            
            # Compara com o timestamp local (se existir)
            if 'last_sync' not in st.session_state:
                st.session_state.last_sync = server_timestamp
                
            if server_timestamp != st.session_state.last_sync:
                # Dados foram atualizados, recarrega
                st.session_state.checklist = get_checklist_from_supabase()
                st.session_state.last_sync = server_timestamp
                show_sync_status("success", "Dados atualizados!")
                time.sleep(1)
                st.rerun()
                
    except Exception:
        pass

# --- INICIALIZAÇÃO DOS DADOS ---
# Carrega os dados no início se não estiverem em cache
if 'checklist' not in st.session_state:
    st.session_state.checklist = get_checklist_from_supabase()

if 'editing_task' not in st.session_state:
    st.session_state.editing_task = None

if 'last_sync' not in st.session_state:
    st.session_state.last_sync = None

# Verificação automática de atualizações (a cada 30 segundos)
if st.session_state.get('auto_refresh_time', 0) < time.time() - 30:
    st.session_state.auto_refresh_time = time.time()
    auto_refresh_data()

# --- FUNÇÕES DE MANIPULAÇÃO LOCAL ---
def add_task(phase, text):
    """Adiciona uma nova tarefa"""
    new_task = {
        'id': f'custom_{datetime.datetime.now().timestamp()}', 
        'text': text, 
        'checked': False
    }
    st.session_state.checklist[phase].append(new_task)
    
    if save_checklist_to_supabase(st.session_state.checklist):
        show_sync_status("success", "Tarefa adicionada!")
    else:
        show_sync_status("error", "Falha ao salvar")

def delete_task(phase, task_id):
    """Remove uma tarefa"""
    st.session_state.checklist[phase] = [
        t for t in st.session_state.checklist[phase] 
        if t['id'] != task_id
    ]
    
    if save_checklist_to_supabase(st.session_state.checklist):
        show_sync_status("success", "Tarefa removida!")
    else:
        show_sync_status("error", "Falha ao salvar")

def update_task_text(phase, task_id, new_text):
    """Atualiza o texto de uma tarefa"""
    for task in st.session_state.checklist[phase]:
        if task['id'] == task_id:
            task['text'] = new_text
            break
            
    st.session_state.editing_task = None
    
    if save_checklist_to_supabase(st.session_state.checklist):
        show_sync_status("success", "Tarefa atualizada!")
    else:
        show_sync_status("error", "Falha ao salvar")

def update_task_status(phase, task_id, status):
    """Atualiza o status de uma tarefa"""
    for task in st.session_state.checklist[phase]:
        if task['id'] == task_id:
            task['checked'] = status
            break
            
    if save_checklist_to_supabase(st.session_state.checklist):
        show_sync_status("success", "✓" if status else "○")
    else:
        show_sync_status("error", "Falha ao salvar")

# --- FUNÇÃO PARA GERAR HTML PARA IMPRESSÃO ---
def generate_printable_html(checklist):
    """Gera HTML para impressão"""
    html = f"""
    <html>
    <head>
        <title>Checklist Casamento - Daniela & Thiago</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Montserrat:wght@400;500;600&display=swap');
            body {{ font-family: 'Montserrat', sans-serif; padding: 20px; line-height: 1.6; }}
            h1 {{ font-family: 'Dancing Script', cursive; font-size: 3rem; color: #c2185b; text-align: center; }}
            h2 {{ font-family: 'Montserrat', sans-serif; color: #333; border-bottom: 2px solid #f1f1f1; padding-bottom: 5px; }}
            ul {{ list-style-type: none; padding-left: 0; }}
            li {{ margin-bottom: 10px; font-size: 1.1rem; }}
            .checked {{ text-decoration: line-through; color: #aaa; }}
            .note {{ background-color: #fffbe6; border-left: 5px solid #ffe58f; padding: 10px; margin: 10px 0; }}
            .progress {{ text-align: right; font-size: 0.9rem; color: #666; margin-bottom: 10px; }}
            .generated-date {{ text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem; }}
        </style>
    </head>
    <body>
        <h1>✨ Daniela & Thiago ✨</h1>
        <p style="text-align: center; font-size: 1.1rem; color: #555;">❤️ Nosso caminho até 05 de Setembro de 2026 ❤️</p>
        <hr>
    """
    
    total_tasks = sum(1 for phase_tasks in checklist.values() for task in phase_tasks if not task.get('is_note'))
    completed_tasks = sum(1 for phase_tasks in checklist.values() for task in phase_tasks if task.get('checked'))
    overall_progress = completed_tasks / total_tasks if total_tasks > 0 else 0
    
    html += f"<div class='progress'>Progresso Geral: {completed_tasks}/{total_tasks} ({overall_progress:.0%})</div>"
    
    for phase, tasks in checklist.items():
        phase_total = sum(1 for t in tasks if not t.get('is_note'))
        phase_completed = sum(1 for t in tasks if t.get('checked'))
        phase_progress = phase_completed / phase_total if phase_total > 0 else 0
        
        html += f"<h2>{phase}</h2>"
        html += f"<div class='progress'>Progresso da fase: {phase_completed}/{phase_total} ({phase_progress:.0%})</div>"
        html += "<ul>"
        
        for task in tasks:
            if task.get('is_note'):
                html += f"<li class='note'>{task['text']}</li>"
            else:
                checked_class = "checked" if task.get('checked') else ""
                checkbox = "☑" if task.get('checked') else "☐"
                html += f"<li class='{checked_class}'>{checkbox} {task['text']}</li>"
        html += "</ul>"
    
    html += f"<div class='generated-date'>Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>"
    html += "</body></html>"
    return html

# --- LAYOUT DA PÁGINA ---
st.markdown('<h1 class="wedding-names">✨ Daniela & Thiago ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="wedding-date">❤️ Nosso caminho até 05 de Setembro de 2026 ❤️</p>', unsafe_allow_html=True)

# --- STATUS DE CONEXÃO ---
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    if supabase:
        st.success("🔄 Conectado - Alterações são sincronizadas automaticamente!")
    else:
        st.warning("⚠️ Modo Offline - Alterações não serão salvas")

with col2:
    if st.button("🔄 Recarregar Dados", help="Recarrega os dados do servidor"):
        st.session_state.checklist = get_checklist_from_supabase()
        show_sync_status("success", "Dados recarregados!")
        st.rerun()

with col3:
    # --- BOTÃO DE EXPORTAR ---
    printable_html = generate_printable_html(st.session_state.checklist)
    st.download_button(
        label="📄 Exportar PDF",
        data=printable_html,
        file_name=f"checklist_casamento_{datetime.datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        help="Baixe o HTML e abra no navegador para imprimir como PDF"
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

countdown_html = f"""
<div class="countdown-container-js">
    <div class="countdown-box-js"><span id="days" class="countdown-number-js"></span><span class="countdown-label-js">Dias</span></div>
    <div class="countdown-box-js"><span id="hours" class="countdown-number-js"></span><span class="countdown-label-js">Horas</span></div>
    <div class="countdown-box-js"><span id="minutes" class="countdown-number-js"></span><span class="countdown-label-js">Minutos</span></div>
    <div class="countdown-box-js"><span id="seconds" class="countdown-number-js"></span><span class="countdown-label-js">Segundos</span></div>
</div>
<script>
const countdownDate = new Date("{wedding_date.isoformat()}").getTime();
const interval = setInterval(function() {{
    const now = new Date().getTime();
    const distance = countdownDate - now;
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    const format = (num) => num < 10 ? '0' + num : num;
    const daysEl = document.getElementById("days");
    const hoursEl = document.getElementById("hours");
    const minutesEl = document.getElementById("minutes");
    const secondsEl = document.getElementById("seconds");
    if(daysEl && hoursEl && minutesEl && secondsEl) {{
        daysEl.innerText = days;
        hoursEl.innerText = format(hours);
        minutesEl.innerText = format(minutes);
        secondsEl.innerText = format(seconds);
    }}
    if (distance < 0) {{
        clearInterval(interval);
        const container = document.querySelector(".countdown-container-js");
        if(container) {{
            container.innerHTML = '<span style="font-size: 1.5rem; font-weight: bold; color: #d81b60;">Feliz Casamento!</span>';
        }}
    }}
}}, 1000);
</script>
"""
components.html(countdown_html, height=130)

# --- Layout do Checklist ---
st.subheader("📋 Nosso Checklist Detalhado")

# Informações sobre sincronização
if supabase:
    st.info("💡 **Dica**: As alterações são salvas automaticamente e sincronizadas entre vocês dois em tempo real!")
else:
    st.error("⚠️ **Atenção**: Sem conexão com o banco de dados. Configure as credenciais do Supabase nos secrets.")

for phase, tasks in st.session_state.checklist.items():
    with st.expander(f"🗓️ {phase}", expanded=False):
        # Cálculo do progresso da fase
        phase_total = sum(1 for t in tasks if not t.get('is_note'))
        phase_completed = sum(1 for t in tasks if t.get('checked'))
        phase_progress = phase_completed / phase_total if phase_total > 0 else 0
        
        # Exibe o progresso da fase
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(phase_progress)
        with col2:
            st.markdown(f"<p style='text-align: right; font-size: 0.9rem; margin-top: 10px;'>{phase_completed}/{phase_total} ({phase_progress:.0%})</p>", unsafe_allow_html=True)
        
        # Lista as tarefas
        for i, task in enumerate(tasks):
            if task.get('is_note'):
                st.warning(task['text'])
                continue

            task_id = task['id']
            cols = st.columns([0.1, 1.6, 0.15, 0.15])
            
            # Checkbox
            with cols[0]:
                current_status = task.get('checked', False)
                is_checked = st.checkbox(
                    "", 
                    value=current_status, 
                    key=f"cb_{task_id}_{i}",
                    help="Marcar como concluída"
                )
                
                if is_checked != current_status:
                    update_task_status(phase, task_id, is_checked)
                    # Pequeno delay para mostrar o status de sincronização
                    time.sleep(0.5)
                    st.rerun()

            # Texto da tarefa (editável ou não)
            with cols[1]:
                if st.session_state.editing_task == task_id:
                    # Modo edição
                    new_text = st.text_input(
                        "Editar tarefa", 
                        value=task['text'], 
                        key=f"edit_{task_id}",
                        label_visibility="collapsed",
                        placeholder="Digite o novo texto da tarefa..."
                    )
                    
                    # Botões de ação para edição
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("💾 Salvar", key=f"save_{task_id}", type="primary"):
                            if new_text.strip():
                                update_task_text(phase, task_id, new_text)
                                st.rerun()
                            else:
                                st.error("O texto da tarefa não pode estar vazio!")
                    
                    with col_cancel:
                        if st.button("❌ Cancelar", key=f"cancel_{task_id}"):
                            st.session_state.editing_task = None
                            st.rerun()
                else:
                    # Modo visualização
                    checked_class = "checked" if task.get('checked') else ""
                    status_icon = "✅" if task.get('checked') else "⭕"
                    st.markdown(
                        f"<div class='task-container'><p class='task-text {checked_class}'>{status_icon} {task['text']}</p></div>", 
                        unsafe_allow_html=True
                    )
            
            # Botão de editar
            with cols[2]:
                if st.session_state.editing_task != task_id:
                    if st.button("✏️", key=f"btn_edit_{task_id}_{i}", help="Editar tarefa"):
                        st.session_state.editing_task = task_id
                        st.rerun()
                        
            # Botão de excluir
            with cols[3]:
                if st.session_state.editing_task != task_id:
                    if st.button("🗑️", key=f"btn_del_{task_id}_{i}", help="Excluir tarefa"):
                        if st.session_state.get(f"confirm_delete_{task_id}"):
                            delete_task(phase, task_id)
                            if f"confirm_delete_{task_id}" in st.session_state:
                                del st.session_state[f"confirm_delete_{task_id}"]
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{task_id}"] = True
                            st.warning("⚠️ Clique novamente para confirmar a exclusão!")
                            st.rerun()
        
        # Seção para adicionar nova tarefa
        st.markdown("---")
        st.markdown("**➕ Adicionar Nova Tarefa**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_text = st.text_input(
                "Nova tarefa", 
                key=f"new_task_{phase}",
                placeholder="Digite aqui a nova tarefa para esta fase...",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("➕ Adicionar", key=f"add_btn_{phase}", type="primary"):
                if new_text.strip():
                    add_task(phase, new_text.strip())
                    # Limpa o campo
                    st.session_state[f"new_task_{phase}"] = ""
                    st.rerun()
                else:
                    st.error("Digite o texto da tarefa!")

# --- Estatísticas Finais ---
st.markdown("---")
st.subheader("📊 Estatísticas do Planejamento")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total de Tarefas",
        value=total_tasks,
        help="Número total de tarefas no checklist"
    )

with col2:
    st.metric(
        label="Concluídas",
        value=completed_tasks,
        delta=f"+{completed_tasks}",
        help="Tarefas já concluídas"
    )

with col3:
    st.metric(
        label="Restantes",
        value=total_tasks - completed_tasks,
        delta=f"-{total_tasks - completed_tasks}" if completed_tasks > 0 else None,
        help="Tarefas ainda pendentes"
    )

with col4:
    st.metric(
        label="Progresso",
        value=f"{progress:.0%}",
        help="Percentual de conclusão geral"
    )

# --- Próximas Tarefas Importantes ---
st.subheader("⚡ Próximas Tarefas Prioritárias")

# Encontra tarefas não concluídas que contêm prazos
priority_tasks = []
for phase, tasks in st.session_state.checklist.items():
    for task in tasks:
        if (not task.get('checked', False) and 
            not task.get('is_note', False) and
            ('PRAZO:' in task['text'] or 'ATENÇÃO' in task['text'] or 'URGENTE' in task['text'])):
            priority_tasks.append((phase, task))

if priority_tasks:
    for phase, task in priority_tasks[:5]:  # Mostra até 5 tarefas prioritárias
        st.warning(f"**{phase}**: {task['text']}")
else:
    # Se não há tarefas prioritárias, mostra as próximas não concluídas
    next_tasks = []
    for phase, tasks in st.session_state.checklist.items():
        for task in tasks:
            if not task.get('checked', False) and not task.get('is_note', False):
                next_tasks.append((phase, task))
                if len(next_tasks) >= 3:
                    break
        if len(next_tasks) >= 3:
            break
    
    if next_tasks:
        st.info("**Próximas tarefas a fazer:**")
        for phase, task in next_tasks:
            st.info(f"• **{phase}**: {task['text']}")
    else:
        st.success("🎉 **Parabéns! Todas as tarefas foram concluídas!** 🎉")

# --- Dicas e Lembretes ---
st.subheader("💡 Dicas Importantes")
st.info("""
📝 **Lembretes Importantes:**
- **Documentos**: Certidões têm prazo de validade (90 dias)
- **Casamento Civil**: Deve ser realizado ANTES do religioso
- **Xerox da Certidão Civil**: Entregar na paróquia no mesmo dia
- **Backup**: Este checklist é salvo automaticamente na nuvem
- **Sincronização**: As alterações aparecem para ambos em tempo real
""")

# --- Rodapé ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p class="footer-text">Juntos para Sempre</p>
    <p class="footer-subtext">Cada tarefa completada nos aproxima do nosso sonho realizado ❤️</p>
    <p style="font-size: 0.8rem; color: #999; margin-top: 1rem;">
        💾 Dados salvos automaticamente • 🔄 Sincronização em tempo real
    </p>
</div>
""", unsafe_allow_html=True)

# Lembre-se de atualizar o arquivo requirements.txt para que esta linha funcione!
import streamlit as st
import datetime
import streamlit.components.v1 as components
import json
from supabase import create_client, Client
import time
from collections import OrderedDict

# --- Configuração da Página ---
st.set_page_config(
    page_title="Checklist do Casamento | Daniela & Thiago",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS Customizado Responsivo com Modo Escuro ---
st.markdown("""
<style>
/* Importando as fontes do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Montserrat:wght@400;500;600&display=swap');

/* --- VARIÁVEIS CSS PARA TEMA CLARO E ESCURO --- */
:root {
    --bg-primary: #fff9fb;
    --bg-secondary: #ffffff;
    --bg-gradient-start: #fff0f3;
    --bg-gradient-middle: #ffe0e6;
    --bg-gradient-end: #fff5f8;
    --text-primary: #333333;
    --text-secondary: #555555;
    --text-muted: #666666;
    --accent-color: #c2185b;
    --accent-light: rgba(194, 24, 91, 0.1);
    --border-color: rgba(194, 24, 91, 0.1);
    --shadow-light: rgba(194, 24, 91, 0.15);
    --shadow-medium: rgba(194, 24, 91, 0.25);
    --card-bg: #ffffff;
    --input-bg: #ffffff;
    --success-bg: #d4edda;
    --success-text: #155724;
    --warning-bg: #fff3cd;
    --warning-text: #856404;
    --error-bg: #f8d7da;
    --error-text: #721c24;
    --countdown-bg: linear-gradient(135deg, #fff0f3 0%, #ffe0e6 50%, #fff5f8 100%);
    --romantic-quote-bg: linear-gradient(135deg, rgba(194, 24, 91, 0.05) 0%, rgba(255, 192, 203, 0.05) 100%);
}

/* Tema Escuro */
[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --bg-gradient-start: #2a1f23;
    --bg-gradient-middle: #3d2a30;
    --bg-gradient-end: #2a1f26;
    --text-primary: #ffffff;
    --text-secondary: #e0e0e0;
    --text-muted: #b0b0b0;
    --accent-color: #ff4081;
    --accent-light: rgba(255, 64, 129, 0.2);
    --border-color: rgba(255, 64, 129, 0.3);
    --shadow-light: rgba(255, 64, 129, 0.3);
    --shadow-medium: rgba(255, 64, 129, 0.4);
    --card-bg: #333333;
    --input-bg: #404040;
    --success-bg: #1e4d2b;
    --success-text: #90ee90;
    --warning-bg: #4d3d1e;
    --warning-text: #ffd700;
    --error-bg: #4d1e1e;
    --error-text: #ffb3b3;
    --countdown-bg: linear-gradient(135deg, #2a1f23 0%, #3d2a30 50%, #2a1f26 100%);
    --romantic-quote-bg: linear-gradient(135deg, rgba(255, 64, 129, 0.1) 0%, rgba(255, 105, 180, 0.1) 100%);
}

/* Auto detecção do modo escuro do sistema */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --bg-gradient-start: #2a1f23;
        --bg-gradient-middle: #3d2a30;
        --bg-gradient-end: #2a1f26;
        --text-primary: #ffffff;
        --text-secondary: #e0e0e0;
        --text-muted: #b0b0b0;
        --accent-color: #ff4081;
        --accent-light: rgba(255, 64, 129, 0.2);
        --border-color: rgba(255, 64, 129, 0.3);
        --shadow-light: rgba(255, 64, 129, 0.3);
        --shadow-medium: rgba(255, 64, 129, 0.4);
        --card-bg: #333333;
        --input-bg: #404040;
        --success-bg: #1e4d2b;
        --success-text: #90ee90;
        --warning-bg: #4d3d1e;
        --warning-text: #ffd700;
        --error-bg: #4d1e1e;
        --error-text: #ffb3b3;
        --countdown-bg: linear-gradient(135deg, #2a1f23 0%, #3d2a30 50%, #2a1f26 100%);
        --romantic-quote-bg: linear-gradient(135deg, rgba(255, 64, 129, 0.1) 0%, rgba(255, 105, 180, 0.1) 100%);
    }
}

/* --- ESTILOS GERAIS --- */
body { 
    background-color: var(--bg-primary);
    color: var(--text-primary);
    transition: all 0.3s ease;
}

.stApp {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Montserrat', sans-serif;
    min-height: 100vh;
    transition: all 0.3s ease;
}

#MainMenu, footer { display: none; }

/* --- BOTÃO DE ALTERNÂNCIA DE TEMA --- */
.theme-toggle {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1001;
    background: var(--card-bg);
    border: 2px solid var(--accent-color);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px var(--shadow-light);
}

.theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px var(--shadow-medium);
}

/* --- CABEÇALHO RESPONSIVO --- */
.wedding-names {
    font-family: 'Dancing Script', cursive;
    font-size: clamp(2.5rem, 8vw, 4.5rem);
    font-weight: 700;
    text-align: center;
    color: var(--accent-color);
    margin-bottom: -10px;
    transition: all 0.3s ease;
}

.wedding-date {
    font-family: 'Montserrat', sans-serif;
    text-align: center;
    font-size: clamp(0.9rem, 3vw, 1.1rem);
    color: var(--text-secondary);
    letter-spacing: 1px;
    margin-bottom: 2rem;
}

/* --- PROGRESSO RESPONSIVO --- */
.progress-section {
    text-align: center;
    margin-bottom: 2rem;
    padding: 0 1rem;
}

.progress-text {
    font-size: clamp(1rem, 4vw, 1.2rem);
    font-weight: 600;
    color: var(--accent-color);
}

.progress-subtext {
    color: var(--text-muted);
    font-size: clamp(0.8rem, 3vw, 1rem);
}

/* --- STATUS DE SINCRONIZAÇÃO RESPONSIVO --- */
.sync-status {
    position: fixed;
    top: 10px;
    right: 10px;
    padding: 0.5rem;
    border-radius: 5px;
    font-size: clamp(0.7rem, 2vw, 0.8rem);
    z-index: 1000;
    max-width: 200px;
    word-wrap: break-word;
}

.sync-success {
    background-color: var(--success-bg);
    color: var(--success-text);
}

.sync-error {
    background-color: var(--error-bg);
    color: var(--error-text);
}

.sync-loading {
    background-color: var(--warning-bg);
    color: var(--warning-text);
}

/* --- CONTAGEM REGRESSIVA RESPONSIVA --- */
.countdown-section {
    text-align: center;
    margin: 2rem 0;
    background: var(--countdown-bg);
    padding: clamp(1.5rem, 5vw, 2.5rem);
    border-radius: 25px;
    box-shadow: 0 8px 32px var(--shadow-light);
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
}

.countdown-title {
    font-family: 'Dancing Script', cursive;
    font-size: clamp(2rem, 6vw, 2.8rem);
    font-weight: 700;
    color: var(--accent-color);
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    position: relative;
    z-index: 2;
}

.countdown-subtitle {
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(0.8rem, 3vw, 1rem);
    color: var(--text-muted);
    margin-bottom: 2rem;
    position: relative;
    z-index: 2;
}

.countdown-container-modern {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: clamp(0.5rem, 3vw, 1.5rem);
    justify-items: center;
    position: relative;
    z-index: 2;
    max-width: 500px;
    margin: 0 auto;
}

.countdown-item {
    background: var(--card-bg);
    padding: clamp(1rem, 3vw, 1.5rem);
    border-radius: 20px;
    min-width: 80px;
    width: 100%;
    max-width: 120px;
    box-shadow: 0 8px 25px var(--shadow-light);
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.countdown-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px var(--shadow-medium);
}

.countdown-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-color), #ff4081, var(--accent-color));
}

.countdown-number {
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(1.5rem, 5vw, 2.5rem);
    font-weight: 700;
    color: var(--accent-color);
    display: block;
    line-height: 1;
    margin-bottom: 0.5rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.countdown-label {
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(0.7rem, 2vw, 0.85rem);
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 500;
}

.countdown-hearts {
    margin-top: 1.5rem;
    font-size: clamp(1.2rem, 4vw, 1.5rem);
    opacity: 0.7;
    animation: heartbeat 2s ease-in-out infinite;
}

@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* --- CITAÇÃO ROMÂNTICA RESPONSIVA --- */
.romantic-quote {
    text-align: center;
    margin: 2rem 0;
    padding: clamp(1rem, 4vw, 1.5rem);
    background: var(--romantic-quote-bg);
    border-radius: 15px;
    border-left: 4px solid var(--accent-color);
}

.romantic-quote p {
    font-family: 'Dancing Script', cursive;
    font-size: clamp(1.3rem, 4vw, 1.8rem);
    color: var(--accent-color);
    font-style: italic;
    margin: 0;
}

.romantic-quote small {
    font-family: 'Montserrat', sans-serif;
    color: var(--text-muted);
    font-size: clamp(0.8rem, 2vw, 0.9rem);
}

/* --- CHECKLIST RESPONSIVO --- */
.stExpander {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px var(--shadow-light) !important;
    margin-bottom: 1rem !important;
    transition: all 0.3s ease !important;
}

.stExpander:hover {
    box-shadow: 0 6px 20px var(--shadow-medium) !important;
}

.task-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.task-text {
    margin: 0;
    padding-left: 10px;
    font-size: clamp(0.9rem, 3vw, 1rem);
    color: var(--text-primary);
    transition: all 0.3s ease;
    flex: 1;
    word-wrap: break-word;
    line-height: 1.4;
}

.task-text.checked {
    text-decoration: line-through;
    color: var(--text-muted);
    opacity: 0.7;
}

/* --- BOTÕES RESPONSIVOS --- */
.stButton > button {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    padding: 0.25rem 0.5rem !important;
    font-size: clamp(0.7rem, 2vw, 0.9rem) !important;
    transition: all 0.3s ease !important;
    min-height: 38px !important;
}

.stButton > button:hover {
    background-color: var(--accent-color) !important;
    color: white !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px var(--shadow-light) !important;
}

/* --- INPUTS RESPONSIVOS --- */
.stTextInput > div > div > input {
    background-color: var(--input-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    font-size: clamp(0.9rem, 3vw, 1rem) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 0 2px var(--accent-light) !important;
}

/* --- CHECKBOXES RESPONSIVOS --- */
.stCheckbox > label {
    color: var(--text-primary) !important;
    font-size: clamp(0.9rem, 3vw, 1rem) !important;
}

/* --- ALERTAS RESPONSIVOS --- */
.stAlert {
    background-color: var(--warning-bg) !important;
    color: var(--warning-text) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    font-size: clamp(0.8rem, 2.5vw, 0.9rem) !important;
}

.stSuccess {
    background-color: var(--success-bg) !important;
    color: var(--success-text) !important;
}

.stError {
    background-color: var(--error-bg) !important;
    color: var(--error-text) !important;
}

/* --- MÉTRICAS RESPONSIVAS --- */
.metric-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

/* --- RODAPÉ RESPONSIVO --- */
.footer {
    text-align: center;
    padding: clamp(1rem, 4vw, 2rem);
    background-color: var(--card-bg);
    border-radius: 15px;
    margin-top: 2rem;
    box-shadow: 0 4px 15px var(--shadow-light);
}

.footer-text {
    font-size: clamp(1.2rem, 4vw, 1.5rem);
    font-weight: 600;
    color: var(--accent-color);
}

.footer-subtext {
    color: var(--text-secondary);
    font-size: clamp(0.9rem, 3vw, 1rem);
}

/* --- MEDIA QUERIES ESPECÍFICAS --- */
@media (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    
    .countdown-container-modern {
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
    
    .countdown-item {
        padding: 1rem 0.5rem;
    }
    
    .task-container {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .task-text {
        padding-left: 0;
        width: 100%;
    }
    
    .sync-status {
        position: relative;
        top: auto;
        right: auto;
        margin-bottom: 1rem;
        width: 100%;
    }
    
    .theme-toggle {
        position: relative;
        top: auto;
        left: auto;
        margin: 1rem auto;
    }
}

@media (max-width: 480px) {
    .countdown-container-modern {
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
    }
    
    .countdown-item {
        min-width: 70px;
        padding: 0.8rem 0.3rem;
    }
    
    .countdown-number {
        font-size: 1.8rem;
    }
    
    .countdown-label {
        font-size: 0.7rem;
    }
    
    .metric-container {
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
    }
}

/* --- ANIMAÇÕES SUAVES --- */
* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

/* --- SCROLLBAR PERSONALIZADA --- */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--accent-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #ff4081;
}
</style>
""", unsafe_allow_html=True)

# --- SCRIPT PARA ALTERNÂNCIA DE TEMA ---
theme_toggle_script = """
<script>
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Atualiza o ícone
    const toggle = document.querySelector('.theme-toggle');
    if (toggle) {
        toggle.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    
    document.body.setAttribute('data-theme', theme);
    
    // Cria o botão de alternância
    const toggle = document.createElement('div');
    toggle.className = 'theme-toggle';
    toggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    toggle.onclick = toggleTheme;
    toggle.title = 'Alternar tema claro/escuro';
    
    document.body.appendChild(toggle);
}

// Inicializa o tema quando a página carrega
document.addEventListener('DOMContentLoaded', initTheme);

// Para Streamlit, tenta inicializar após um pequeno delay
setTimeout(initTheme, 500);
</script>
"""

components.html(theme_toggle_script, height=0)

# --- CONFIGURAÇÃO DO SUPABASE (VERSÃO CORRETA E COMPLETA) ---
@st.cache_resource
def init_supabase():
    """Inicializa a conexão com o Supabase de forma robusta"""
    url = None
    key = None

    # Tenta encontrar as credenciais em diferentes formatos
    if "supabase" in st.secrets and "supabase_url" in st.secrets.supabase:
        url = st.secrets.supabase["supabase_url"]
        key = st.secrets.supabase["supabase_key"]
    elif "general" in st.secrets and "supabase_url" in st.secrets.general:
        url = st.secrets.general["supabase_url"]
        key = st.secrets.general["supabase_key"]
    elif "supabase_url" in st.secrets and "supabase_key" in st.secrets:
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]

    # Se encontrou as credenciais, tenta conectar
    if url and key:
        try:
            supabase_client = create_client(url, key)
            # Testa a conexão fazendo uma pequena consulta
            supabase_client.table("checklists").select("id").limit(1).execute()
            return supabase_client
        except Exception as e:
            st.error(f"❌ Falha ao conectar com o Supabase: Verifique a URL, a Chave e se a tabela 'checklists' existe. Erro: {e}")
            return None
    else:
        # Se não encontrou as credenciais em nenhum formato
        st.error("⚠️ As credenciais do Supabase não foram encontradas nos segredos do Streamlit.")
        st.info("Verifique se o seu arquivo de secrets está configurado com [supabase] ou com as variáveis supabase_url e supabase_key.")
        return None

def show_sync_status(status, message=""):
    """Exibe o status de sincronização"""
    if status == "success":
        st.markdown(f'<div class="sync-status sync-success">✅ Sincronizado {message}</div>', unsafe_allow_html=True)
    elif status == "error":
        st.markdown(f'<div class="sync-status sync-error">❌ Erro na sincronização {message}</div>', unsafe_allow_html=True)
    elif status == "loading":
        st.markdown(f'<div class="sync-status sync-loading">⏳ Sincronizando... {message}</div>', unsafe_allow_html=True)

# --- STATUS DE CONEXÃO COM DEBUG ---
st.markdown("### 🔗 Status da Conexão")
supabase = init_supabase()

if supabase:
    st.success("🔄 Conectado - Alterações são sincronizadas automaticamente!")
else:
    st.warning("⚠️ Modo Offline - Alterações não serão salvas permanentemente")
    st.info("Para conectar ao Supabase, verifique as credenciais nos secrets")

CHECKLIST_ID = "daniela_thiago_2026"

# --- DADOS INICIAIS DO CHECKLIST (ORDENADOS CORRETAMENTE) ---
initial_checklist_data = OrderedDict([
    ("Fase 1: Planejamento Inicial (até Dez/25)", [
        {'id': 'definir-orcamento', 'text': 'Definir o Orçamento Geral do Casamento.', 'checked': False},
        {'id': 'lista-convidados-preliminar', 'text': 'Criar a Lista Preliminar de Convidados.', 'checked': False},
        {'id': 'escolher-padrinhos', 'text': 'Convidar Padrinhos e Madrinhas (máx. 3 casais por noivo).', 'checked': False},
        {'id': 'ponto-atencao-padre', 'text': '❤️ ATENÇÃO ESPECIAL: Agendar conversa com Padre Carlos para alinhar detalhes sobre viuvez e o processo religioso.', 'is_note': True},
        {'id': 'agendar-curso-noivos', 'text': 'Pesquisar e se inscrever no Curso de Noivos.', 'checked': False},
        {'id': 'confirmar-salao', 'text': 'Confirmar a reserva do salão anexo da igreja para a recepção.', 'checked': False},
        {'id': 'design-convites', 'text': 'Definir o design dos convites.', 'checked': False},
    ]),
    ("Fase 2: Contratando Fornecedores (Jan/26 a Mar/26)", [
        {'id': 'contato-paroquia', 'text': 'Contato Inicial com a Paróquia: Agendar data religiosa (05/09/2026).', 'checked': False},
        {'id': 'foto-video', 'text': 'Conversar e fechar com a amiga fotógrafa (repassar regras).', 'checked': False},
        {'id': 'musica-cerimonia', 'text': 'Conversar e fechar com os amigos músicos (repertório religioso).', 'checked': False},
        {'id': 'decoracao', 'text': 'Contratar florista/decoração (repassar regras).', 'checked': False},
        {'id': 'bolo-doces', 'text': 'Pesquisar e agendar degustações de bolo e doces.', 'checked': False},
        {'id': 'definir-lua-de-mel', 'text': 'Lua de Mel: Definir Destino e reservar passagens/hotéis.', 'checked': False},
        {'id': 'pesquisar-vestido-noiva', 'text': 'Vestido da Noiva: Iniciar pesquisa e provas.', 'checked': False},
        {'id': 'pesquisar-traje-noivo', 'text': 'Traje do Noivo: Iniciar pesquisa.', 'checked': False},
        {'id': 'pesquisar-dia-noiva', 'text': 'Pesquisar profissional para o Dia da Noiva em casa.', 'checked': False},
    ]),
    ("Fase 3: Detalhes e Documentos (Abr/26 a Mai/26)", [
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
    ]),
    ("Fase 4: Processos Oficiais (Jun/26 a Jul/26)", [
        {'id': 'solicitar-docs-daniela', 'text': '🗓️ PRAZO: A partir de 04/06/2026 - Daniela: Solicitar certidões de Casamento Anterior, Óbito e Inventário (valem 90 dias).', 'checked': False},
        {'id': 'solicitar-docs-thiago', 'text': '🗓️ PRAZO: A partir de 04/06/2026 - Thiago: Solicitar certidão de Nascimento (vale 90 dias).', 'checked': False},
        {'id': 'marcar-entrevista-padre', 'text': '🗓️ PRAZO: Até 27/06/26 - Marcar Entrevista com o Padre e iniciar o processo na Paróquia.', 'checked': False},
        {'id': 'entregar-docs-paroquia', 'text': 'Entregar documentos do processo religioso na paróquia.', 'checked': False},
        {'id': 'habilitacao-cartorio', 'text': '🗓️ PRAZO: Início de Julho - Dar Entrada na Habilitação do Casamento Civil com as testemunhas.', 'checked': False},
        {'id': 'imprimir-enviar-convites', 'text': 'Imprimir e começar a enviar/entregar os convites.', 'checked': False},
    ]),
    ("Fase 5: Reta Final (Agosto/2026)", [
        {'id': 'confirmar-presenca-rsvp', 'text': '🗓️ PRAZO: Até 22/08/26 - Confirmar Presença (RSVP).', 'checked': False},
        {'id': 'reuniao-final-fornecedores', 'text': 'Reunião Final com todos os fornecedores.', 'checked': False},
        {'id': 'prova-final-trajes', 'text': 'Prova Final do Vestido e Terno.', 'checked': False},
        {'id': 'definir-leituras-musicas', 'text': 'Definir com o Padre as leituras e músicas.', 'checked': False},
        {'id': 'prova-cabelo-maquiagem', 'text': 'Fazer teste final de cabelo e maquiagem.', 'checked': False},
    ]),
    ("Na Semana do Casamento", [
        {'id': 'casamento-civil', 'text': '❤️ GRANDE PASSO: 03/09/2026 - Casamento Civil no Cartório!', 'checked': False},
        {'id': 'entregar-certidao-civil', 'text': '⚠️ URGENTE: 03/09/2026 - Entregar a Xerox da Certidão Civil na Paróquia!', 'is_note': True},
        {'id': 'buscar-trajes', 'text': 'Buscar o Vestido e o Terno.', 'checked': False},
        {'id': 'confirmar-horarios-todos', 'text': 'Confirmar horário com TODOS os profissionais.', 'checked': False},
        {'id': 'finalizar-tercos', 'text': 'Finalizar a produção e embalagem dos terços.', 'checked': False},
        {'id': 'organizar-malas-lua-de-mel', 'text': 'Organizar as Malas da Lua de Mel.', 'checked': False},
        {'id': 'relaxar', 'text': 'Descansar e relaxar! Delegar as últimas tarefas.', 'checked': False},
    ]),
    ("O Grande Dia do Casamento", [
        {'id': 'cerimonia-religiosa', 'text': '💒 05/09/2026 - 16h - Cerimônia Religiosa na Igreja!', 'checked': False},
        {'id': 'recepcao-festa', 'text': '🎉 Recepção e Festa no salão anexo!', 'checked': False},
        {'id': 'entregar-tercos-convidados', 'text': '🙏 Entregar os terços de Nossa Senhora das Lágrimas aos convidados.', 'checked': False},
        {'id': 'fotos-especiais', 'text': '📸 Sessão de fotos especiais com os noivos.', 'checked': False},
        {'id': 'corte-bolo', 'text': '🎂 Cerimônia do corte do bolo.', 'checked': False},
        {'id': 'primeira-danca', 'text': '💃🕺 Primeira dança como casal.', 'checked': False},
        {'id': 'despedida-convidados', 'text': '👋 Despedida dos convidados com gratidão.', 'checked': False},
        {'id': 'inicio-lua-de-mel', 'text': '✈️ Partida para a Lua de Mel!', 'checked': False},
    ])
])

# --- FUNÇÕES DE MANIPULAÇÃO DO CHECKLIST COM SUPABASE ---
def get_checklist_from_supabase():
    """Carrega o checklist do Supabase"""
    if not supabase:
        return initial_checklist_data
        
    try:
        response = supabase.table("checklists").select("data, updated_at").eq("id", CHECKLIST_ID).execute()
        
        if response.data:
            data = response.data[0]["data"]
            # Converte para OrderedDict para manter a ordem
            if isinstance(data, dict) and not isinstance(data, OrderedDict):
                ordered_data = OrderedDict()
                # Define a ordem das fases
                phase_order = [
                    "Fase 1: Planejamento Inicial (até Dez/25)",
                    "Fase 2: Contratando Fornecedores (Jan/26 a Mar/26)",
                    "Fase 3: Detalhes e Documentos (Abr/26 a Mai/26)",
                    "Fase 4: Processos Oficiais (Jun/26 a Jul/26)",
                    "Fase 5: Reta Final (Agosto/2026)",
                    "Na Semana do Casamento",
                    "O Grande Dia do Casamento"
                ]
                # Adiciona as fases na ordem correta
                for phase in phase_order:
                    if phase in data:
                        ordered_data[phase] = data[phase]
                # Adiciona qualquer fase extra que não esteja na lista
                for phase, tasks in data.items():
                    if phase not in ordered_data:
                        ordered_data[phase] = tasks
                return ordered_data
            return data
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
        # Converte OrderedDict para dict normal para serialização JSON
        clean_data = dict(data) if isinstance(data, OrderedDict) else data
        clean_data = json.loads(json.dumps(clean_data))
        
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

# --- CORAÇÕES FLUTUANTES ---
floating_hearts_html = """
<div class="floating-hearts" id="floating-hearts"></div>
<script>
function createFloatingHeart() {
    const heartsContainer = document.getElementById('floating-hearts');
    if (!heartsContainer) return;
    
    const heart = document.createElement('div');
    heart.className = 'floating-heart';
    heart.innerHTML = Math.random() > 0.5 ? '💕' : '💖';
    heart.style.left = Math.random() * 100 + '%';
    heart.style.animationDelay = Math.random() * 5 + 's';
    heart.style.animationDuration = (8 + Math.random() * 4) + 's';
    
    heartsContainer.appendChild(heart);
    
    setTimeout(() => {
        if (heart.parentNode) {
            heart.parentNode.removeChild(heart);
        }
    }, 12000);
}

// Cria corações a cada 4 segundos
setInterval(createFloatingHeart, 4000);

// Cria alguns corações iniciais
for(let i = 0; i < 3; i++) {
    setTimeout(createFloatingHeart, i * 1500);
}
</script>
"""
components.html(floating_hearts_html, height=0)

# --- FRASE ROMÂNTICA ---
romantic_quotes = [
    "O amor não se vê com os olhos, mas com o coração.",
    "Duas almas, um só coração.",
    "O amor verdadeiro nunca tem fim.",
    "Juntos somos mais fortes, unidos somos eternos.",
    "Cada dia ao seu lado é um presente."
]

import random
today_quote = random.choice(romantic_quotes)

st.markdown(f"""
<div class="romantic-quote">
    <p>"{today_quote}"</p>
    <small>— Frase do dia para nosso amor —</small>
</div>
""", unsafe_allow_html=True)

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
        if supabase:
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

# --- CONTAGEM REGRESSIVA CORRIGIDA ---
wedding_date = datetime.datetime(2026, 9, 5, 16, 0, 0)
now = datetime.datetime.now()
time_remaining = wedding_date - now

# Cria a contagem regressiva usando Streamlit nativo ao invés de HTML/JS problemático
st.markdown('<div class="countdown-section">', unsafe_allow_html=True)
st.markdown('<h2 class="countdown-title">Contagem Regressiva para o Grande Dia</h2>', unsafe_allow_html=True)
st.markdown('<p class="countdown-subtitle">Cada segundo nos aproxima do nosso "Sim" eterno</p>', unsafe_allow_html=True)

if time_remaining.total_seconds() > 0:
    days = time_remaining.days
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Exibe a contagem usando colunas do Streamlit
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="countdown-item">
            <span class="countdown-number">{days}</span>
            <span class="countdown-label">Dias</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="countdown-item">
            <span class="countdown-number">{hours:02d}</span>
            <span class="countdown-label">Horas</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="countdown-item">
            <span class="countdown-number">{minutes:02d}</span>
            <span class="countdown-label">Minutos</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="countdown-item">
            <span class="countdown-number">{seconds:02d}</span>
            <span class="countdown-label">Segundos</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="countdown-celebration">🎉 Feliz Casamento! 🎉</div>', unsafe_allow_html=True)

st.markdown('<div class="countdown-hearts">💕 ✨ 💕 ✨ 💕</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh da contagem a cada 30 segundos
time.sleep(0.1)  # Pequeno delay para não sobrecarregar

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
                    st.rerun()
                else:
                    st.error("Digite o texto da tarefa!")

# --- Estatísticas Românticas ---
st.markdown("---")
st.subheader("💕 Nosso Progresso de Amor")

col1, col2, col3, col4 = st.columns(4)

# Calcula marcos especiais
days_until_wedding = (wedding_date - datetime.datetime.now()).days
percentage_complete = progress * 100

with col1:
    st.metric(
        label="💕 Total de Sonhos",
        value=total_tasks,
        help="Cada tarefa é um passo para realizarmos nossos sonhos"
    )

with col2:
    st.metric(
        label="✨ Sonhos Realizados",
        value=completed_tasks,
        delta=f"+{completed_tasks} realizados",
        help="Tarefas já concluídas com amor"
    )

with col3:
    st.metric(
        label="🎯 Faltam Realizar",
        value=total_tasks - completed_tasks,
        delta=f"-{total_tasks - completed_tasks}" if completed_tasks > 0 else None,
        help="Sonhos ainda por realizar juntos"
    )

with col4:
    st.metric(
        label="💖 Progresso do Amor",
        value=f"{percentage_complete:.0f}%",
        help="Percentual de conclusão do nosso grande dia"
    )

# Marco especial baseado no progresso
if percentage_complete >= 75:
    st.success("🎉 **MARCO ESPECIAL**: Vocês estão quase lá! Menos de 25% para o grande dia!")
elif percentage_complete >= 50:
    st.info("💫 **MARCO ESPECIAL**: Metade do caminho percorrido! Vocês estão indo muito bem!")
elif percentage_complete >= 25:
    st.info("🌟 **MARCO ESPECIAL**: Um quarto do planejamento concluído! Continuem assim!")
else:
    st.info("💕 **INÍCIO DA JORNADA**: Nosso grande amor começa com um primeiro passo!")

# Dias especiais até o casamento
if days_until_wedding > 365:
    st.info(f"📅 Ainda temos **{days_until_wedding // 365} ano(s)** para planejar cada detalhe com amor!")
elif days_until_wedding > 30:
    st.info(f"📅 Faltam apenas **{days_until_wedding}** dias para nosso grande dia!")
elif days_until_wedding > 0:
    st.warning(f"🔥 **RETA FINAL!** Apenas **{days_until_wedding}** dias para o casamento!")
else:
    st.success("💒 **É HOJE!** O grande dia chegou!")

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
- **Modo Escuro**: Use o botão 🌙/☀️ no canto superior esquerdo para alternar temas
""")

# --- Instruções para Modo Mobile ---
st.markdown("---")
st.markdown("### 📱 **Dica para Celular**")
st.info("""
📱 **Para melhor experiência no celular:**
- Use o botão **🌙** no canto superior esquerdo para ativar o **modo escuro**
- O modo escuro melhora muito a legibilidade em telas pequenas
- O tema se adapta automaticamente às configurações do seu telefone
- Todas as funcionalidades funcionam perfeitamente no mobile
""")

# --- Rodapé ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p class="footer-text">Juntos para Sempre</p>
    <p class="footer-subtext">Cada tarefa completada nos aproxima do nosso sonho realizado ❤️</p>
    <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 1rem;">
        💾 Dados salvos automaticamente • 🔄 Sincronização em tempo real • 🌙 Modo escuro disponível
    </p>
</div>
""", unsafe_allow_html=True)

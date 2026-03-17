import os
import json
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from supabase import create_client, Client
from functools import wraps
from collections import defaultdict

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "puc-chat-secret-key-2024")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Credenciais de login
LOGIN_USER = os.getenv("LOGIN_USER", "admin")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "puc2024")

# Decorador para rotas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUXILIAR: BUSCA TOTAL DE DADOS ---
def get_all_supabase_data(table_name):
    """Auxiliar para buscar todos os dados contornando o limite de 1000 registros."""
    all_data = []
    limit = 1000
    offset = 0
    
    while True:
        response = supabase.table(table_name) \
            .select("*") \
            .range(offset, offset + limit - 1) \
            .execute()
        
        batch = response.data
        if not batch:
            break
            
        all_data.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
        
    return all_data

# --- ROTAS DE PÁGINAS ---

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == LOGIN_USER and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401
    
    return render_template('chat_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('chat_dashboard.html', username=session.get('username'))

@app.route('/conversas')
@login_required
def conversas():
    return render_template('chat_conversas.html', username=session.get('username'))

@app.route('/conversa/<session_id>')
@login_required
def conversa_detalhe(session_id):
    return render_template('chat_detalhe.html', session_id=session_id, username=session.get('username'))

# --- ROTAS DE API (CORRIGIDAS) ---

@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """Retorna estatísticas completas sem a trava de 1000 linhas."""
    try:
        messages = get_all_supabase_data("conteudo_puc_conversas")
        
        if not messages:
            return jsonify({
                'success': True,
                'total_messages': 0,
                'total_conversations': 0,
                'human_messages': 0,
                'ai_messages': 0,
                'system_messages': 0
            })
        
        sessions = set()
        human_count = 0
        ai_count = 0
        system_count = 0
        
        for msg in messages:
            sessions.add(msg['session_id'])
            try:
                m_json = json.loads(msg['message']) if isinstance(msg['message'], str) else msg['message']
                msg_type = m_json.get('type', '').lower()
                
                if msg_type == 'human': human_count += 1
                elif msg_type == 'ai': ai_count += 1
                elif msg_type == 'system': system_count += 1
            except:
                continue
        
        return jsonify({
            'success': True,
            'total_messages': len(messages),
            'total_conversations': len(sessions),
            'human_messages': human_count,
            'ai_messages': ai_count,
            'system_messages': system_count
        })
    except Exception as e:
        logger.error(f"Erro em stats: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/conversas', methods=['GET'])
@login_required
def get_conversas():
    """Retorna lista de todas as conversas agrupadas, processando o banco inteiro."""
    try:
        all_data = get_all_supabase_data("conteudo_puc_conversas")
        
        if not all_data:
            return jsonify({'success': True, 'conversations': []})
        
        conversations_dict = defaultdict(list)
        for msg in all_data:
            try:
                m_json = json.loads(msg['message']) if isinstance(msg['message'], str) else msg['message']
                conversations_dict[msg['session_id']].append({
                    'id': msg['id'],
                    'type': m_json.get('type', '').lower(),
                    'content': m_json.get('content', ''),
                    'created_at': msg.get('created_at', '')
                })
            except: continue
        
        conversations = []
        for session_id, msgs in conversations_dict.items():
            first_human = next((m for m in msgs if m['type'] == 'human'), None)
            preview = first_human['content'][:100] + '...' if first_human and len(first_human['content']) > 100 else (first_human['content'] if first_human else 'Sem mensagens')
            
            conversations.append({
                'session_id': session_id,
                'message_count': len(msgs),
                'human_count': sum(1 for m in msgs if m['type'] == 'human'),
                'ai_count': sum(1 for m in msgs if m['type'] == 'ai'),
                'preview': preview,
                'last_message': msgs[-1]['created_at'] if msgs else None
            })
        
        conversations.sort(key=lambda x: x['last_message'] or '', reverse=True)
        return jsonify({'success': True, 'conversations': conversations})
    except Exception as e:
        logger.error(f"Erro em conversas: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/conversa/<session_id>', methods=['GET'])
@login_required
def get_conversa(session_id):
    """Busca mensagens de uma conversa específica (sem limites curtos)."""
    try:
        response = supabase.table("conteudo_puc_conversas") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("id", desc=False) \
            .execute()
        
        messages = []
        for msg in response.data:
            try:
                m_json = json.loads(msg['message']) if isinstance(msg['message'], str) else msg['message']
                msg_type = m_json.get('type', '').lower()
                if msg_type == 'system': continue
                
                content = m_json.get('content', '')
                if msg_type == 'ai' and content.startswith('{'):
                    try:
                        content_json = json.loads(content)
                        content = content_json.get('output', {}).get('mensagem', content_json.get('mensagem', content))
                    except: pass
                
                messages.append({
                    'id': msg['id'],
                    'type': msg_type,
                    'content': content,
                    'created_at': msg.get('created_at', '')
                })
            except: continue
            
        return jsonify({'success': True, 'session_id': session_id, 'messages': messages})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
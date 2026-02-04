import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from supabase import create_client, Client
from functools import wraps
from collections import defaultdict
import logging

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


@app.route('/')
def index():
    """Redireciona para login ou dashboard"""
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == LOGIN_USER and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401
    
    return render_template('chat_login.html')


@app.route('/logout')
def logout():
    """Logout do sistema"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard com estatísticas das conversas"""
    return render_template('chat_dashboard.html', username=session.get('username'))


@app.route('/conversas')
@login_required
def conversas():
    """Página de listagem de conversas"""
    return render_template('chat_conversas.html', username=session.get('username'))


@app.route('/conversa/<session_id>')
@login_required
def conversa_detalhe(session_id):
    """Página de detalhes de uma conversa específica"""
    return render_template('chat_detalhe.html', 
                         session_id=session_id,
                         username=session.get('username'))


@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """Retorna estatísticas das conversas"""
    try:
        # Buscar todas as conversas
        response = supabase.table("conteudo_puc_conversas") \
            .select("*") \
            .execute()
        
        if not response.data:
            return jsonify({
                'success': True,
                'total_messages': 0,
                'total_conversations': 0,
                'human_messages': 0,
                'ai_messages': 0,
                'system_messages': 0
            })
        
        # Processar estatísticas
        messages = response.data
        sessions = set()
        human_count = 0
        ai_count = 0
        system_count = 0
        
        for msg in messages:
            sessions.add(msg['session_id'])
            
            # Parsear mensagem JSON
            try:
                message_data = json.loads(msg['message']) if isinstance(msg['message'], str) else msg['message']
                msg_type = message_data.get('type', '').lower()
                
                if msg_type == 'human':
                    human_count += 1
                elif msg_type == 'ai':
                    ai_count += 1
                elif msg_type == 'system':
                    system_count += 1
            except:
                pass
        
        return jsonify({
            'success': True,
            'total_messages': len(messages),
            'total_conversations': len(sessions),
            'human_messages': human_count,
            'ai_messages': ai_count,
            'system_messages': system_count
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro ao buscar estatísticas'
        }), 500


@app.route('/api/conversas', methods=['GET'])
@login_required
def get_conversas():
    """Retorna lista de conversas agrupadas por session_id"""
    try:
        # Buscar todas as conversas
        response = supabase.table("conteudo_puc_conversas") \
            .select("*") \
            .order("id", desc=False) \
            .execute()
        
        if not response.data:
            return jsonify({
                'success': True,
                'conversations': []
            })
        
        # Agrupar por session_id
        conversations_dict = defaultdict(list)
        
        for msg in response.data:
            try:
                message_data = json.loads(msg['message']) if isinstance(msg['message'], str) else msg['message']
                msg_type = message_data.get('type', '').lower()
                content = message_data.get('content', '')
                
                conversations_dict[msg['session_id']].append({
                    'id': msg['id'],
                    'type': msg_type,
                    'content': content,
                    'created_at': msg.get('created_at', '')
                })
            except Exception as e:
                logger.error(f"Erro ao processar mensagem {msg['id']}: {str(e)}")
                continue
        
        # Criar lista de conversas com resumo
        conversations = []
        for session_id, messages in conversations_dict.items():
            # Pegar primeira mensagem humana como preview
            first_human = next((m for m in messages if m['type'] == 'human'), None)
            preview = first_human['content'][:100] + '...' if first_human and len(first_human['content']) > 100 else (first_human['content'] if first_human else 'Sem mensagens')
            
            # Contar mensagens por tipo
            human_count = sum(1 for m in messages if m['type'] == 'human')
            ai_count = sum(1 for m in messages if m['type'] == 'ai')
            
            conversations.append({
                'session_id': session_id,
                'message_count': len(messages),
                'human_count': human_count,
                'ai_count': ai_count,
                'preview': preview,
                'last_message': messages[-1]['created_at'] if messages else None,
                'first_message': messages[0]['created_at'] if messages else None
            })
        
        # Ordenar por última mensagem (mais recente primeiro)
        conversations.sort(key=lambda x: x['last_message'] or '', reverse=True)
        
        return jsonify({
            'success': True,
            'conversations': conversations
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar conversas: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro ao buscar conversas'
        }), 500


@app.route('/api/conversa/<session_id>', methods=['GET'])
@login_required
def get_conversa(session_id):
    """Retorna todas as mensagens de uma conversa específica"""
    try:
        # Buscar mensagens da conversa
        response = supabase.table("conteudo_puc_conversas") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("id", desc=False) \
            .execute()
        
        if not response.data:
            return jsonify({
                'success': True,
                'messages': [],
                'session_id': session_id
            })
        
        # Processar mensagens
        messages = []
        for msg in response.data:
            try:
                message_data = json.loads(msg['message']) if isinstance(msg['message'], str) else msg['message']
                msg_type = message_data.get('type', '').lower()
                content = message_data.get('content', '')
                
                # Ignorar mensagens do tipo system
                if msg_type == 'system':
                    continue
                
                # Se for mensagem AI, tentar extrair do output/mensagem
                if msg_type == 'ai':
                    try:
                        # Se content é um JSON string, fazer parse
                        if content.startswith('{'):
                            content_json = json.loads(content)
                            # Tentar extrair a mensagem do output
                            if 'output' in content_json and 'mensagem' in content_json['output']:
                                content = content_json['output']['mensagem']
                            elif 'mensagem' in content_json:
                                content = content_json['mensagem']
                    except:
                        # Se der erro, manter o content original
                        pass
                
                messages.append({
                    'id': msg['id'],
                    'type': msg_type,
                    'content': content,
                    'created_at': msg.get('created_at', ''),
                    'additional_kwargs': message_data.get('additional_kwargs', {}),
                    'response_metadata': message_data.get('response_metadata', {})
                })
            except Exception as e:
                logger.error(f"Erro ao processar mensagem {msg['id']}: {str(e)}")
                continue
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'messages': messages,
            'total': len(messages)
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar conversa {session_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro ao buscar conversa'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

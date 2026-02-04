# PUC Chat - Sistema de Visualização de Conversas

Sistema moderno para visualizar e gerenciar conversas armazenadas no Supabase.

## 🎯 Funcionalidades

- ✅ **Dashboard Completo** - Estatísticas em tempo real
- ✅ **Listagem de Conversas** - Visualize todas as conversas
- ✅ **Detalhes da Conversa** - Veja mensagens completas
- ✅ **Interface Moderna** - Design limpo e profissional
- ✅ **Multi-usuário** - Suporta múltiplos administradores
- ✅ **Busca Inteligente** - Encontre conversas rapidamente
- ✅ **Responsivo** - Funciona em desktop e mobile
- ✅ **Tempo Real** - Atualizações automáticas

## 📊 Estrutura do Banco de Dados

### Tabela: `conteudo_puc_conversas`

```sql
CREATE TABLE conteudo_puc_conversas (
  id BIGINT PRIMARY KEY,
  session_id TEXT NOT NULL,
  message JSONB NOT NULL
);
```

### Formato das Mensagens

```json
{
  "type": "human",
  "content": "Boa tarde",
  "additional_kwargs": {},
  "response_metadata": {}
}
```

**Tipos de mensagem:**
- `human` - Mensagens do usuário (exibidas à direita, azul)
- `ai` - Respostas da IA (exibidas à esquerda, verde)
- `system` - Mensagens do sistema (ignoradas na visualização)

## 🚀 Instalação

### 1. Instale as dependências

```bash
cd puc-chat
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar pacotes
pip install -r requirements.txt
```

### 2. Configure o .env

```bash
cp .env.example .env
```

Edite o `.env`:

```env
# Login
LOGIN_USER=admin
LOGIN_PASSWORD=puc2024

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-publica
```

### 3. Adicione a Logo (Opcional)

Coloque sua logo em:
```
puc-chat/static/logo.png
```

Se não adicionar logo, o sistema usará um ícone padrão.

### 4. Execute o sistema

```bash
python app.py
```

Acesse: **http://localhost:5001**

## 📱 Como Usar

### Login
1. Acesse http://localhost:5001
2. Use as credenciais do `.env`
3. Login padrão: `admin` / `puc2024`

### Dashboard
- Veja estatísticas gerais:
  - Total de conversas
  - Total de mensagens
  - Mensagens de usuários
  - Respostas da IA
- Atualização automática a cada 30 segundos

### Conversas
- Lista todas as conversas por session_id
- Busque por ID ou conteúdo
- Veja preview da primeira mensagem
- Click para ver detalhes

### Detalhes da Conversa
- Visualize todas as mensagens
- Mensagens organizadas cronologicamente
- Interface estilo chat
- Diferenciação visual:
  - **Usuário (azul)**: à direita
  - **IA (verde)**: à esquerda

## 🎨 Interface

### Design
- **Fonte Principal**: Inter
- **Fonte Mono**: JetBrains Mono
- **Paleta de Cores**:
  - Primário: Azul #2563EB
  - Secundário: Roxo #8B5CF6
  - Sucesso: Verde #10B981

### Componentes
- **Sidebar** - Navegação fixa
- **Cards** - Informações organizadas
- **Chat Bubbles** - Mensagens estilizadas
- **Animações** - Transições suaves

## 📂 Estrutura do Projeto

```
puc-chat/
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências Python
├── .env.example               # Template de configuração
├── .env                       # Configuração (não committar)
├── README.md                  # Este arquivo
├── static/
│   └── logo.png              # Logo da aplicação (opcional)
└── templates/
    ├── chat_base.html        # Template base
    ├── chat_login.html       # Página de login
    ├── chat_dashboard.html   # Dashboard principal
    ├── chat_conversas.html   # Lista de conversas
    └── chat_detalhe.html     # Detalhes da conversa
```

## 🔧 API Endpoints

### `GET /api/stats`
Retorna estatísticas gerais

**Resposta:**
```json
{
  "success": true,
  "total_messages": 150,
  "total_conversations": 25,
  "human_messages": 75,
  "ai_messages": 70,
  "system_messages": 5
}
```

### `GET /api/conversas`
Lista todas as conversas

**Resposta:**
```json
{
  "success": true,
  "conversations": [
    {
      "session_id": "abc123",
      "message_count": 10,
      "human_count": 5,
      "ai_count": 5,
      "preview": "Boa tarde...",
      "last_message": "2024-02-03T14:30:00Z"
    }
  ]
}
```

### `GET /api/conversa/<session_id>`
Retorna mensagens de uma conversa

**Resposta:**
```json
{
  "success": true,
  "session_id": "abc123",
  "messages": [
    {
      "id": 1,
      "type": "human",
      "content": "Boa tarde",
      "created_at": "2024-02-03T14:30:00Z"
    }
  ],
  "total": 10
}
```

## 🔐 Segurança

### Multi-usuário
- Suporta múltiplos usuários
- Sessões independentes
- Logout seguro

### Credenciais
- Armazenadas em variáveis de ambiente
- Não expostas no código
- Fácil de alterar

### Supabase
- Conexão segura via HTTPS
- API Key protegida
- Row Level Security (configure no Supabase)

## 🎯 Casos de Uso

### Suporte ao Cliente
- Visualize conversas de suporte
- Identifique padrões
- Analise qualidade das respostas

### Análise de Chatbot
- Monitore performance
- Veja taxa de resposta
- Identifique melhorias

### Auditoria
- Histórico completo
- Busca por sessão
- Exportação de dados

## 🔄 Atualização de Dados

O sistema busca dados diretamente do Supabase:
- **Dashboard**: Atualiza a cada 30 segundos
- **Conversas**: Load on demand
- **Mensagens**: Load on demand

Para forçar atualização manual, recarregue a página.

## 📊 Estatísticas

O dashboard mostra:
1. **Total de Conversas** - Número de session_ids únicos
2. **Total de Mensagens** - Todas as mensagens no banco
3. **Mensagens de Usuários** - Tipo "human"
4. **Respostas da IA** - Tipo "ai"

## 🎨 Personalização

### Alterar Logo
1. Substitua `/static/logo.png`
2. Formato recomendado: PNG transparente
3. Tamanho: 80x80px ou maior

### Alterar Cores
Edite `chat_base.html`:
```css
:root {
    --primary: #2563EB;
    --secondary: #8B5CF6;
    --accent: #10B981;
}
```

### Alterar Porta
Em `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🐛 Troubleshooting

### Erro: "No module named 'supabase'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Conversas não aparecem
- Verifique se há dados na tabela `conteudo_puc_conversas`
- Verifique as credenciais do Supabase
- Veja os logs no terminal

### Logo não aparece
- Crie a pasta `static/`
- Adicione o arquivo `logo.png`
- Ou deixe o sistema usar o ícone padrão

## 📝 Notas

- **Porta padrão**: 5001 (diferente do sistema de docs que usa 5000)
- **Mensagens system**: São ignoradas na visualização
- **Ordem**: Mensagens ordenadas por ID (cronológico)
- **Busca**: Case-insensitive, busca em ID e conteúdo

## 🚀 Próximos Passos

1. ✅ Sistema funcionando
2. 🔄 Adicione logo personalizada
3. 🎨 Customize cores se necessário
4. 🔐 Configure RLS no Supabase
5. 📊 Monitore conversas
6. 🌐 Faça deploy em produção

---

**Desenvolvido com Flask, Supabase e boas práticas de UX/UI** 🎓

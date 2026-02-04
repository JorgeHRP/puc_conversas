# 🚀 Guia de Início Rápido - PUC Chat

Configure e execute o sistema em **3 minutos**!

## ⚡ Instalação Rápida

### 1. Instale as dependências (1 min)

```bash
cd puc-chat
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# Instalar
pip install -r requirements.txt
```

### 2. Configure o .env (30 segundos)

```bash
cp .env.example .env
nano .env  # ou use seu editor favorito
```

**Preencha apenas 2 coisas:**

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

### 3. Execute! (10 segundos)

```bash
python app.py
```

Acesse: **http://localhost:5001**

Login: `admin` / `puc2024`

---

## 🎯 Verificação Rápida

### ✅ Funcionou se você vê:

1. Página de login com design roxo
2. Dashboard com 4 cards de estatísticas
3. Aba "Conversas" com lista de conversas
4. Consegue clicar em uma conversa e ver as mensagens

### ❌ Não funcionou?

**Erro: "Invalid API key"**
- Verifique se copiou a chave correta do Supabase
- Use a chave **anon public**, não a service_role

**Erro: "No module named 'flask'"**
- Ative o ambiente virtual: `source venv/bin/activate`

**Sem conversas aparecendo**
- Verifique se há dados na tabela `conteudo_puc_conversas`

---

## 📊 Estrutura da Tabela (Se ainda não criou)

Execute no Supabase SQL Editor:

```sql
CREATE TABLE conteudo_puc_conversas (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  session_id TEXT NOT NULL,
  message JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para melhor performance
CREATE INDEX idx_session_id ON conteudo_puc_conversas(session_id);
```

---

## 🎨 Adicionar Logo (Opcional)

```bash
# Coloque sua logo aqui:
puc-chat/static/logo.png

# Formato: PNG com transparência
# Tamanho: 200x200px (recomendado)
```

Veja instruções completas em: `static/LOGO_INSTRUCTIONS.md`

---

## 📱 Navegação do Sistema

### 1. Dashboard (`/dashboard`)
- Total de conversas
- Total de mensagens  
- Mensagens de usuários
- Respostas da IA

### 2. Conversas (`/conversas`)
- Lista todas as conversas
- Busca por session_id ou conteúdo
- Preview da primeira mensagem
- Click para ver detalhes

### 3. Detalhes (`/conversa/<session_id>`)
- Todas as mensagens da conversa
- Interface estilo chat
- Usuário à direita (azul)
- IA à esquerda (verde)

---

## 🔧 Personalização Rápida

### Mudar Porta

Em `app.py`, última linha:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude aqui
```

### Mudar Credenciais de Login

No `.env`:
```env
LOGIN_USER=seu_usuario
LOGIN_PASSWORD=sua_senha
```

### Mudar Cores

Em `templates/chat_base.html`:
```css
:root {
    --primary: #2563EB;     /* Cor principal */
    --secondary: #8B5CF6;   /* Cor secundária */
    --accent: #10B981;      /* Cor de destaque */
}
```

---

## 🧪 Testar com Dados de Exemplo

### Inserir Conversa de Teste

No Supabase SQL Editor:

```sql
-- Inserir mensagem do usuário
INSERT INTO conteudo_puc_conversas (session_id, message)
VALUES ('teste-123', '{
  "type": "human",
  "content": "Olá, como você está?",
  "additional_kwargs": {},
  "response_metadata": {}
}'::jsonb);

-- Inserir resposta da IA
INSERT INTO conteudo_puc_conversas (session_id, message)
VALUES ('teste-123', '{
  "type": "ai",
  "content": "Olá! Estou bem, obrigado por perguntar. Como posso ajudá-lo hoje?",
  "additional_kwargs": {},
  "response_metadata": {}
}'::jsonb);

-- Inserir mais uma mensagem do usuário
INSERT INTO conteudo_puc_conversas (session_id, message)
VALUES ('teste-123', '{
  "type": "human",
  "content": "Preciso de informações sobre matrícula",
  "additional_kwargs": {},
  "response_metadata": {}
}'::jsonb);

-- Inserir resposta da IA
INSERT INTO conteudo_puc_conversas (session_id, message)
VALUES ('teste-123', '{
  "type": "ai",
  "content": "Claro! As matrículas para o próximo semestre começam dia 15. Você precisa ter os seguintes documentos: histórico escolar, comprovante de residência e documento de identidade.",
  "additional_kwargs": {},
  "response_metadata": {}
}'::jsonb);
```

Agora recarregue o dashboard e veja as estatísticas atualizarem! 🎉

---

## 📊 Formato das Mensagens

### Mensagem do Usuário (Human)
```json
{
  "type": "human",
  "content": "Sua mensagem aqui",
  "additional_kwargs": {},
  "response_metadata": {}
}
```

### Resposta da IA
```json
{
  "type": "ai",
  "content": "Resposta da IA aqui",
  "additional_kwargs": {},
  "response_metadata": {}
}
```

### Mensagem do Sistema (Ignorada)
```json
{
  "type": "system",
  "content": "Mensagem de sistema",
  "additional_kwargs": {},
  "response_metadata": {}
}
```

**Nota**: Mensagens do tipo `system` não aparecem na interface!

---

## 🎯 Checklist Final

- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Arquivo .env configurado
- [ ] Tabela criada no Supabase
- [ ] Servidor rodando (`python app.py`)
- [ ] Login funcionando
- [ ] Dashboard mostrando estatísticas
- [ ] Conversas aparecendo na lista
- [ ] Mensagens visíveis ao clicar na conversa

**Tudo certo? Parabéns! 🎊**

---

## 🆘 Ajuda Rápida

**Dúvidas?** Veja o README.md completo para:
- API endpoints detalhados
- Estrutura completa do projeto
- Troubleshooting avançado
- Casos de uso

**Logo?** Veja `static/LOGO_INSTRUCTIONS.md` para:
- Como adicionar sua logo
- Especificações de tamanho
- Dicas de design

---

## 🚀 Próximos Passos

1. ✅ Sistema funcionando
2. 🎨 Adicione sua logo
3. 📊 Monitore conversas reais
4. 🔐 Configure RLS no Supabase (produção)
5. 🌐 Faça deploy (Heroku, Railway, etc.)

---

**Tempo total de setup: ~3 minutos** ⚡

**Aproveite seu novo sistema de visualização de conversas!** 🎓

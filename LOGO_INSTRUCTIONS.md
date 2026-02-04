# 🖼️ Como Adicionar sua Logo

Para personalizar o sistema com a logo da PUC, siga estas instruções:

## 📁 Localização

Adicione sua logo neste caminho:
```
puc-chat/static/logo.png
```

## 📐 Especificações Recomendadas

### Formato
- **Extensão**: `.png` (com transparência)
- **Alternativa**: `.svg` para qualidade escalável

### Tamanho
- **Recomendado**: 200x200px ou maior
- **Mínimo**: 80x80px
- **Proporção**: Quadrada (1:1) ou próxima disso

### Qualidade
- **Fundo**: Transparente (PNG)
- **Resolução**: Alta (300 DPI ideal)
- **Cores**: RGB

## 🎯 Locais onde a Logo Aparece

A logo será exibida em:

1. **Página de Login**
   - Tamanho: 80x80px
   - Localização: Centro superior
   - Fundo: Card branco

2. **Sidebar (Dashboard e Conversas)**
   - Tamanho: 40x40px
   - Localização: Topo da sidebar
   - Fundo: Escuro (#1E293B)

## 📝 Passo a Passo

### Opção 1: Arquivo PNG
```bash
# 1. Coloque sua logo na pasta static
cp /caminho/para/sua/logo.png puc-chat/static/logo.png

# 2. Reinicie o servidor Flask
# Ctrl+C para parar
python app.py
```

### Opção 2: Usar SVG
Se preferir SVG, altere nos templates:

**chat_login.html** (linha ~33):
```html
<img src="/static/logo.svg" alt="PUC Logo" ...>
```

**chat_dashboard.html** (linha ~20):
```html
<img src="/static/logo.svg" alt="PUC Logo" ...>
```

## 🎨 Dicas de Design

### Para Fundo Escuro (Sidebar)
- Use logo em cores claras
- Ou logo branca com detalhes
- Adicione padding se necessário

### Para Fundo Claro (Login)
- Qualquer cor funciona
- Considere adicionar sombra sutil

## 🔧 Ajustes de Tamanho

Se sua logo precisar de tamanhos diferentes, edite o CSS:

**Para a sidebar** (chat_dashboard.html):
```css
.logo-image {
    width: 40px;    /* Ajuste aqui */
    height: 40px;   /* Ajuste aqui */
    object-fit: contain;
}
```

**Para o login** (chat_login.html):
```css
.login-logo img {
    width: 100%;    /* Mantém responsivo */
    height: 100%;
    object-fit: contain;
}
```

## ⚠️ Fallback Automático

Se a logo não for encontrada, o sistema mostra automaticamente:
- **Ícone de chat**: 💬
- **Texto "PUC Chat"**

Não há quebra no layout!

## ✅ Verificação

Após adicionar a logo:

1. ✔️ Verifique se o arquivo existe em `/static/logo.png`
2. ✔️ Acesse a página de login
3. ✔️ A logo deve aparecer no centro
4. ✔️ Faça login e veja a logo na sidebar

## 🎭 Exemplos de Logo

### Logo Colorida
```
puc-chat/static/logo.png
- Fundo transparente
- Logo colorida da PUC
- 200x200px
```

### Logo Monocromática
```
puc-chat/static/logo.png
- Fundo transparente
- Logo branca/preta
- Funciona em qualquer fundo
```

## 🔄 Se Mudar a Logo

1. Substitua o arquivo `logo.png`
2. **Force refresh** no navegador:
   - Windows/Linux: `Ctrl + F5`
   - Mac: `Cmd + Shift + R`
3. Ou limpe o cache do navegador

## 📱 Logo Responsiva

O sistema já está preparado:
- **Desktop**: 40px na sidebar
- **Mobile**: Adapta automaticamente
- **Login**: 80px em todas as telas

## 🎨 Variações por Tema

Se quiser logos diferentes para claro/escuro:

```html
<!-- Logo para tema claro -->
<img src="/static/logo-light.png" class="logo-light">

<!-- Logo para tema escuro -->
<img src="/static/logo-dark.png" class="logo-dark">
```

E adicione CSS para trocar conforme o tema.

## 📞 Ajuda

Problemas com a logo?

1. Verifique o caminho: `/static/logo.png`
2. Veja permissões do arquivo
3. Teste com uma logo simples primeiro
4. Verifique o console do navegador (F12)

---

**Nota**: O sistema funciona perfeitamente sem logo personalizada! O ícone padrão é moderno e profissional.

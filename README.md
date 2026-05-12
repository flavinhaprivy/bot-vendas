# 🤖 Bot de Vendas — Tutorial Completo

## Arquivos do projeto

```
bot_vendas/
├── bot.py           ← código do bot
├── requirements.txt ← bibliotecas necessárias
├── Procfile         ← instrução pro Railway rodar o bot
└── README.md        ← este tutorial
```

---

## PARTE 1 — Configurar o bot antes de subir

Abra o arquivo `bot.py` e preencha as variáveis no topo:

| Variável      | O que colocar                          | Exemplo                  |
|---------------|----------------------------------------|--------------------------|
| `PIX_KEY`     | Sua chave PIX                          | `12345678900`            |
| `PIX_VALUE`   | Valor cobrado                          | `R$ 29,90`               |
| `LINK_ENTREGA`| Link que o cliente recebe após pagar   | `https://t.me/+XXXXXXX`  |
| `AUDIO_1/2/3` | file_id do áudio (veja abaixo)         | `AgACAgIAAxk...`         |
| `VIDEO_1/2`   | file_id do vídeo (veja abaixo)         | `BAACAgIAAxk...`         |
| `IMAGE_1`     | file_id da imagem (veja abaixo)        | `AgACAgIAAxk...`         |

### Como obter o file_id de um arquivo

1. Adicione o bot **@RawDataBot** no Telegram
2. Encaminhe seu áudio / vídeo / foto para ele
3. Ele vai te responder com um JSON — copie o valor de `file_id`
4. Cole no `bot.py` no campo correspondente

---

## PARTE 2 — Criar conta no GitHub (gratuito)

O Railway precisa que o código esteja no GitHub.

1. Acesse **https://github.com** e clique em **Sign up**
2. Crie sua conta (e-mail + senha)
3. Confirme o e-mail
4. Clique em **New repository** (botão verde no canto superior direito)
5. Dê um nome: `bot-vendas`
6. Marque **Private** (privado)
7. Clique em **Create repository**

---

## PARTE 3 — Subir os arquivos para o GitHub

### Opção A — Pelo site (mais fácil, sem instalar nada)

1. Dentro do repositório criado, clique em **uploading an existing file**
2. Arraste os 4 arquivos: `bot.py`, `requirements.txt`, `Procfile`, `README.md`
3. Clique em **Commit changes**

### Opção B — Pelo terminal (se quiser)

```bash
git clone https://github.com/SEU_USUARIO/bot-vendas
cd bot-vendas
# copie os arquivos para esta pasta
git add .
git commit -m "primeiro commit"
git push
```

---

## PARTE 4 — Criar conta no Railway e hospedar (gratuito)

1. Acesse **https://railway.app**
2. Clique em **Start a New Project**
3. Faça login com o **GitHub** (clique em "Login with GitHub")
4. Autorize o Railway a acessar sua conta
5. Clique em **New Project → Deploy from GitHub repo**
6. Selecione o repositório `bot-vendas`
7. O Railway vai detectar o `Procfile` automaticamente ✅

---

## PARTE 5 — Configurar as variáveis de ambiente no Railway

Em vez de deixar dados sensíveis no código, você pode configurar
as variáveis direto no Railway (mais seguro):

1. No painel do projeto, clique na sua aplicação
2. Vá na aba **Variables**
3. Adicione cada variável clicando em **New Variable**:

```
TOKEN        = 8790169082:AAEqhlwMh5X-6pPGzjp6SgE9rHe5IO5nHvY
PIX_KEY      = seu_pix_aqui
PIX_VALUE    = R$ 29,90
LINK_ENTREGA = https://seu_link_aqui
AUDIO_1      = file_id_do_audio_1
AUDIO_2      = file_id_do_audio_2
AUDIO_3      = file_id_do_audio_3
VIDEO_1      = file_id_do_video_1
VIDEO_2      = file_id_do_video_2
IMAGE_1      = file_id_da_imagem_1
```

4. Clique em **Deploy** (ou o Railway faz automaticamente)

---

## PARTE 6 — Verificar se o bot está rodando

1. Na aba **Deployments** do Railway, veja se aparece ✅ **Active**
2. Abra o Telegram, procure seu bot e mande `/start`
3. Se responder, está funcionando! 🎉

---

## Plano gratuito do Railway

- **Hobby (grátis):** 5 dólares de crédito por mês — suficiente para
  um bot leve rodar o mês inteiro sem custo
- Sem precisar de cartão de crédito para começar

---

## Problemas comuns

| Problema                        | Solução                                              |
|---------------------------------|------------------------------------------------------|
| Bot não responde                | Verifique se o TOKEN está correto nas variáveis      |
| Erro de áudio/vídeo             | O file_id está errado — reenvie para @RawDataBot     |
| Deploy falhou                   | Clique em **View Logs** no Railway e me manda o erro |
| Bot para depois de um tempo     | Normal no plano free — reinicie o deploy manualmente |

---

## Suporte

Se travar em algum passo, me chama que te ajudo! 💛

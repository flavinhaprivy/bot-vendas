#!/usr/bin/env python3
"""
Bot de Vendas - Telegram
Hospedado no Railway (gratuito)
"""

import asyncio
import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ──────────────────────────────────────────────────────────
#  CONFIGURAÇÕES  ←  edite só aqui antes de subir
# ──────────────────────────────────────────────────────────
TOKEN        = os.getenv("TOKEN",        "8790169082:AAEqhlwMh5X-6pPGzjp6SgE9rHe5IO5nHvY")
PIX_KEY      = os.getenv("PIX_KEY",      "SEU_PIX_AQUI")       # CPF, e-mail, celular ou chave aleatória
PIX_VALUE    = os.getenv("PIX_VALUE",    "R$ 00,00")            # ex: R$ 29,90
LINK_ENTREGA = os.getenv("LINK_ENTREGA", "https://SEU_LINK_AQUI")

# file_id  →  como obter: veja o README.md
AUDIO_1  = os.getenv("AUDIO_1",  "AUDIO_1_FILE_ID")
AUDIO_2  = os.getenv("AUDIO_2",  "AUDIO_2_FILE_ID")
AUDIO_3  = os.getenv("AUDIO_3",  "AUDIO_3_FILE_ID")
VIDEO_1  = os.getenv("VIDEO_1",  "VIDEO_1_FILE_ID")
VIDEO_2  = os.getenv("VIDEO_2",  "VIDEO_2_FILE_ID")
IMAGE_1  = os.getenv("IMAGE_1",  "IMAGE_1_FILE_ID")
# ──────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Estado de cada usuário  { telegram_user_id: passo_atual }
user_state: dict[int, int] = {}


# ── helpers ────────────────────────────────────────────────
async def typing(chat_id, ctx, secs=1.2):
    await ctx.bot.send_chat_action(chat_id=chat_id, action="typing")
    await asyncio.sleep(secs)

async def voice_action(chat_id, ctx, secs=1.5):
    await ctx.bot.send_chat_action(chat_id=chat_id, action="upload_voice")
    await asyncio.sleep(secs)

async def video_action(chat_id, ctx, secs=2.0):
    await ctx.bot.send_chat_action(chat_id=chat_id, action="upload_video")
    await asyncio.sleep(secs)

async def msg(update, ctx, text, delay=0, parse_mode=None):
    if delay:
        await asyncio.sleep(delay)
    await typing(update.effective_chat.id, ctx)
    await update.message.reply_text(text, parse_mode=parse_mode)


# ── /start ─────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = 1
    await msg(update, ctx,
        "Oi! 😊 Seja muito bem-vindo(a)!\n\n"
        "Você veio no lugar certo. Tenho algo MUITO especial pra te mostrar... 👀\n\n"
        "Qual é o seu nome?"
    )


# ── handler principal ──────────────────────────────────────
async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    chat = update.effective_chat.id
    text = (update.message.text or "").strip()
    step = user_state.get(uid, 0)

    # ---------- PASSO 1 — recebe o nome ----------
    if step == 1:
        user_state[uid] = 2
        nome = text.split()[0].capitalize() if text else update.effective_user.first_name
        await msg(update, ctx,
            f"Que nome lindo, {nome}! 🥰\n\n"
            "Deixa eu te contar uma coisa… o que eu vou te mostrar hoje mudou a vida de muita gente.\n\n"
            "Você topa ver? Responde SIM ou NÃO 👇"
        )

    # ---------- PASSO 2 — interesse ----------
    elif step == 2:
        user_state[uid] = 3
        await msg(update, ctx,
            "Amei! 🔥 Então presta atenção…\n\n"
            "Vou te mandar um conteúdo EXCLUSIVO agora. É só pra quem chegou aqui.\n\n"
            "Aguarda um segundo... ⏳"
        )
        await asyncio.sleep(3)
        await msg(update, ctx,
            "Pronto, tô aqui! 😏\n\n"
            "Antes de te mostrar tudo, me diz: você já conhece esse tipo de conteúdo?\n\n"
            "1️⃣ Sim, já conheço\n"
            "2️⃣ Não, é novidade pra mim"
        )

    # ---------- PASSO 3 — conhece? ----------
    elif step == 3:
        user_state[uid] = 4
        await msg(update, ctx,
            "Perfeito! Então vou começar do início mesmo 😄\n\n"
            "Manda um \"ok\" que já te envio o primeiro conteúdo especial 🎧"
        )

    # ---------- PASSO 4 — ÁUDIO 1 ----------
    elif step == 4:
        user_state[uid] = 5
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_1)
        await msg(update, ctx,
            "Curtiu? 🔥\n\n"
            "Tenho MUITO mais por aqui… isso foi só o aperitivo!\n\n"
            "Quer ver o próximo? 👇",
            delay=2
        )

    # ---------- PASSO 5 — VÍDEO 1 ----------
    elif step == 5:
        user_state[uid] = 6
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_1)
        await msg(update, ctx,
            "🤤 Deu gosto de ver né?\n\n"
            "Isso é só uma AMOSTRA do pacote completo.\n\n"
            "Responde qualquer coisa pra eu te contar mais 👇",
            delay=2
        )

    # ---------- PASSO 6 — apresenta pacote + localização ----------
    elif step == 6:
        user_state[uid] = 7
        await msg(update, ctx,
            "Olha o que tem no pacote completo:\n\n"
            "✅ Conteúdo exclusivo\n"
            "✅ Acesso imediato\n"
            "✅ Sem mensalidade\n"
            "✅ Suporte direto comigo\n\n"
            f"Tudo isso por apenas *{PIX_VALUE}*! 🎉",
            parse_mode="Markdown"
        )
        await msg(update, ctx, "📍 Localização detectada: Brasil 🇧🇷", delay=2)
        await msg(update, ctx,
            "Você está online agora… isso é bom sinal! 😏\n\n"
            "Quem compra NUNCA se arrepende.\n\n"
            "Vou te mandar mais uma coisa antes do pagamento… aguarda! 🎧",
            delay=2
        )

    # ---------- PASSO 7 — ÁUDIO 2 ----------
    elif step == 7:
        user_state[uid] = 8
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_2)
        await msg(update, ctx,
            "Tá vendo? É EXATAMENTE isso que você leva no pacote! 🔥\n\n"
            "Bora? Me manda um \"quero\" 👇",
            delay=2
        )

    # ---------- PASSO 8 — ÁUDIO 3 + VÍDEO 2 ----------
    elif step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_3)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        # Espera 8 segundos e continua
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await update.message.reply_text(
            "Ainda aqui? 😍 Porque EU tô!\n\n"
            "Tudo que você viu está no pacote.\n\n"
            "Me fala: gostou? 👇"
        )

    # ---------- PASSO 9 — ÁUDIO 3 (bis) ----------
    elif step == 9:
        user_state[uid] = 10
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_1)
        await msg(update, ctx,
            "Tá chegando no melhor… 🤭\n\n"
            "Vou te mandar o último vídeo antes do pagamento.\n\n"
            "Prepara o coração! 💥 Responde \"to pronto\" 👇",
            delay=2
        )

    # ---------- PASSO 10 — VÍDEO final ----------
    elif step == 10:
        user_state[uid] = 11
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await msg(update, ctx,
            "PRONTO! É ISSO! 🔥🔥🔥\n\n"
            "Agora você já sabe o que vai levar…\n\n"
            "Vem fechar! 👇",
            delay=2
        )
        await msg(update, ctx,
            "Só mais uma coisinha antes do pagamento…\n\n"
            "Tenho uma imagem especial pra te mostrar 📸",
            delay=2
        )

    # ---------- PASSO 11 — IMAGEM + urgência (2 min) ----------
    elif step == 11:
        user_state[uid] = 12
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_1)
        # 2 minutos de delay — cria senso de urgência
        await asyncio.sleep(120)
        await typing(chat, ctx)
        await update.message.reply_text("Ainda pensando? 🤔\n\nOlha, esse preço é por TEMPO LIMITADO…")
        await msg(update, ctx,
            "Quando eu fechar as vagas, acabou. Simples assim.\n\n"
            "Não quero que você perca essa oportunidade! 💛",
            delay=2
        )
        await msg(update, ctx,
            "Então me responde: ainda tá afim de fechar? 👇\n\n"
            "1️⃣ Sim, quero fechar agora!\n"
            "2️⃣ Tenho uma dúvida",
            delay=2
        )

    # ---------- PASSO 12 — dúvida ou confirmação ----------
    elif step == 12:
        if "2" in text or "dúvida" in text.lower() or "duvida" in text.lower():
            # fica no passo 12 para responder a dúvida
            await msg(update, ctx, "Claro! Me faz a pergunta que te respondo agora mesmo 😊")
        else:
            user_state[uid] = 13
            await msg(update, ctx,
                f"Ótimo! 🎉 Que decisão incrível!\n\n"
                f"Me confirma: você quer garantir o pacote por *{PIX_VALUE}*?",
                parse_mode="Markdown"
            )

    # ---------- PASSO 13 — envia PIX ----------
    elif step == 13:
        user_state[uid] = 14
        await msg(update, ctx, "SHOW! Preparando seu pagamento… 💳")
        await msg(update, ctx,
            f"📲 *PAGAMENTO VIA PIX*\n\n"
            f"🔑 Chave: `{PIX_KEY}`\n"
            f"💰 Valor: *{PIX_VALUE}*\n\n"
            "Faça o pagamento e me manda o *comprovante* aqui!\n\n"
            "Assim que confirmar, te mando o acesso na hora! ⚡",
            delay=2,
            parse_mode="Markdown"
        )

    # ---------- PASSO 14 — comprovante → libera acesso ----------
    elif step == 14:
        user_state[uid] = 99
        await msg(update, ctx, "Recebi! ✅ Confirmando o pagamento…\n\nUm segundo! ⏳")
        await msg(update, ctx,
            f"✅ *PAGAMENTO CONFIRMADO!* 🎉\n\n"
            f"Aqui está o seu acesso:\n👉 {LINK_ENTREGA}\n\n"
            "Seja muito bem-vindo(a)! 🥳\n"
            "Qualquer dúvida, é só falar aqui 💬",
            delay=2,
            parse_mode="Markdown"
        )

    # ---------- FIM ----------
    elif step == 99:
        await msg(update, ctx, "Já te enviei tudo! 😊 Qualquer dúvida é só chamar aqui. 💛")

    # ---------- Sem /start ----------
    else:
        await msg(update, ctx, "Oi! Digite /start para começar. 😊")


# ── main ───────────────────────────────────────────────────
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle))
    logger.info("✅ Bot rodando!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

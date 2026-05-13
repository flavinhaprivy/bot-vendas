#!/usr/bin/env python3
"""
Bot de Vendas - Telegram
Hospedado no Railway — Python 3.11 + PTB 21.9
"""

import asyncio
import logging
import os
import aiohttp

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ══════════════════════════════════════════════════════════
#   CONFIGURAÇÕES  ←  preencha aqui ou nas variáveis do Railway
# ══════════════════════════════════════════════════════════
TOKEN        = os.getenv("TOKEN",        "8790169082:AAEqhlwMh5X-6pPGzjp6SgE9rHe5IO5nHvY")
PIX_KEY      = os.getenv("PIX_KEY",      "SEU_PIX_AQUI")
PIX_VALUE    = os.getenv("PIX_VALUE",    "R$ 00,00")
LINK_ENTREGA = os.getenv("LINK_ENTREGA", "hhttps://t.me/Flavinahbot")
LINK_ENTREGA = "https://t.me/Flavinahbot"

# ── File IDs das mídias ───────────────────────────────────
# Use o comando /capturar_id para descobrir o file_id de cada mídia
# Envie a mídia pro bot após ativar o modo de captura com /capturar_id
# Cole os IDs nas variáveis do Railway ou diretamente aqui
AUDIO_1 = os.getenv("AUDIO_1", "AUDIO_1_FILE_ID")
AUDIO_1 = "AwACAgEAAxkBAAPDagO9XdZYKv9_M-_F4GAF1B_d8-0AAnwGAALagiFEYK8SjDXgbrA7BA"
AUDIO_2 = os.getenv("AUDIO_2", "AUDIO_2_FILE_ID")
AUDIO_2 = "AwACAgEAAxkBAAOragO8ntVXUe33j6mcwSds5sNAJa0AAnYGAALagiFE5m4QqBjT_CM7BA"
AUDIO_3 = os.getenv("AUDIO_3", "AUDIO_3_FILE_ID")
AUDIO_3 = "AwACAgEAAxkBAAOvagO8x6finonjz_t2PfcAAUJhNSnzAAJ3BgAC2oIhREoIjn8DBrjHOwQ"
AUDIO_4 = os.getenv("AUDIO_4", "AUDIO_4_FILE_ID")
AUDIO_4 = "AwACAgEAAxkBAAOzagO9AAHZX3sS7qgWbcSgPa1o5oXfAAJ4BgAC2oIhRLJ2D1IYZcxJOwQ"
AUDIO_5 = os.getenv("AUDIO_5", "AUDIO_5_FILE_ID")
AUDIO_5 = "AwACAgEAAxkBAAO3agO9HTm_G1cYWnaFeeItGMzl2zYAAnkGAALagiFEMFFUnOSN1U47BA"
AUDIO_6 = os.getenv("AUDIO_6", "AUDIO_6_FILE_ID")
AUDIO_6 = "AwACAgEAAxkBAAO7agO9LMvBA1vnaqYHfDaY--FV4vkAAnoGAALagiFEjkK2u3C9naM7BA"
AUDIO_7 = os.getenv("AUDIO_7", "AUDIO_7_FILE_ID")
AUDIO_7 = "AwACAgEAAxkBAAO_agO9Q8fvZq_k75yeCY7T63XxUx0AAnsGAALagiFE47AunJzKGzM7BA"
VIDEO_1 = os.getenv("VIDEO_1", "VIDEO_1_FILE_ID")
VIDEO_1 = "BAACAgEAAxkBAAOSagO6XlYtWkoROh6j9VlpvOOnAYgAAnAGAALagiFEF7_3Rf_BhSI7BA"
VIDEO_2 = os.getenv("VIDEO_2", "VIDEO_2_FILE_ID")
VIDEO_2 = "BAACAgEAAxkBAAOUagO6fle6NhGsATRoEUx288EzWF4AAnEGAALagiFEl6p5skCkVhE7BA"
VIDEO_3 = os.getenv("VIDEO_3", "VIDEO_3_FILE_ID")
VIDEO_3 = "BAACAgEAAxkBAAObagO6sAr3cWOJ21TnfJtOjAVPMegAAnIGAALagiFE9jVtXuW8HUU7BA"
VIDEO_4 = os.getenv("VIDEO_4", "VIDEO_4_FILE_ID")
VIDEO_4 = "BAACAgEAAxkBAAOfagO6vvPkUZYi-ELbVnuE07A_zjIAAnMGAALagiFE-eIlilAmEC47BA"
VIDEO_5 = os.getenv("VIDEO_5", "VIDEO_5_FILE_ID")
VIDEO_5 = "BAACAgEAAxkBAAOjagO6yVwW63smYxewBQg-nZSh9N4AAnQGAALagiFE0xZbqlnRpA87BA"
IMAGE_1 = "AgACCagEAAxkBAANcagOiTrmhMjEPiiWMLWWrAAGqaU2gAAIMDGsbI1oRRNwOpLHrWtClAQADAgADdwADOwQ"
IMAGE_2 = os.getenv("IMAGE_2", "IMAGE_2_FILE_ID")
IMAGE_2 = "AgACAgEAAxkBAAPHagO9vMPmxnJHayQerq_GdJGAVJoAAhIMaxvagiFEDAqpCxdRkJABAAMCAAN3AAM7BA"
# ── Adicione mais mídias aqui se precisar ─────────────────
# AUDIO_4 = os.getenv("AUDIO_4", "AUDIO_4_FILE_ID")
# VIDEO_3 = os.getenv("VIDEO_3", "VIDEO_3_FILE_ID")
# IMAGE_2 = os.getenv("IMAGE_2", "IMAGE_2_FILE_ID")
# ══════════════════════════════════════════════════════════

# ── Modo de captura de File IDs ───────────────────────────
# Mude para True temporariamente para capturar os file_ids das mídias
# Depois volte para False antes de subir para produção
MODO_CAPTURA = os.getenv("MODO_CAPTURA", "false").lower() == "true"



async def capturar_id(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Ativa o modo de captura de file_id para o usuário."""
    ctx.user_data["capturando"] = True
    await update.message.reply_text(
        "📎 Modo de captura ativado!\n\n"
        "Agora envie uma foto, áudio ou vídeo direto no chat.\n"
        "Vou te devolver o file_id dela. 📋"
    )

async def capturar_midia(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Recebe a mídia e retorna o file_id."""
    logger.info(
        "capturar_midia chamado | capturando=%s | user_id=%s | chat_id=%s",
        ctx.user_data.get("capturando"),
        update.effective_user.id if update.effective_user else None,
        update.effective_chat.id if update.effective_chat else None,
    )

    if not ctx.user_data.get("capturando"):
        return  # Não está em modo de captura, ignora

    msg = update.message
    file_id = None
    tipo = None

    if msg.photo:
        file_id = msg.photo[-1].file_id
        tipo = "🖼 IMAGE"
    elif msg.voice:
        file_id = msg.voice.file_id
        tipo = "🎙 VOICE"
    elif msg.audio:
        file_id = msg.audio.file_id
        tipo = "🎵 AUDIO"
    elif msg.video:
        file_id = msg.video.file_id
        tipo = "🎬 VIDEO"
    elif msg.video_note:
        file_id = msg.video_note.file_id
        tipo = "📹 VIDEO_NOTE"
    elif msg.document:
        file_id = msg.document.file_id
        if msg.document.mime_type and msg.document.mime_type.startswith("image/"):
            tipo = "🖼 IMAGE"
        else:
            tipo = "📄 DOCUMENT"

    if file_id:
        logger.info(f"FILE_ID CAPTURADO | {tipo} | {file_id}")
        await update.message.reply_text(
            f"{tipo} — File ID capturado! ✅\n\n"
            f"`{file_id}`\n\n"
            "Cole esse valor na variável correspondente no Railway. 🚀",
            parse_mode="Markdown"
        )
        ctx.user_data["capturando"] = False
    else:
        await update.message.reply_text(
            "⚠️ Não detectei uma mídia válida.\n"
            "Envie uma foto, áudio ou vídeo direto no chat.\n"
            "Se você enviou texto, tente novamente com a mídia correta."
        )


# ══════════════════════════════════════════════════════════
#   HELPERS DE AÇÃO
# ══════════════════════════════════════════════════════════

async def typing(chat_id: int, ctx: ContextTypes.DEFAULT_TYPE, secs: float = 1.2):
    await ctx.bot.send_chat_action(chat_id=chat_id, action="typing")
    await asyncio.sleep(secs)

async def voice_action(chat_id: int, ctx: ContextTypes.DEFAULT_TYPE, secs: float = 1.5):
    await ctx.bot.send_chat_action(chat_id=chat_id, action="upload_voice")
    await asyncio.sleep(secs)

async def video_action(chat_id: int, ctx: ContextTypes.DEFAULT_TYPE, secs: float = 2.0):
    await ctx.bot.send_chat_action(chat_id=chat_id, action="upload_video")
    await asyncio.sleep(secs)

async def msg(
    update: Update,
    ctx: ContextTypes.DEFAULT_TYPE,
    text: str,
    delay: float = 0,
    parse_mode: str | None = None,
):
    if delay:
        await asyncio.sleep(delay)
    await typing(update.effective_chat.id, ctx)
    await update.message.reply_text(text, parse_mode=parse_mode)


# ══════════════════════════════════════════════════════════
#   /start
# ══════════════════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = 1
    await msg(
        update, ctx,
        "Oieee 👀 \n\n"
        "Qual é o seu nome?"
    )


# ══════════════════════════════════════════════════════════
#   HANDLER PRINCIPAL — FLUXO DE VENDAS
# ══════════════════════════════════════════════════════════

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    chat = update.effective_chat.id
    text = (update.message.text or "").strip()
    step = user_state.get(uid, 0)

    # ── Verifica modo de captura antes de entrar no fluxo ─
    if ctx.user_data.get("capturando"):
        await capturar_midia(update, ctx)
        return

    # ── 1 · recebe o nome ─────────────────────────────────
    if step == 1:
        user_state[uid] = 2
        nome = text.split()[0].capitalize() if text else (update.effective_user.first_name or "você")
        await msg(update, ctx,
            f"Que nome lindo, {nome}! 🥰\n\n"
             "Tudo bem com você?"
        )

    # ── 2 · interesse ─────────────────────────────────────
    elif step == 2:
        user_state[uid] = 3
        await msg(update, ctx,
            "Entendii amor, eu estou bem :)\n\n"
            "Pera aí que já converso contigo, mo é que tô no banho agora"
        )
        await asyncio.sleep(3)
        await msg(update, ctx,
            "você consegue escutar áudio? ta meio dificil escrever kkk  😏\n\n"
            
        )
    # ── 3 · ÁUDIO 1 ───────────────────────────────────────
    elif step == 3:
        user_state[uid] = 4
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_1)
        await msg(update, ctx,
            "Se você quiser eu te mando amor 🔥 \n\n"
            "kkk mas você promete que isso fica só entre a gente?",
            delay=2
        )
        
    # ── 4 · VÍDEO 1 ───────────────────────────────────────
    elif step == 4:
        user_state[uid] = 5
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_1)
        await msg(update, ctx,
            "Fiquei até com vergonha agora kkk \n\n",
            delay=2
        )
    # ── 5 · conhece? ──────────────────────────────────────
    elif step == 5:
        user_state[uid] = 6
        await msg(update, ctx,
            "ah, nem me apresentei direito, meu nome é Miya e fiz 21 aninhos esses dias 😄 \n\n"
             "Comecei a morar sozinha aqui ( ip usuário) e faço faculdade online de jornalismo, como não tenho muito tempo pra sair de casa por conta das aulas comecei a vender meus videos e fotos aqui no telegram \n\n"
              "Comecei a fazer Conteúdo 18+  escondida, me promete que isso fica só entre a gente? \n\n"
        )

    # ── 6 · ÁUDIO 2 ───────────────────────────────────────
    elif step == 6:
        user_state[uid] = 7
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_2)
        await msg(update, ctx,
            "Se você quiser eu te mando amor 🔥 \n\n"
            "Posso amor?",
            delay=2
        )

   # ── 7 · ÁUDIO 3 + VÍDEO 2 ────────────────────────────
    elif step == 7:
        user_state[uid] = 8
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_3)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx,
            "Gostou, lindo? posso mandar outro? \n\n",
            delay=2
        )

    # ── 8 · ÁUDIO 4 ───────────────────────────────────────
    elif step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_4)
        await msg(update, ctx,
            "Melhor que uma foto, um videozinho 🔥\n\n"
           
        )

   # ── 9 · VÍDEO 1 ───────────────────────────────────────
    elif step == 9:
        user_state[uid] = 10
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_3)
        await msg(update, ctx,
            "Esse vídeozinho que Mandei tem 4 minitos e no final gozei bem gostoso  🔥\n\n"
            "Tenho muuiito mais amor, o vip que eu to vendendo tem vários vídeos, inclusive varios videos dando muito o meu cuzinho.",
            delay=2
        )

    # ── 11 · IMAGEM + urgência ────────────────────────────
    elif step == 10:
        user_state[uid] = 11
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_1)
        await asyncio.sleep(120)  # 2 minutos de suspense
        await typing(chat, ctx)
        await update.message.reply_text(
            "São mais de x conteúdos e várias fotinhas dando muito o cuzinho, masturbando até gozar VÍDEOS COM MINHAS AMIGUINHASS e muito mais \n\n"
            "Normalmente eu vendo mais caro mas hoje tô deixando entrar pro R$ 19,99😏"
            "Se você comprar agora podemos marcar uma chamadinha de vídeo ou até mesmo se encontrar possoalmente",
            delay=2
        )
 # ── 1 · recebe o nome ─────────────────────────────────
    if step == 11:
        user_state[uid] = 12
        nome = text.split()[0].capitalize() if text else (update.effective_user.first_name or "você")
        await msg(update, ctx,
            "Te manda o acesso e a gente combina certinho! 💕\n\n"
            "Deixa eu gerar seu link de pagamento... ⏳"
            f"Que nome lindo, {nome}! 🥰\n\n"
             "Tudo bem com você?"
        )
    
      # ── 11 · Gera link de checkout ───────────────────────────
    elif step == 12:
        user_state[uid] = 99
        nome = (update.effective_user.first_name or "Cliente")
        email = f"user_{uid}@telegram.bot"
        
        await msg(update, ctx,
            "https://t.me/Flavinahbot \n\n"
        )
        

    # ── 99 · fim ──────────────────────────────────────────
    elif step == 99:
        await msg(update, ctx, "Já te enviei tudo! 😊 Qualquer dúvida é só chamar aqui. 💛")

    # ── sem /start ────────────────────────────────────────
    else:
        await msg(update, ctx, "Oi! Digite /start para começar. 😊")


# ══════════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════════

def main():
    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("capturar_id", capturar_id))

    # Captura de mídias em modo de captura
    app.add_handler(MessageHandler(
       filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE,
        capturar_midia
    ))

    # Mensagens e mídias — o handler principal decide o que fazer
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle))

    logger.info("✅ Bot rodando!")
    if MODO_CAPTURA:
        logger.info("⚠️  MODO CAPTURA ATIVO — use /capturar_id para obter file_ids")

    app.run_polling()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bot de Vendas - Telegram
Hospedado no Railway — Python 3.11 + PTB 21.9
"""

import asyncio
import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ══════════════════════════════════════════════════════════
TOKEN = os.getenv(
    "TOKEN",
    "8790169082:AAEqhlwMh5X-6pPGzjp6SgE9rHe5IO5nHvY",
)

LINK_ENTREGA = os.getenv("LINK_ENTREGA", "https://t.me/Flavinahbot")

# ══════════════════════════════════════════════════════════
# MÍDIAS (File IDs)
# ══════════════════════════════════════════════════════════
AUDIO_1 = "AwACAgEAAxkBAAPDagO9XdZYKv9_M-_F4GAF1B_d8-0AAnwGAALagiFEYK8SjDXgbrA7BA"
AUDIO_2 = "AwACAgEAAxkBAAOragO8ntVXUe33j6mcwSds5sNAJa0AAnYGAALagiFE5m4QqBjT_CM7BA"
AUDIO_3 = "AwACAgEAAxkBAAOvagO8x6finonjz_t2PfcAAUJhNSnzAAJ3BgAC2oIhREoIjn8DBrjHOwQ"
AUDIO_4 = "AwACAgEAAxkBAAOzagO9AAHZX3sS7qgWbcSgPa1o5oXfAAJ4BgAC2oIhRLJ2D1IYZcxJOwQ"

VIDEO_1 = "BAACAgEAAxkBAAOSagO6XlYtWkoROh6j9VlpvOOnAYgAAnAGAALagiFEF7_3Rf_BhSI7BA"
VIDEO_2 = "BAACAgEAAxkBAAOUagO6fle6NhGsATRoEUx288EzWF4AAnEGAALagiFEl6p5skCkVhE7BA"
VIDEO_3 = "BAACAgEAAxkBAAObagO6sAr3cWOJ21TnfJtOjAVPMegAAnIGAALagiFE9jVtXuW8HUU7BA"

IMAGE_1 = (
    "AgACCagEAAxkBAANcagOiTrmhMjEPiiWMLWWrAAGqaU2gAAIMDGsbI1oRRNwOpLHrWtClAQADAgADdwADOwQ"
)

# Modo captura (use /capturar_id para obter file_id das mídias)
MODO_CAPTURA = os.getenv("MODO_CAPTURA", "false").lower() == "true"

# Estados do usuário
user_state: dict[int, int] = {}


# ══════════════════════════════════════════════════════════
# AJUDANTES
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
# CAPTURA DE FILE_ID
# ══════════════════════════════════════════════════════════

async def capturar_id(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["capturando"] = True
    await update.message.reply_text(
        "📎 Modo de captura ativado!\n\n"
        "Agora envie uma foto, áudio ou vídeo direto no chat.\n"
        "Vou te devolver o file_id dela. 📋"
    )


async def capturar_midia(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.user_data.get("capturando"):
        return

    message = update.message
    file_id = None
    tipo = None

    if message.photo:
        file_id = message.photo[-1].file_id
        tipo = "🖼 IMAGE"
    elif message.voice:
        file_id = message.voice.file_id
        tipo = "🎙 VOICE"
    elif message.audio:
        file_id = message.audio.file_id
        tipo = "🎵 AUDIO"
    elif message.video:
        file_id = message.video.file_id
        tipo = "🎬 VIDEO"
    elif message.video_note:
        file_id = message.video_note.file_id
        tipo = "📹 VIDEO_NOTE"
    elif message.document:
        file_id = message.document.file_id
        if message.document.mime_type and message.document.mime_type.startswith("image/"):
            tipo = "🖼 IMAGE"
        else:
            tipo = "📄 DOCUMENT"

    if file_id:
        logger.info("FILE_ID CAPTURADO | %s | %s", tipo, file_id)
        await update.message.reply_text(
            f"{tipo} — File ID capturado! ✅\n\n`{file_id}`\n\n"
            "Cole esse valor na variável correspondente no Railway. 🚀",
            parse_mode="Markdown",
        )
        ctx.user_data["capturando"] = False
    else:
        await update.message.reply_text(
            "⚠️ Não detectei uma mídia válida.\n"
            "Envie uma foto, áudio ou vídeo direto no chat.\n"
            "Se você enviou texto, tente novamente com a mídia correta."
        )


# ══════════════════════════════════════════════════════════
# /start
# ══════════════════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = 1
    await msg(
        update,
        ctx,
        "Oieee 👀 \n\n"
        "Qual é o seu nome?",
    )


# ══════════════════════════════════════════════════════════
# FLUXO DE VENDAS
# ══════════════════════════════════════════════════════════

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    chat = update.effective_chat.id
    text = (update.message.text or "").strip()
    step = user_state.get(uid, 0)

    # Captura de mídia
    if ctx.user_data.get("capturando"):
        await capturar_midia(update, ctx)
        return

    # 1 - recebe nome
    if step == 1:
        user_state[uid] = 2
        nome = text.split()[0].capitalize() if text else (update.effective_user.first_name or "você")
        ctx.user_data["nome"] = nome  # salva o nome para usar depois
        await msg(update, ctx, f"Que nome lindo, {nome}! 🥰\n\nTudo bem com você?")
        return

    # 2 - interesse
    if step == 2:
        user_state[uid] = 3
        await msg(update, ctx, "Entendii amor, eu estou bem :)\n\n")
        await asyncio.sleep(3)
        await msg(update, ctx, "Pera  \n\n")
        await asyncio.sleep(3)
        await msg(update, ctx, "você consegue escutar áudio? ta meio dificil escrever kkk  😏\n\n")
        return

    # 3 - áudio 1
    if step == 3:
        user_state[uid] = 4
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_1)
        await msg(update, ctx, "Se você quiser  \n\n", delay=2)
        return

    # 4 - vídeo 1
    if step == 4:
        user_state[uid] = 5
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_1)
        await msg(update, ctx, "Fiquei \n\n", delay=2)
        return

    # 5 - conhece?
    if step == 5:
        user_state[uid] = 6
        await msg(update, ctx, "ah, ne ")
        return

    # 6 - áudio 2
    if step == 6:
        user_state[uid] = 7
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_2)
        await msg(update, ctx, "Se você quiser eu te mando ", delay=2)
        return

    # 7 - áudio 3 + vídeo 2
    if step == 7:
        user_state[uid] = 8
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_3)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx, "Gostou,  \n\n", delay=2)
        return

    # 8 - áudio 4
    if step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_4)
        await msg(update, ctx, "Melhor que uma foto, um vi\n\n")
        return

    # 9 - vídeo 3
    if step == 9:
        user_state[uid] = 10
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_3)
        await msg(update, ctx, "Esse ", delay=2)
        return

    # ══════════════════════════════════════════════════════
    # 10 - imagem + suspense + envia o LINK
    # CORREÇÃO: removido asyncio.sleep(120) e delay= inválido
    # ══════════════════════════════════════════════════════
    if step == 10:
        user_state[uid] = 99

        # Envia a imagem
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_1)

        # Suspense curto (3 segundos — ajuste como quiser)
        await asyncio.sleep(3)

        # Mensagem de quantidade de conteúdos
        await typing(chat, ctx)
        await update.message.reply_text("São mais de x conteúdos")

        # Pega o nome salvo (ou tenta pelo texto atual)
        nome = ctx.user_data.get("nome") or (
            text.split()[0].capitalize() if text else (update.effective_user.first_name or "você")
        )

        # Mensagem de acesso
        await msg(
            update,
            ctx,
            f"{nome} vou te mandar o acesso e a gente combina certinho! 💕\n\n"
            "Aqui está seu link de acesso: 🥰",
            delay=2,
        )

        # ✅ Envia o link de entrega
        await msg(update, ctx, f"{LINK_ENTREGA}", delay=1)
        return

    # 99 - fim
    if step == 99:
        await msg(update, ctx, "Já te enviei tudo! 😊 Qualquer dúvida é só chamar aqui. 💛")
        return


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════

def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .read_timeout(30)
        .connect_timeout(15)
        .get_updates_http_version("1.1")
        .build()
    )

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("capturar_id", capturar_id))

    # Captura de mídias em modo de captura
    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE,
            capturar_midia,
        )
    )

    # Mensagens — o handler principal decide o que fazer
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle))

    logger.info("✅ Bot rodando!")
    if MODO_CAPTURA:
        logger.info("⚠️ MODO CAPTURA ATIVO — use /capturar_id para obter file_ids")

    app.run_polling()


if __name__ == "__main__":
    main()

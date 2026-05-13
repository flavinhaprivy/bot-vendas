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
            tipo = "🖼
#!/usr/bin/env python3
"""Bot de Vendas - Telegram"""

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

# ══════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ══════════════════════════════════════════════════════════
TOKEN        = os.environ["TOKEN"]
LINK_ENTREGA = os.getenv("LINK_ENTREGA", "https://t.me/seu_canal_aqui")

# ── File IDs das mídias ───────────────────────────────────
AUDIO_1 = "AwACAgEAAxkBAAPDagO9XdZYKv9_M-_F4GAF1B_d8-0AAnwGAALagiFEYK8SjDXgbrA7BA"
AUDIO_2 = "AwACAgEAAxkBAAOragO8ntVXUe33j6mcwSds5sNAJa0AAnYGAALagiFE5m4QqBjT_CM7BA"
AUDIO_3 = "AwACAgEAAxkBAAOvagO8x6finonjz_t2PfcAAUJhNSnzAAJ3BgAC2oIhREoIjn8DBrjHOwQ"
AUDIO_4 = "AwACAgEAAxkBAAOzagO9AAHZX3sS7qgWbcSgPa1o5oXfAAJ4BgAC2oIhRLJ2D1IYZcxJOwQ"
AUDIO_5 = "AwACAgEAAxkBAAO3agO9HTm_G1cYWnaFeeItGMzl2zYAAnkGAALagiFEMFFUnOSN1U47BA"
AUDIO_6 = "AwACAgEAAxkBAAO7agO9LMvBA1vnaqYHfDaY--FV4vkAAnoGAALagiFEjkK2u3C9naM7BA"
AUDIO_7 = "AwACAgEAAxkBAAO_agO9Q8fvZq_k75yeCY7T63XxUx0AAnsGAALagiFE47AunJzKGzM7BA"

VIDEO_1 = "BAACAgEAAxkBAAOSagO6XlYtWkoROh6j9VlpvOOnAYgAAnAGAALagiFEF7_3Rf_BhSI7BA"
VIDEO_2 = "BAACAgEAAxkBAAOUagO6fle6NhGsATRoEUx288EzWF4AAnEGAALagiFEl6p5skCkVhE7BA"
VIDEO_3 = "BAACAgEAAxkBAAObagO6sAr3cWOJ21TnfJtOjAVPMegAAnIGAALagiFE9jVtXuW8HUU7BA"
VIDEO_4 = "BAACAgEAAxkBAAOfagO6vvPkUZYi-ELbVnuE07A_zjIAAnMGAALagiFE-eIlilAmEC47BA"
VIDEO_5 = "BAACAgEAAxkBAAOjagO6yVwW63smYxewBQg-nZSh9N4AAnQGAALagiFE0xZbqlnRpA87BA"

IMAGE_1 = "AgACCagEAAxkBAANcagOiTrmhMjEPiiWMLWWrAAGqaU2gAAIMDGsbI1oRRNwOpLHrWtClAQADAgADdwADOwQ"
IMAGE_2 = "AgACAgEAAxkBAAPHagO9vMPmxnJHayQerq_GdJGAVJoAAhIMaxvagiFEDAqpCxdRkJABAAMCAAN3AAM7BA"

# ══════════════════════════════════════════════════════════
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

user_state: dict[int, int] = {}


# ══════════════════════════════════════════════════════════
# HELPERS
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
        tipo = "🖼 IMAGE" if message.document.mime_type and message.document.mime_type.startswith("image/") else "📄 DOCUMENT"

    if file_id:
        logger.info("FILE_ID CAPTURADO | %s | %s", tipo, file_id)
        await update.message.reply_text(
            f"{tipo} — File ID capturado! ✅\n\n`{file_id}`\n\n"
            "Cole esse valor na variável correspondente. 🚀",
            parse_mode="Markdown",
        )
        ctx.user_data["capturando"] = False
    else:
        await update.message.reply_text(
            "⚠️ Não detectei uma mídia válida.\n"
            "Envie uma foto, áudio ou vídeo direto no chat."
        )


# ══════════════════════════════════════════════════════════
# /start
# ══════════════════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = 1
    await msg(update, ctx, "Oieee 👀 \n\nQual é o seu nome?")


# ══════════════════════════════════════════════════════════
# FLUXO DE VENDAS
# ══════════════════════════════════════════════════════════

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    chat = update.effective_chat.id
    text = (update.message.text or "").strip()
    step = user_state.get(uid, 0)

    # Modo captura
    if ctx.user_data.get("capturando"):
        await capturar_midia(update, ctx)
        return

    # ── 1 · recebe o nome ────────────────────────────────
    if step == 1:
        user_state[uid] = 2
        nome = text.split()[0].capitalize() if text else (update.effective_user.first_name or "você")
        ctx.user_data["nome"] = nome
        await msg(update, ctx, f"Que nome lindo, {nome}! 🥰\n\nTudo bem com você?")

    # ── 2 · interesse ────────────────────────────────────
    elif step == 2:
        user_state[uid] = 3
        await msg(update, ctx, "Entendii amor, eu estou bem :)")
        await asyncio.sleep(3)
        await msg(update, ctx, "você consegue escutar áudio? ta meio difícil escrever kkk 😏")

    # ── 3 · ÁUDIO 1 ──────────────────────────────────────
    elif step == 3:
        user_state[uid] = 4
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_1)
        await msg(update, ctx, "Se você quiser \n\n", delay=2)

    # ── 4 · VÍDEO 1 ──────────────────────────────────────
    elif step == 4:
        user_state[uid] = 5
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_1)
        await msg(update, ctx, "Fiquei \n\n", delay=2)

    # ── 5 ────────────────────────────────────────────────
    elif step == 5:
        user_state[uid] = 6
        await msg(update, ctx, "ah, nem me apresentei direito \n\n")

    # ── 6 · ÁUDIO 2 ──────────────────────────────────────
    elif step == 6:
        user_state[uid] = 7
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_2)
        await msg(update, ctx, "Se você quiser eu te mando", delay=2)

    # ── 7 · ÁUDIO 3 + VÍDEO 2 ───────────────────────────
    elif step == 7:
        user_state[uid] = 8
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_3)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx, "Gostou? \n\n", delay=2)

    # ── 8 · ÁUDIO 4 ──────────────────────────────────────
    elif step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_4)
        await msg(update, ctx, "Melhor que uma foto, um vide \n\n")

    # ── 9 · VÍDEO 3 ──────────────────────────────────────
    elif step == 9:
        user_state[uid] = 10
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_3)
        await msg(update, ctx, "Esse vídeo \n\n", delay=2)

    # ── 10 · ÁUDIO 5 ─────────────────────────────────────
    elif step == 10:
        user_state[uid] = 11
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_5)
        await msg(update, ctx, "Tá vendo? É EXATAMENTE isso que você leva! 🔥\n\nBora? Me manda um \"quero\" 👇", delay=2)

    # ── 11 · ÁUDIO 6 + VÍDEO 4 ──────────────────────────
    elif step == 11:
        user_state[uid] = 12
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_6)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_4)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx, "Ainda aqui? 😍\n\nTudo que você viu está no pacote. Gostou? 👇")

    # ── 12 · ÁUDIO 7 ─────────────────────────────────────
    elif step == 12:
        user_state[uid] = 13
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_7)
        await msg(update, ctx, "Tá chegando no melhor… 🤭\n\nPrepara o coração! 💥", delay=2)

    # ── 13 · VÍDEO 5 ─────────────────────────────────────
    elif step == 13:
        user_state[uid] = 14
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_5)
        await msg(update, ctx, "PRONTO! É ISSO! 🔥🔥🔥\n\nAgora você já sabe o que vai levar…\n\nVem fechar! 👇", delay=2)

    # ── 14 · IMAGEM 1 + suspense ─────────────────────────
    elif step == 14:
        user_state[uid] = 15
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_1)
        await asyncio.sleep(5)
        await typing(chat, ctx)
        await msg(update, ctx, "São mais de x conteúdos exclusivos… 🤭")
        await msg(update, ctx, "Ainda pensando? 🤔\n\nOlha, esse preço é por TEMPO LIMITADO…", delay=2)
        await msg(update, ctx, "Quando eu fechar as vagas, acabou. Simples assim. 💛", delay=2)

    # ── 15 · IMAGEM 2 + link final ───────────────────────
    elif step == 15:
        user_state[uid] = 99
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_2)
        await asyncio.sleep(3)

        nome = ctx.user_data.get("nome") or (update.effective_user.first_name or "você")

        await msg(update, ctx,
            f"{nome}, vou te mandar o acesso e a gente combina certinho! 💕\n\n"
            "Aqui está seu link de acesso 🥰",
            delay=2
        )
        await msg(update, ctx, f"👉 {LINK_ENTREGA}", delay=1)

    # ── 99 · fim ─────────────────────────────────────────
    elif step == 99:
        await msg(update, ctx, "Já te enviei tudo! 😊 Qualquer dúvida é só chamar aqui. 💛")


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

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("capturar_id", capturar_id))
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE,
        capturar_midia
    ))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle))

    logger.info("✅ Bot rodando!")
    app.run_polling()


if __name__ == "__main__":
    main()

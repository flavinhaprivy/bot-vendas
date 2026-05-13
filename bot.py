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
LINK_ENTREGA = os.getenv("LINK_ENTREGA", "https://t.me/Flavinahbot")

# ── File IDs das mídias ───────────────────────────────────
AUDIO_1 = "AwACAgEAAxkBAAIKN2oE4zwHq5put-i8m3ty2B_eKhg9AAKZBgAC2oIpRP_DMyd44CZGOwQ"
AUDIO_2 = "AwACAgEAAxkBAAIKP2oE45iPAR0bVxjmRs3Yy8Ge5HtDAAKbBgAC2oIpRGRg27Y9Kd81OwQ"
AUDIO_3 = "AwACAgEAAxkBAAIKQ2oE49D-HMOaDCObKKbB5onQM0XWAAKcBgAC2oIpRC7xnG0onx5oOwQ"
AUDIO_4 = "AwACAgEAAxkBAAIKR2oE5AfWHjv4ELNaPbwE_S9KrUtVAAKdBgAC2oIpRN5-11Pv0VisOwQ"
AUDIO_5 = "AwACAgEAAxkBAAO3agO9HTm_G1cYWnaFeeItGMzl2zYAAnkGAALagiFEMFFUnOSN1U47BA"
AUDIO_6 = "AwACAgEAAxkBAAO7agO9LMvBA1vnaqYHfDaY--FV4vkAAnoGAALagiFEjkK2u3C9naM7BA"
AUDIO_7 = "AwACAgEAAxkBAAO_agO9Q8fvZq_k75yeCY7T63XxUx0AAnsGAALagiFE47AunJzKGzM7BA"

VIDEO_1 = "CgACAgEAAxkBAAIKS2oE5NbhDGsNyzOeKQ4Oanfxz3q4AAKfBgAC2oIpRIKn-t2fIu5QOwQ"
VIDEO_2 = "BAACAgEAAxkBAAIKVGoE5vNBmS28CVZgL9uRmkp0adICAAKgBgAC2oIpRDFGp6TwUHL9OwQ"
VIDEO_3 = "BAACAgEAAxkBAAObagO6sAr3cWOJ21TnfJtOjAVPMegAAnIGAALagiFE9jVtXuW8HUU7BA"
VIDEO_4 = "BAACAgEAAxkBAAOfagO6vvPkUZYi-ELbVnuE07A_zjIAAnMGAALagiFE-eIlilAmEC47BA"
VIDEO_5 = "BAACAgEAAxkBAAOjagO6yVwW63smYxewBQg-nZSh9N4AAnQGAALagiFE0xZbqlnRpA87BA"

IMAGE_1 = "AgACAgEAAxkBAAIKL2oE4ptTxnZXpXobCbEyEXtMKau2AAI-DGsbwBMRRNvWuNb676VCAQADAgADdwADOwQ"
IMAGE_2 = "AgACAgEAAxkBAAIKUGoE5iCisdBhbohnr5oCx5EgnI0uAAIlDWsb2oIpREL_hrPCj9k3AQADAgADeAADOwQ"


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
        await msg(update, ctx, "Pera aí que já converso contigo, mo é que tô no banho agora\n\n"
                  "você consegue escutar áudio? ta meio dificil escrever kkk  😏")

    # ── 3 · ÁUDIO 1 ──────────────────────────────────────
    elif step == 3:
        user_state[uid] = 4
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_1)
        await msg(update, ctx, "Se você quiser eu te mando amor 🔥 \n\n"
                  "kkk mas você promete que isso fica só entre a gente? \n\n", delay=2)

    # ── 4 · VÍDEO 1 ──────────────────────────────────────
    elif step == 4:
        user_state[uid] = 5
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_1)
        await msg(update, ctx, "Fiquei até com vergonha agora kkk \n\n", delay=2)

    # ── 5 ────────────────────────────────────────────────
    elif step == 5:
        user_state[uid] = 6
        await msg(update, ctx, "ah, nem me apresentei direito, meu nome é Miya e fiz 21 aninhos esses dias 😄 \n\n"
                  "Comecei a morar sozinha aqui ( ip usuário) e faço faculdade online de jornalismo, como não tenho muito tempo pra sair de casa por conta das aulas comecei a vender meus videos e fotos aqui no telegram \n\n"
                  "Comecei a fazer Conteúdo 18+  escondida, me promete que isso fica só entre a gente? \n\n")

    # ── 6 · ÁUDIO 2 ──────────────────────────────────────
    elif step == 6:
        user_state[uid] = 7
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_2)
        await msg(update, ctx, "Se você quiser eu te mando amor 🔥 \n\n"
                  "Posso amor?", delay=2)

    # ── 7 · ÁUDIO 3 + VÍDEO 2 ───────────────────────────
    elif step == 7:
        user_state[uid] = 8
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_3)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=IMAGE_2)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx, "Gostou, lindo? posso mandar outro? \n\n", delay=2)

    # ── 8 · ÁUDIO 4 ──────────────────────────────────────
    elif step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_4)
        await msg(update, ctx, "Melhor que uma foto, um videozinho 🔥\n\n")

    # ── 9 · VÍDEO 3 ──────────────────────────────────────
    elif step == 9:
        user_state[uid] = 10
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await msg(update, ctx, "Esse vídeozinho que Mandei tem 4 minitos e no final gozei bem gostoso  🔥\n\n"
                  "Tenho muuiito mais amor, o vip que eu to vendendo tem vários vídeos, inclusive varios videos dando muito o meu cuzinho.", delay=2)

    # ── 10 · ÁUDIO 5 ─────────────────────────────────────
    elif step == 10:
        user_state[uid] = 11
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=IMAGE_1)
        await msg(update, ctx, "São mais de x conteúdos e várias fotinhas dando muito o cuzinho, masturbando até gozar VÍDEOS COM MINHAS AMIGUINHASS e muito mais \n\n"
                  "Normalmente eu vendo mais caro mas hoje tô deixando entrar pro R$ 19,99😏\n\n"
                  "Se você comprar agora podemos marcar uma chamadinha de vídeo ou até mesmo se encontrar possoalmente", delay=2)

    # ── 11 · ÁUDIO 6 + VÍDEO 4 ──────────────────────────
    elif step == 11:
        user_state[uid] = 15

        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_6)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_4)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx, "Te manda o acesso e a gente combina certinho! 💕\n\n"
                  "Deixa eu gerar seu link de pagamento... ⏳")

    # ── 15 · IMAGEM 2 + link final ───────────────────────
    elif step == 15:
        user_state[uid] = 99
        await asyncio.sleep(2)

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
        user_state.pop(uid, None)

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

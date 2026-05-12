#!/usr/bin/env python3
"""
Bot de Vendas - Telegram
Hospedado no Railway — Python 3.11 + PTB 21.9
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

# ══════════════════════════════════════════════════════════
#   CONFIGURAÇÕES  ←  preencha aqui ou nas variáveis do Railway
# ══════════════════════════════════════════════════════════
TOKEN        = os.getenv("TOKEN",        "8790169082:AAEqhlwMh5X-6pPGzjp6SgE9rHe5IO5nHvY")
PIX_KEY      = os.getenv("PIX_KEY",      "SEU_PIX_AQUI")
PIX_VALUE    = os.getenv("PIX_VALUE",    "R$ 00,00")
LINK_ENTREGA = os.getenv("LINK_ENTREGA", "https://SEU_LINK_AQUI")

# ── File IDs das mídias ───────────────────────────────────
# Use o comando /capturar_id para descobrir o file_id de cada mídia
# Envie a mídia pro bot após ativar o modo de captura com /capturar_id
# Cole os IDs nas variáveis do Railway ou diretamente aqui
AUDIO_1 = os.getenv("AUDIO_1", "AUDIO_1_FILE_ID")
AUDIO_2 = os.getenv("AUDIO_2", "AUDIO_2_FILE_ID")
AUDIO_3 = os.getenv("AUDIO_3", "AUDIO_3_FILE_ID")
VIDEO_1 = os.getenv("VIDEO_1", "VIDEO_1_FILE_ID")
VIDEO_2 = os.getenv("VIDEO_2", "VIDEO_2_FILE_ID")
IMAGE_1 = os.getenv("IMAGE_1", "IMAGE_1_FILE_ID")

# ── Adicione mais mídias aqui se precisar ─────────────────
# AUDIO_4 = os.getenv("AUDIO_4", "AUDIO_4_FILE_ID")
# VIDEO_3 = os.getenv("VIDEO_3", "VIDEO_3_FILE_ID")
# IMAGE_2 = os.getenv("IMAGE_2", "IMAGE_2_FILE_ID")
# ══════════════════════════════════════════════════════════

# ── Modo de captura de File IDs ───────────────────────────
# Mude para True temporariamente para capturar os file_ids das mídias
# Depois volte para False antes de subir para produção
MODO_CAPTURA = os.getenv("MODO_CAPTURA", "false").lower() == "true"
# ══════════════════════════════════════════════════════════

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Guarda em qual passo cada usuário está
user_state: dict[int, int] = {}


# ══════════════════════════════════════════════════════════
#   CAPTURA DE FILE IDs
#   Use /capturar_id e envie qualquer mídia pro bot.
#   O file_id aparecerá no terminal e será enviado de volta pra você.
# ══════════════════════════════════════════════════════════

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
        "Oi! 😊 Seja muito bem-vindo(a)!\n\n"
        "Você veio no lugar certo. Tenho algo MUITO especial pra te mostrar... 👀\n\n"
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
            "O que eu vou te mostrar hoje mudou a vida de muita gente.\n\n"
            "Você topa ver? Responde SIM ou NÃO 👇"
        )

    # ── 2 · interesse ─────────────────────────────────────
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

    # ── 3 · conhece? ──────────────────────────────────────
    elif step == 3:
        user_state[uid] = 4
        await msg(update, ctx,
            "Perfeito! Então vou começar do início mesmo 😄\n\n"
            "Manda um \"ok\" que já te envio o primeiro conteúdo especial 🎧"
        )

    # ── 4 · ÁUDIO 1 ───────────────────────────────────────
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

    # ── 5 · VÍDEO 1 ───────────────────────────────────────
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

    # ── 6 · apresenta pacote ──────────────────────────────
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
            "Vou te mandar mais uma coisinha antes do pagamento… aguarda! 🎧",
            delay=2
        )

    # ── 7 · ÁUDIO 2 ───────────────────────────────────────
    elif step == 7:
        user_state[uid] = 8
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_2)
        await msg(update, ctx,
            "Tá vendo? É EXATAMENTE isso que você leva no pacote! 🔥\n\n"
            "Bora? Me manda um \"quero\" 👇",
            delay=2
        )

    # ── 8 · ÁUDIO 3 + VÍDEO 2 ────────────────────────────
    elif step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_3)
        await asyncio.sleep(2)
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await update.message.reply_text(
            "Ainda aqui? 😍 Porque EU tô!\n\n"
            "Tudo que você viu está no pacote.\n\n"
            "Me fala: gostou? 👇"
        )

    # ── 9 · mais um áudio ─────────────────────────────────
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

    # ── 10 · VÍDEO final ──────────────────────────────────
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

    # ── 11 · IMAGEM + urgência ────────────────────────────
    elif step == 11:
        user_state[uid] = 12
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_1)
        await asyncio.sleep(120)  # 2 minutos de suspense
        await typing(chat, ctx)
        await update.message.reply_text(
            "Ainda pensando? 🤔\n\nOlha, esse preço é por TEMPO LIMITADO…"
        )
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

    # ── 12 · dúvida ou confirmação ────────────────────────
    elif step == 12:
        if "2" in text or "dúvida" in text.lower() or "duvida" in text.lower():
            await msg(update, ctx, "Claro! Me faz a pergunta que te respondo agora mesmo 😊")
            # fica no passo 12
        else:
            user_state[uid] = 13
            await msg(update, ctx,
                f"Ótimo! 🎉 Que decisão incrível!\n\n"
                f"Me confirma: você quer garantir o pacote por *{PIX_VALUE}*?",
                parse_mode="Markdown"
            )

    # ── 13 · envia PIX ────────────────────────────────────
    elif step == 13:
        user_state[uid] = 14
        await msg(update, ctx, "SHOW! Preparando seu pagamento… 💳")
        await msg(update, ctx,
            "📲 *PAGAMENTO VIA PIX*\n\n"
            f"🔑 Chave: `{PIX_KEY}`\n"
            f"💰 Valor: *{PIX_VALUE}*\n\n"
            "Faça o pagamento e me manda o *comprovante* aqui!\n\n"
            "Assim que confirmar, te mando o acesso na hora! ⚡",
            delay=2,
            parse_mode="Markdown"
        )

    # ── 14 · recebe comprovante ───────────────────────────
    elif step == 14:
        user_state[uid] = 99
        await msg(update, ctx, "Recebi! ✅ Confirmando o pagamento…\n\nUm segundo! ⏳")
        await msg(update, ctx,
            "✅ *PAGAMENTO CONFIRMADO!* 🎉\n\n"
            f"Aqui está o seu acesso:\n👉 {LINK_ENTREGA}\n\n"
            "Seja muito bem-vindo(a)! 🥳\n"
            "Qualquer dúvida, é só falar aqui 💬",
            delay=2,
            parse_mode="Markdown"
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
        filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE | filters.Document,
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

action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_2)
        await asyncio.sleep(8)
        await typing(chat, ctx)
        await msg(update, ctx, 
                  "Gostou, lindo? posso mandar outro? \n\n"
                  , delay=2)
        return

    # 8 - áudio 4
    if step == 8:
        user_state[uid] = 9
        await voice_action(chat, ctx)
        await ctx.bot.send_voice(chat_id=chat, voice=AUDIO_4)
        await msg(update, ctx, 
                  "Melhor que uma foto, um videozinho 🔥\n\n")
        return

    # 9 - vídeo 3
    if step == 9:
        user_state[uid] = 10
        await video_action(chat, ctx)
        await ctx.bot.send_video(chat_id=chat, video=VIDEO_3)
        await msg(update, ctx, 
                  "Esse vídeozinho que Mandei tem 4 minitos e no final gozei bem gostoso  🔥\n\n"
                  "Tenho muuiito mais amor, o vip que eu to vendendo tem vários vídeos, inclusive varios videos dando muito o meu cuzinho.", 
                  delay=2)
        return

    # 10 - imagem + suspense
    if step == 10:
        user_state[uid] = 11
        await ctx.bot.send_photo(chat_id=chat, photo=IMAGE_1)
        await asyncio.sleep(120)
        await typing(chat, ctx)
        await update.message.reply_text( 
            "São mais de x conteúdos e várias fotinhas dando muito o cuzinho, masturbando até gozar VÍDEOS COM MINHAS AMIGUINHASS e muito mais \n\n"
            "Normalmente eu vendo mais caro mas hoje tô deixando entrar pro R$ 19,99😏 \n\n"
            "Se você comprar agora podemos marcar uma chamadinha de vídeo ou até mesmo se encontrar possoalmente", 
            delay=2)
        return

    # 11 - ETAPA que você quer: APENAS enviar o link
    if step == 11:
        user_state[uid] = 99
        nome = text.split()[0].capitalize() if text else (update.effective_user.first_name or "você")
        await msg(update, ctx, 
                  f"{nome} vou te manda o acesso e a gente combina certinho! 💕\n\n"
                  "Deixa eu gerar seu link de pagamento... ⏳! 🥰\n\n ", 
                  delay=0)
        await msg(update, ctx, f"{LINK_ENTREGA} \n\n")
        return

    # 99 - fim (encerrar fluxo)
    if step == 99:
        await msg(update, ctx, "Já te enviei tudo! 😊 Qualquer dúvida é só chamar aqui. 💛")
        user_state.pop(uid, None)  # evita reentrar/loopar no estado final
        return


    
   


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════

def main():
    app = (
        Application.builder()
        .token(TOKEN)
        # Aumenta timeouts e adiciona tentativas para reduzir httpx.ReadError na inicialização
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
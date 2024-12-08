#!/usr/bin/env python3
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext.filters import TEXT

from config import TOKEN
from yt_downloader import YT_DLP_Downloader


class BotHandlers:

    async def hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'/hello\n/help')

    async def download_upload_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE, url: str) -> None:
        # Download the video
        yt_downloader = YT_DLP_Downloader()
        yt_downloader.setUrl(url)
        output_file = yt_downloader.download_audio()

        if(output_file == None):
            await update.message.reply_text("Error downloading video")
            return

        await update.message.reply_document(document=open(output_file, 'rb'))

        os.remove(output_file)

    async def download(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Get the download link from the message
        message = update.message.text
        url = message.replace('/download ', '')

        context.application.create_task(self.download_upload_audio(update, context, url))
        await update.message.reply_text("Downloading and uploading video...")

    async def message_handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)

class BotApp:
    def __init__(self):
        self.app = ApplicationBuilder().token(TOKEN).build()
        self.handlers = BotHandlers()

        self.app.add_handler(CommandHandler("hello", self.handlers.hello))
        self.app.add_handler(CommandHandler("help", self.handlers.help_command))
        self.app.add_handler(CommandHandler("download", self.handlers.download))
        self.app.add_handler(MessageHandler(TEXT, self.handlers.message_handle))


    def run(self):
        self.app.run_polling()



bot_app = BotApp()
bot_app.run()
#!/usr/bin/env python3

import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext.filters import TEXT

from config import TOKEN
from yt_downloader import YT_DLP_Downloader


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'/hello\n/help')

async def download_upload_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str) -> None:
    # Download the video
    yt_downloader = YT_DLP_Downloader()
    yt_downloader.setUrl(url)
    output_file = yt_downloader.download_audio()

    if(output_file == None):
        await update.message.reply_text("Error downloading video")
        return

    await update.message.reply_document(document=open(output_file, 'rb'))

    os.remove(output_file)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the download link from the message
    message = update.message.text
    url = message.replace('/download ', '')

    context.application.create_task(download_upload_audio(update, context, url))
    await update.message.reply_text("Downloading and uploading video...")

async def message_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("download", download))
app.add_handler(MessageHandler(TEXT, message_handle))


app.run_polling()
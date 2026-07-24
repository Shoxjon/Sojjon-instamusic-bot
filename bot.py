
import os
import yt_dlp
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Instagram video havolasini yuboring 🎥\n"
        "Men sizga video va undan ajratilgan MP3 musiqani yuboraman 🎵"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com" not in url:
        await update.message.reply_text("Instagram havolasini yuboring.")
        return

    await update.message.reply_text("⏳ Video va audio tayyorlanmoqda...")

    video_file = "video.mp4"
    audio_file = "audio.mp3"

    try:
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": video_file,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_file,
            "-vn",
            "-acodec", "libmp3lame",
            "-q:a", "2",
            audio_file
        ], check=True)

        with open(video_file, "rb") as video:
            await update.message.reply_video(video)

        with open(audio_file, "rb") as audio:
            await update.message.reply_audio(
                audio,
                title="Instagram Audio 🎵"
            )

        os.remove(video_file)
        os.remove(audio_file)

    except Exception as e:
        await update.message.reply_text(
            "❌ Yuklashda xatolik yuz berdi. Boshqa Instagram link bilan urinib ko‘ring."
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
    )

    app.run_polling()

if __name__ == "__main__":
    main()

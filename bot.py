import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@YOUR_CHANNEL_USERNAME")
VIDEO_FILE_ID = os.getenv("VIDEO_FILE_ID", "YOUR_VIDEO_FILE_ID")
PORT = int(os.getenv("PORT", "10000"))

# Small HTTP server for Render
app = Flask(__name__)

@app.get("/")
def home():
    return "Telegram bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🔴 Join Channel",
                url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Verify",
                callback_data="verify"
            )
        ]
    ]

    await update.message.reply_text(
        "🔒 ভিডিওটি দেখতে হলে প্রথমে আমাদের Telegram Channel-এ Join করুন।\n\n"
        "1️⃣ Join Channel চাপুন\n"
        "2️⃣ Channel-এ Join করুন\n"
        "3️⃣ তারপর ✅ Verify চাপুন",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Verify channel membership
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in ("member", "administrator", "creator"):

            await query.message.reply_text(
                "✅ Verification successful! ভিডিও পাঠানো হচ্ছে..."
            )

            await context.bot.send_video(
                chat_id=user_id,
                video=VIDEO_FILE_ID,
                caption="🎬 আপনার ভিডিও উপভোগ করুন!"
            )

        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔴 Join Channel",
                        url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Verify Again",
                        callback_data="verify"
                    )
                ]
            ]

            await query.message.reply_text(
                "❌ আপনি এখনো Channel-এ Join করেননি। "
                "আগে Join করুন, তারপর আবার Verify চাপুন।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception:
        await query.message.reply_text(
            "⚠️ Verification করা যাচ্ছে না। "
            "নিশ্চিত করুন Bot-টি Channel-এর Administrator।"
        )


# Send Video → Get Video File ID
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        file_id = update.message.video.file_id

        await update.message.reply_text(
            f"🎬 Video File ID:\n\n{file_id}"
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    # Start web server for Render
    Thread(target=run_web, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            verify,
            pattern="^verify$"
        )
    )

    # When a video is sent to the bot, reply with File ID
    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            get_video_id
        )
    )

    print("🤖 Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@YOUR_CHANNEL_USERNAME")
VIDEO_FILE_ID = os.getenv("VIDEO_FILE_ID", "YOUR_VIDEO_FILE_ID")
PORT = int(os.getenv("PORT", "10000"))

# Small HTTP server for Render
app = Flask(__name__)

@app.get("/")
def home():
    return "Telegram bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🔴 Join Channel",
                url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Verify",
                callback_data="verify"
            )
        ]
    ]

    await update.message.reply_text(
        "🔒 ভিডিওটি দেখতে হলে প্রথমে আমাদের Telegram Channel-এ Join করুন।\n\n"
        "1️⃣ Join Channel চাপুন\n"
        "2️⃣ Channel-এ Join করুন\n"
        "3️⃣ তারপর ✅ Verify চাপুন",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Verify channel membership
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in ("member", "administrator", "creator"):

            await query.message.reply_text(
                "✅ Verification successful! ভিডিও পাঠানো হচ্ছে..."
            )

            await context.bot.send_video(
                chat_id=user_id,
                video=VIDEO_FILE_ID,
                caption="🎬 আপনার ভিডিও উপভোগ করুন!"
            )

        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔴 Join Channel",
                        url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Verify Again",
                        callback_data="verify"
                    )
                ]
            ]

            await query.message.reply_text(
                "❌ আপনি এখনো Channel-এ Join করেননি। "
                "আগে Join করুন, তারপর আবার Verify চাপুন।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception:
        await query.message.reply_text(
            "⚠️ Verification করা যাচ্ছে না। "
            "নিশ্চিত করুন Bot-টি Channel-এর Administrator।"
        )


# Send Video → Get Video File ID
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        file_id = update.message.video.file_id

        await update.message.reply_text(
            f"🎬 Video File ID:\n\n{file_id}"
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    # Start web server for Render
    Thread(target=run_web, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            verify,
            pattern="^verify$"
        )
    )

    # When a video is sent to the bot, reply with File ID
    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            get_video_id
        )
    )

    print("🤖 Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@YOUR_CHANNEL_USERNAME")
VIDEO_FILE_ID = os.getenv("VIDEO_FILE_ID", "YOUR_VIDEO_FILE_ID")
PORT = int(os.getenv("PORT", "10000"))

# Small HTTP server for Render
app = Flask(__name__)

@app.get("/")
def home():
    return "Telegram bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🔴 Join Channel",
                url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Verify",
                callback_data="verify"
            )
        ]
    ]

    await update.message.reply_text(
        "🔒 ভিডিওটি দেখতে হলে প্রথমে আমাদের Telegram Channel-এ Join করুন।\n\n"
        "1️⃣ Join Channel চাপুন\n"
        "2️⃣ Channel-এ Join করুন\n"
        "3️⃣ তারপর ✅ Verify চাপুন",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Verify channel membership
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in ("member", "administrator", "creator"):

            await query.message.reply_text(
                "✅ Verification successful! ভিডিও পাঠানো হচ্ছে..."
            )

            await context.bot.send_video(
                chat_id=user_id,
                video=VIDEO_FILE_ID,
                caption="🎬 আপনার ভিডিও উপভোগ করুন!"
            )

        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔴 Join Channel",
                        url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Verify Again",
                        callback_data="verify"
                    )
                ]
            ]

            await query.message.reply_text(
                "❌ আপনি এখনো Channel-এ Join করেননি। "
                "আগে Join করুন, তারপর আবার Verify চাপুন।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception:
        await query.message.reply_text(
            "⚠️ Verification করা যাচ্ছে না। "
            "নিশ্চিত করুন Bot-টি Channel-এর Administrator।"
        )


# Send Video → Get Video File ID
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        file_id = update.message.video.file_id

        await update.message.reply_text(
            f"🎬 Video File ID:\n\n{file_id}"
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    # Start web server for Render
    Thread(target=run_web, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            verify,
            pattern="^verify$"
        )
    )

    # When a video is sent to the bot, reply with File ID
    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            get_video_id
        )
    )

    print("🤖 Bot is running...")

    application.run_polling()


if __name__ == "__main__":

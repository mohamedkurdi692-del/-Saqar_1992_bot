import time
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ================== CONFIG ==================
TOKEN = "8685912597:AAFWwKI0XJEUDQLO7zGLe-gLIar1ZBEp4cI"
OWNER_ID = 2011675494
DEV_USERNAME = "ShexSaqar"
CHANNEL_USERNAME = "ybpi1" 

# إعدادات الحماية الافتراضية
locks = {
    "links": True,
    "spam": True,
    "media": False
}

user_msgs = {}

# ================== تحقق اشتراك ==================
async def check_sub(user_id, context):
    try:
        member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await check_sub(user.id, context):
        btn = [[InlineKeyboardButton("📢 اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME}")]]
        await update.message.reply_text(
            "🚫 يجب الاشتراك بالقناة أولاً لتتمكن من استخدام البوت!",
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return

    buttons = [
        [InlineKeyboardButton("🛡️ الحماية", callback_data="protect")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
        [InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME}")]
    ]
    await update.message.reply_text(
        "🔥 مرحباً بك في TITAN BOT\nأقوى بوت حماية لمجموعتك 🦅",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ================== لوحة التحكم ==================
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    buttons = [
        [InlineKeyboardButton(f"🔗 الروابط: {'✅' if locks['links'] else '❌'}", callback_data="toggle_links")],
        [InlineKeyboardButton(f"🚫 الوسائط: {'✅' if locks['media'] else '❌'}", callback_data="toggle_media")],
        [InlineKeyboardButton(f"🧠 السبام: {'✅' if locks['spam'] else '❌'}", callback_data="toggle_spam")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_to_start")]
    ]
    await query.edit_message_text("⚙️ لوحة تحكم الحماية:", reply_markup=InlineKeyboardMarkup(buttons))

# ================== تبديل الإعدادات ==================
async def toggle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data.startswith("toggle_"):
        key = data.replace("toggle_", "")
        locks[key] = not locks[key]
        await panel(update, context) # تحديث اللوحة بعد التغيير

# ================== حماية ذكية ==================
async def protection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_id = update.effective_user.id
    text = update.message.text
    now = time.time()

    # نظام منع السبام
    if locks["spam"]:
        if user_id not in user_msgs: user_msgs[user_id] = []
        user_msgs[user_id].append(now)
        user_msgs[user_id] = user_msgs[user_id][-5:]
        if len(user_msgs[user_id]) >= 5 and (user_msgs[user_id][-1] - user_msgs[user_id][0] < 4):
            await update.message.delete()
            return

    # منع الروابط
    if locks["links"] and ("http" in text or "t.me" in text):
        await update.message.delete()
        return

# ================== تشغيل البوت ==================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(panel, pattern="^(protect|settings)$"))
    app.add_handler(CallbackQueryHandler(toggle_handler, pattern="^toggle_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, protection))

    print("🚀 TITAN BOT IS READY SIR SAQAR!")
    app.run_polling()

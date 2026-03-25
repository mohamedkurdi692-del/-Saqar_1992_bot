‏# ================== CONFIG ==================
‏TOKEN = "8685912597:AAHzqRcTNbyd0dum2JFtZ9tzWAkxyre_7Lo"
‏OWNER_ID = 2011675494
‏DEV_USERNAME = "@ShexSaqar"   # معرفك
‏CHANNEL_USERNAME = "@ybpi1"  # القناة
‏
‏# ===========================================
‏
‏from telegram import *
‏from telegram.ext import *
‏import time
‏import asyncio
‏
‏app = ApplicationBuilder().token(TOKEN).build()
‏
‏# ================== تحقق اشتراك ==================
‏async def check_sub(user_id, context):
‏    try:
‏        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
‏        return member.status in ["member", "administrator", "creator"]
‏    except:
‏        return False
‏
‏# ================== START ==================
‏async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
‏    user = update.effective_user
‏
‏    if not await check_sub(user.id, context):
‏        btn = [[InlineKeyboardButton("📢 اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")]]
‏        await update.message.reply_text(
‏            "🚫 يجب الاشتراك بالقناة أولاً",
‏            reply_markup=InlineKeyboardMarkup(btn)
‏        )
‏        return
‏
‏    buttons = [
‏        [InlineKeyboardButton("🛡️ الحماية", callback_data="protect")],
‏        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
‏        [InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME.replace('@','')}")]
‏    ]
‏
‏    await update.message.reply_text(
‏        "🔥 مرحباً بك في TITAN BOT\nأقوى بوت حماية",
‏        reply_markup=InlineKeyboardMarkup(buttons)
‏    )
‏
‏# ================== لوحة التحكم ==================
‏locks = {
‏    "links": True,
‏    "spam": True,
‏    "media": False
‏}
‏
‏async def panel(update, context):
‏    q = update.callback_query
‏    await q.answer()
‏
‏    buttons = [
‏        [InlineKeyboardButton("🔗 الروابط", callback_data="links")],
‏        [InlineKeyboardButton("🚫 الوسائط", callback_data="media")],
‏        [InlineKeyboardButton("🧠 السبام", callback_data="spam")]
‏    ]
‏
‏    await q.edit_message_text("⚙️ لوحة التحكم:", reply_markup=InlineKeyboardMarkup(buttons))
‏
‏# ================== تبديل ==================
‏async def toggle(update, context):
‏    q = update.callback_query
‏    data = q.data
‏
‏    locks[data] = not locks[data]
‏
‏    status = "✅ مفعل" if locks[data] else "❌ معطل"
‏    await q.answer(f"{data} {status}")
‏
‏# ================== حماية ذكية ==================
‏user_msgs = {}
‏
‏async def protection(update: Update, context: ContextTypes.DEFAULT_TYPE):
‏    if not update.message:
‏        return
‏
‏    user = update.effective_user.id
‏    text = update.message.text or ""
‏
‏    now = time.time()
‏
‏    if user not in user_msgs:
‏        user_msgs[user] = []
‏
‏    user_msgs[user].append(now)
‏    user_msgs[user] = user_msgs[user][-5:]
‏
‏    # سبام سريع
‏    if locks["spam"] and len(user_msgs[user]) >= 5:
‏        if user_msgs[user][-1] - user_msgs[user][0] < 4:
‏            await update.message.delete()
‏            await update.message.reply_text("🚫 سبام سريع")
‏            return
‏
‏    # روابط
‏    if locks["links"] and "http" in text:
‏        await update.message.delete()
‏        await update.message.reply_text("🚫 الروابط ممنوعة")
‏        return
‏
‏    # وسائط
‏    if locks["media"] and (update.message.photo or update.message.video):
‏        await update.message.delete()
‏        await update.message.reply_text("🚫 الوسائط ممنوعة")
‏        return
‏
‏# ================== عضو جديد ==================
‏async def new_member(update, context):
‏    for user in update.message.new_chat_members:
‏        await context.bot.restrict_chat_member(
‏            update.effective_chat.id,
‏            user.id,
‏            ChatPermissions(can_send_messages=False)
‏        )
‏
‏        msg = await update.message.reply_text("👋 اضغط تحقق خلال 15 ثانية")
‏
‏        await asyncio.sleep(15)
‏        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
‏
‏# ================== تشغيل ==================
‏app.add_handler(CommandHandler("start", start))
‏app.add_handler(CallbackQueryHandler(panel, pattern="protect"))
‏app.add_handler(CallbackQueryHandler(panel, pattern="settings"))
‏app.add_handler(CallbackQueryHandler(toggle))
‏
‏app.add_handler(MessageHandler(filters.ALL, protection))
‏app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
‏
‏print("🔥 TITAN BOT RUNNING...")
‏app.run_polling()

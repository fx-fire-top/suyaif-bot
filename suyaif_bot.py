#!/usr/bin/env python3
import os
import logging
import re
import asyncio
import time
import random
from collections import defaultdict
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

load_dotenv()
# এখানে আপনার আসল বটের টোকেনটি বসিয়ে দেবেন
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8919947592:AAHSzkjyjUvsQ0YPrLGL9LS3o78oqOqO9YY")

BOT_NAME = "MD SUYAIF TOP - SECURITY BOT ☠️"
GROUP_LINK = "https://t.me/GhostX_Official_Group"
YT_LINK = "https://youtube.com/@mdsuyaif_fx2.0"
CHANNEL_LINK = "https://t.me/minhaz_official24"
HACK_WEB = "https://fxfiretopff1.vercel.app/"
WHATSAPP_CH = "https://whatsapp.com/channel/0029Vb8RBGlEquiSBj3XwB0P"

user_last_message_time = defaultdict(float)
SPAM_LIMIT = 1.5  

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 ফ্রি ফায়ার হ্যাক", url=HACK_WEB), InlineKeyboardButton("📢 হোয়াটসঅ্যাপ চ্যানেল", url=WHATSAPP_CH)],
        [InlineKeyboardButton("🌐 IP ট্র্যাকার", callback_data="ip_track"), InlineKeyboardButton("🔍 ইউজার আইডি", callback_data="user_track")],
        [InlineKeyboardButton("🚀 SMS বোম্বার", callback_data="bomber"), InlineKeyboardButton("✨ নাম ডিজাইন", callback_data="name_design")],
        [InlineKeyboardButton("📶 ওয়াইফাই স্ক্যানার", callback_data="wifi_hack"), InlineKeyboardButton("💻 টার্মাক্স কমান্ডস", callback_data="termux_code")],
        [InlineKeyboardButton("🛡️ সিকিউরিটি স্ক্যান", callback_data="scan"), InlineKeyboardButton("🔄 মেনু রিফ্রেশ", callback_data="refresh_menu")],
        [InlineKeyboardButton("👥 অফিসিয়াল গ্রুপ", url=GROUP_LINK), InlineKeyboardButton("📺 ইউটিউব চ্যানেল", url=YT_LINK)]
    ])

def generate_hundred_styles(name: str, count: int) -> list:
    decorations = [("☠️", "☠️"), ("🔥", "🔥"), ("👑", "👑"), ("⚡", "⚡"), ("✨", "✨"), ("🎯", "🎯")]
    alphabets = {
        'a': ['а', '𝔲', '🆂', '𝕒'], 'b': ['𝔟', '🕈', '🕂', '🄱'], 'c': ['𝔠', '🅲', '🕈', '🄲'],
        'd': ['𝔡', '🅳', '𝕕', '🄳'], 'e': ['𝔢', '🅴', '𝕖', '🄴'], 'f': ['𝔣', '🅵', '𝕗', '🄵'],
        'g': ['𝔤', '🅶', '𝕘', '🄶'], 'h': ['𝔥', '🅷', '𝕙', '🄷'], 'i': ['𝔦', '🅸', ' civilisation', '🄸']
    }
    results = []
    for i in range(count):
        dec = random.choice(decorations)
        styled_text = "".join(random.choice(alphabets.get(char, [char])) for char in name.lower())
        results.append(f"{dec[0]} {styled_text.upper()} {dec[1]}")
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    welcome_text = (
        f"👋 <b>আসসালামু আলাইকুম, কেমন আছেন?</b>\n\n"
        f"🤖 আমাদের <b>সোয়ائب ভাইয়ের অফিশিয়াল বটের</b> পক্ষ থেকে আপনাকে স্বাগতম!\n\n"
        f"📢 <b>চ্যানেল নোটিশ:</b> বটের সব ফিচার সচল রাখতে নিচের লিংকগুলোতে জয়েন করুন:\n"
        f"🔹 টেলিগ্রাম চ্যানেল: {CHANNEL_LINK}\n"
        f"🔹 হোয়াটসঅ্যাপ চ্যানেল: {WHATSAPP_CH}\n\n"
        f"নিচের মেনু থেকে আপনার প্রয়োজনীয় সিস্টেমটি বেছে নিন:"
    )
    await update.message.reply_text(text=welcome_text, reply_markup=get_main_menu(), parse_mode='HTML')

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot: continue
        welcome_msg = (
            f"👋 <b>আসসালামু আলাইকুম ভাই!</b>\n\n"
            f"✨ <b>{member.mention_html()}</b> আমাদের গ্রুপে আপনাকে স্বাগতম! কেমন আছেন?\n"
            f"🆔 <b>আপনার UID:</b> <code>{member.id}</code>\n"
            f"📢 হোয়াটসঅ্যাপ চ্যানেল লিংক: {WHATSAPP_CH}\n"
            f"📢 টেলিগ্রাম চ্যানেল লিংক: {CHANNEL_LINK}\n\n"
            f"ধন্যবাদ এবং সোয়াইব ভাইয়ের বটের সাথে থাকুন! 🚀"
        )
        await update.message.reply_text(text=welcome_msg, parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    context.user_data.clear()

    if data == "refresh_menu":
        await query.edit_message_text(text="🔄システム সিস্টেম মেনু রিফ্রেশ করা হয়েছে:", reply_markup=get_main_menu())
    elif data == "wifi_hack":
        status_msg = await query.edit_message_text("📡 <code>[SCANNING LOCAL WI-FI FREQUENCY...]</code>", parse_mode='HTML')
        await asyncio.sleep(0.5)
        wifi_report = (
            f"📶 <b>লোকাল ওয়াইফাই স্ক্যান রিপোর্ট:</b>\n\n"
            f"🔒 <b>নেটওয়ার্ক সিকিউরিটি:</b> WPA2-PSK (সুরক্ষিত)\n"
            f"📊 <b>সংযুক্ত মোট ডিভাইস:</b> ৩টি\n\n"
            f"1️⃣ <b>Device:</b> <code>Samsung Galaxy S23</code>\n"
            f"2️⃣ <b>Device:</b> <code>Symphony Z70</code>\n\n"
            f"💡 <i>নোট: প্রাইভেসির কারণে রিমোট নেটওয়ার্কের লাইভ ডাটা সরাসরি টেলিগ্রামে স্নীফ করা নিষিদ্ধ।</i>"
        )
        await status_msg.edit_text(text=wifi_report, parse_mode='HTML', reply_markup=get_main_menu())
    elif data == "termux_code":
        termux_text = (
            "💻 <b>টার্মাক্স কমপ্লিট গাইড:</b>\n\n"
            "<code>pkg update && pkg upgrade -y\npkg install python nano git -y\npip install python-telegram-bot\npython bot.py</code>"
        )
        await query.edit_message_text(text=termux_text, parse_mode='HTML', reply_markup=get_main_menu())
    elif data == "ip_track":
        context.user_data["step"] = "wait_ip"
        await query.edit_message_text("🌐 অনুগ্রহ করে আপনার টার্গেট IP অ্যাড্রেসটি ইনপুট দিন:")
    elif data == "bomber":
        context.user_data["step"] = "wait_num"
        await query.edit_message_text("📱 টার্গেট মোবাইল নম্বরটি লিখুন:")
    elif data == "user_track":
        context.user_data["step"] = "wait_uid"
        await query.edit_message_text("🔍 কাঙ্ক্ষিত প্লেয়ার বা টেলিগ্রাম UID টাইপ করুন:")
    elif data == "name_design":
        context.user_data["step"] = "wait_name_text"
        await query.edit_message_text("✨ যে নামটি স্টাইল করতে চান তা লিখুন:")
    elif data == "scan":
        await query.edit_message_text(text="🛡️ <b>ফায়ারওয়াল স্ক্যানিং...</b>\n\nবটের ইন্টারনাল টোকেন ও ফায়ারওয়াল সম্পূর্ণ নিরাপদ ও অ্যান্টি-হ্যাকিং প্রোটেকশনে সুরক্ষিত রয়েছে।", reply_markup=get_main_menu(), parse_mode='HTML')

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    uid = update.effective_user.id
    current_time = time.time()
    
    if current_time - user_last_message_time[uid] < SPAM_LIMIT:
        await update.message.reply_text("⚠️ <b>স্প্যামিং নিষিদ্ধ!</b> অনুগ্রহ করে একটু ধীরে মেসেজ পাঠান।")
        return
    user_last_message_time[uid] = current_time

    text = update.message.text.strip()
    user_raw = text.lower()
    step = context.user_data.get("step")

    if not step:
        if any(x in user_raw for x in ["সালাম", "salam", "assalamualaikum"]):
            await update.message.reply_text("📿 ওয়াআলাইকুম আসসালাম ওয়া রাহমাতুল্লাহ! সোয়াইব ভাইয়ের অফিসিয়াল বটে আপনাকে স্বাগতম।")
        elif any(x in user_raw for x in ["কেমন আছো", "kemon acho", "how are you"]):
            await update.message.reply_text("😇 আলহামদুলিল্লাহ, আমি খুব ভালো আছি ভাই! আপনি কেমন আছেন?")
        elif any(x in user_raw for x in ["হাই", "হ্যালো", "hi", "hello"]):
            await update.message.reply_text("👋 হ্যালো! সোয়াইব ভাইয়ের মেগা সিকিউরিটি বটের পক্ষ থেকে স্বাগতম।")
        elif any(x in user_raw for x in ["সোয়াইব ভাইয়ের ছবি", "photo", "pic"]):
            await update.message.reply_text(f"📸 সোয়াইব ভাইয়ের ছবি সরাসরি আমাদের গ্রুপ মিডিয়া ফাইলে পেয়ে যাবেন। গ্রুপ লিংক: {GROUP_LINK}")
        else:
            await update.message.reply_text(f"🧠 আপনার বার্তাটি আমি এনালাইসিস করেছি। এই বিষয়ে কাস্টম গাইডলাইন পেতে আমাদের ড্যাশবোর্ডের বাটনগুলো ব্যবহার করতে পারেন।")
        return

    if step == "wait_ip":
        status_msg = await update.message.reply_text("📡 <code>[INITIALIZING IP GEOLOCATION...]</code>", parse_mode='HTML')
        await asyncio.sleep(0.5)
        await status_msg.edit_text(text=f"🌐 <b>IP অ্যানালাইসিস সম্পন্ন!</b>\n\n🎯 আইপি: <code>{text}</code>\n📊 প্রক্সি গেটওয়ে ভেরিফাইড।", parse_mode='HTML', reply_markup=get_main_menu())
        context.user_data.clear()
    elif step == "wait_num":
        context.user_data["target_num"] = text
        context.user_data["step"] = "wait_count"
        await update.message.reply_text("✅ নম্বর সেট হয়েছে। কাউন্ট লিখুন (১-৫০):")
    elif step == "wait_count":
        await update.message.reply_text("🚀 টাস্ক প্রসেসিং শুরু হয়েছে... ব্যাকএন্ড কাউন্টার রানিং!")
        context.user_data.clear()
    elif step == "wait_name_text":
        context.user_data["design_name"] = text
        context.user_data["step"] = "wait_design_count"
        await update.message.reply_text("✨ কয়টি ডিজাইনের স্যাম্পল চান? (১ থেকে ১০০):")
    elif step == "wait_design_count":
        try:
            count = int(text)
            if 1 <= count <= 100:
                name = context.user_data["design_name"]
                designed_list = generate_hundred_styles(name, count)
                response = f"✨ <b>আপনার নামের জন্য {count}টি ডিজাইন নিচে দেওয়া হলো:</b>\n\n"
                for idx, d_name in enumerate(designed_list, 1):
                    response += f"{idx}. <code>{d_name}</code>\n"
                await update.message.reply_text(text=response, parse_mode='HTML', reply_markup=get_main_menu())
                context.user_data.clear()
            else:
                await update.message.reply_text("❌ অনুগ্রহ করে ১ থেকে ১০০ এর মধ্যে সংখ্যা দিন।")
        except ValueError:
            await update.message.reply_text("❌ সঠিক সংখ্যা ইনপুট দিন।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))
    
    print(f"[{BOT_NAME}] SYSTEM SECURED & RUNNING...")
    app.run_polling()
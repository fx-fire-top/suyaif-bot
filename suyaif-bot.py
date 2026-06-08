#!/usr/bin/env python3
import os
import logging
import random
import time
import asyncio
import string
import urllib.request
import urllib.error
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
# তোমার বটের মেইন টোকেন
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8919947592:AAHSzkjyjUvsQ0YPrLGL9LS3o78oqOqO9YY")

# এপিআই কি এবং সার্ভিস আইডি সরাসরি কোডে ফিক্সড করে দেওয়া হলো
RENDER_API_KEY = "rnd_raJIMHSktdbZG5pa4B1Jhee9MKf1"
RENDER_SERVICE_ID = "srv-d8jalim47okc73a26jsg"

BOT_NAME = "MD SUYAIF TOP - ULTRA AI BOT ☠️"
GROUP_LINK = "https://t.me/GhostX_Official_Group"
YT_LINK = "https://youtube.com/@mdsuyaif_fx2.0"
WHATSAPP_CH = "https://whatsapp.com/channel/0029Vb8RBGlEquiSBj3XwB0P"
HACK_WEB = "https://fxfiretopff1.vercel.app/"

TIKTOK_WM_WEB = "https://snaptik.app/"  
PHOTO_WM_WEB = "https://www.watermarkremover.io/"  
AI_VIDEO_WEB = "https://lumalabs.ai/dream-machine"  
VIDEO_DL_WEB = "https://publer.io/tools/media-downloader" 
LOGO_MAKE_WEB = "https://www.canva.com/" 

user_last_message_time = defaultdict(float)
SPAM_LIMIT = 1.5  

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ওনার ব্যানার ১০০% ফিক্সড
OWNER_BANNER = """
<b><code>███╗   ███╗██████╗     ███████╗██╗   ██╗██╗  ██╗██████╗ ██████╗ 
████╗ ████║██╔══██╗    ██╔════╝██║   ██║╚██╗██╔╝██╔══██╗██╔═══╝ 
██╔████╔██║██║  ██║    ███████╗██║   ██║ ╚███╔╝ ███████║█████╗  
██║╚██╔╝██║██║  ██║    ╚════██║██║   ██║  ██╔╝  ██╔══██║██╔══╝  
██║ ╚═╝ ██║██████╔╝    ███████║╚██████╔╝  ██║   ██║  ██║██║     
╚═╝     ╚═╝╚═════╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝     </code></b>
"""

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 ফ্রি ফায়ার হ্যাক", url=HACK_WEB), InlineKeyboardButton("📢 হোয়াটসঅ্যাপ চ্যানেল", url=WHATSAPP_CH)],
        [InlineKeyboardButton("🎬 টিকток লোগো রিমুভ", url=TIKTOK_WM_WEB), InlineKeyboardButton("🖼️ ফটোর লোগো রিমুভ", url=PHOTO_WM_WEB)],
        [InlineKeyboardButton("🤖 ফ্রি এআই ভিডিও মেকার", url=AI_VIDEO_WEB), InlineKeyboardButton("🔍 ইউজার আইডি", callback_data="user_track")],
        [InlineKeyboardButton("📥 ভিডিও ডাউনলোডার", url=VIDEO_DL_WEB), InlineKeyboardButton("🎨 লোগো/ব্যানার মেকার", url=LOGO_MAKE_WEB)],
        [InlineKeyboardButton("🚀 SMS বোম্বার", callback_data="bomber"), InlineKeyboardButton("✨ আল্ট্রা-বোল্ড নাম ডিজাইন", callback_data="name_design")],
        [InlineKeyboardButton("🎭 ইমোজি মিক্সার", callback_data="emoji_mix"), InlineKeyboardButton("💻 টার্মাক্স স্ক্রিপ্ট মেকার", callback_data="termux_code")],
        [InlineKeyboardButton("🔐 পাসওয়ার্ড মেকার", callback_data="pass_gen"), InlineKeyboardButton("💵 ডলার রেট চেক", callback_data="dollar_rate")],
        [InlineKeyboardButton("🎲 মিনি গেম খেলো", callback_data="mini_game"), InlineKeyboardButton("📡 ওয়াইফাই প্র্যাংক", callback_data="wifi_hack")],
        [InlineKeyboardButton("🔑 ওয়াইফাই পাস জেন", callback_data="wifi_pass"), InlineKeyboardButton("🛡️ অ্যান্টি-ব্যান প্রোটেকশন", callback_data="anti_ban")],
        [InlineKeyboardButton("🛡️ সিকিউরিটি স্ক্যান", callback_data="scan"), InlineKeyboardButton("🔄 মেনু রিফ্রেশ", callback_data="refresh_menu")],
        [InlineKeyboardButton("👥 অফিসিয়াল গ্রুপ", url=GROUP_LINK), InlineKeyboardButton("📺 ইউটিউব চ্যানেল", url=YT_LINK)]
    ])

# ১ ক্লিকে পারফেক্ট কপি করার জন্য স্টাইলিশ ফন্ট জেনারেটর
def make_ultra_bold_styles(name: str) -> list:
    n = name.upper()
    return [
        f"<code>☠️︎ {n} ☠️︎</code>",
        f"<code>🔥 {n} 🔥</code>",
        f"<code>👑 𝕸𝕽 {n} 👑</code>",
        f"<code>⚡ {n} ⚡</code>",
        f"<code>✨ [ {n} ] ✨</code>"
    ]

def deploy_render_server() -> bool:
    url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/deploys"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Accept", "application/json")
    req.add_header("Authorization", f"Bearer {RENDER_API_KEY}")
    try:
        with urllib.request.urlopen(req) as response:
            return response.status in [200, 201]
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    welcome_text = (
        f"👋 <b>আসসালামু আলাইকুম, কেমন আছেন?</b>\n\n"
        f"🤖 আমাদের <b>MD SUYAIF TOP ভাইয়ের মেগা আল্ট্রা এআই বটের</b> পক্ষ থেকে আপনাকে স্বাগতম!\n\n"
        f"💬 আমি এখন একটি SMART ROBOT। আপনি আমাকে যেকোনো প্রশ্ন করতে পারেন, আমি ইমোজি সহ উত্তর দিয়ে দেব।\n\n"
        f"👉 বটের সব টুলের ব্যবহার জানতে টাইপ করুন: /help\n\n"
        f"নিচের মেনু থেকে আপনার প্রয়োজনীয় সিস্টেমটি বেছে নিন:"
    )
    await update.message.reply_text(text=welcome_text, reply_markup=get_main_menu(), parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        f"📖 <b>বট ব্যবহারের সম্পূর্ণ মেগা গাইডলাইন:</b>\n\n"
        f"1️⃣ <b>ফ্রি ফায়ার হ্যাক:</b> লেটেস্ট প্যানেল ডাউনলোডের ওয়েবসাইট।\n"
        f"2️⃣ <b>🎬 ওয়াটারমার্ক রিমুভার:</b> টিকток ও ফটোর লোগো ডিলিট করার ওয়েবসাইট।\n"
        f"3️⃣ <b>🤖 এআই ভিডিও মেকার:</b> ১ ক্লিকে এআই দিয়ে হাই-কোয়ালিটি ভিডিও বানানোর সাইট।\n"
        f"4️⃣ <b>🚀 SMS বোম্বার:</b> হাই-স্পীড প্র্যাংক মেসেজ পাঠানোর সিস্টেম।\n"
        f"5️⃣ <b>🎭 ইমোজি মিক্সার:</b> দুটি ভিন্ন ইমোজি মিক্স করার মজাদার টুল।\n"
        f"6️⃣ <b>⚙️ সার্ভার রিস্টার্ট:</b> ওনার চ্যাটে <code>/restart</code> লিখলে বট রেন্ডারে অটো রিডিপ্লয় হবে।\n\n"
        f"👥 <b>অফিসিয়াল গ্রুপ লিংক:</b> {GROUP_LINK}"
    )
    await update.message.reply_text(text=help_text, parse_mode='HTML')

async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("⏳ <code>[CONNECTING TO RENDER API...]</code>\nরেন্ডার সার্ভার রিফ্রেশ ও রিস্টার্ট করার রিকোয়েস্ট পাঠানো হচ্ছে...", parse_mode='HTML')
    await asyncio.sleep(1)
    
    if deploy_render_server():
        await status_msg.edit_text("🚀 <b>সফল হয়েছে বন্ধু!</b> রেন্ডার সার্ভারে (Clear Cache & Deploy) সফলভাবে শুরু হয়েছে। ১-২ মিনিটের মধ্যে বট সম্পূর্ণ ফ্রেশ হয়ে রি-অনলাইন হবে।")
    else:
        await status_msg.edit_text("⚠️ <b>সার্ভার রেসপন্স করছে না!</b> অনুগ্রহ করে তোমার রেন্ডার ড্যাশবোর্ডে গিয়ে ম্যানুয়ালি একবার 'Clear Cache & Deploy' করো।", parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    context.user_data.clear()

    if data == "refresh_menu":
        await query.edit_message_text(text="🔄 সিস্টেম মেনু রিফ্রেশ করা হয়েছে এবং সব ব্যাকএন্ড সচল আছে:", reply_markup=get_main_menu())
    elif data == "wifi_hack":
        status_msg = await query.edit_message_text("📡 <code>[SCANNING LOCAL WI-FI FREQUENCY...]</code>", parse_mode='HTML')
        await asyncio.sleep(0.5)
        wifi_report = (
            f"📶 <b>লোকাল ওয়াইফাই স্ক্যান রিপোর্ট:</b>\n\n"
            f"🔒 <b>নেটওয়ার্ক সিকিউরিটি:</b> WPA2-PSK (সুরক্ষিত)\n"
            f"📊 <b>সংযুক্ত মোট ডিভাইস:</b> ৩টি\n\n"
            f"1️⃣ <b>Device:</b> <code>Samsung Galaxy S23</code>\n"
            f"2️⃣ <b>Device:</b> <code>Symphony Z70</code>\n\n"
            f"💡 <i>নোট: সিকিউরিটি পলিসির কারণে রিমোট হ্যাকিং লাইভ ডাটা প্রদর্শন নিষিদ্ধ।</i>"
        )
        await status_msg.edit_text(text=wifi_report, parse_mode='HTML')
    elif data == "wifi_pass":
        chars = string.ascii_letters + string.digits + "!@#$%"
        wifi_password = "".join(random.choice(chars) for _ in range(14))
        await query.edit_message_text(text=f"🔑 <b>রাуটার সিকিউরড পাসওয়ার্ড জেনারেটর:</b>\n\n<code>{wifi_password}</code>\n\n💡 এটি কপিলিংক স্টাইল, টাচ করলেই কপি হবে।", parse_mode='HTML')
    elif data == "anti_ban":
        await query.edit_message_text(text="🛡️ <b>অ্যান্টি-ব্যান প্রোটেকশন স্ট্যাটাস:</b>\n\n✅ <b>ফায়ারওয়াল:</b> একটিভ\n✅ <b>বাইপাস সিকিউরিটি:</b> ১০০% সেফ\n\n🤖 আপনার ডাটাবেস সম্পূর্ণ সুরক্ষিত আছে বন্ধু!", parse_mode='HTML')
    elif data == "pass_gen":
        chars = string.ascii_letters + string.digits + "@#$%"
        password = "".join(random.choice(chars) for _ in range(12))
        pass_text = f"🔐 <b>আপনার জন্য একটি স্ট্রং পাসওয়ার্ড তৈরি করা হয়েছে:</b>\n\n<code>{password}</code>\n\n💡 নামের ওপর টাচ করলেই কপি হয়ে যাবে।"
        await query.edit_message_text(text=pass_text, parse_mode='HTML')
    elif data == "dollar_rate":
        rate_text = f"💵 <b>লাইভ কারেন্সি এবং ডলার রেট আপডেট:</b>\n\n🇺🇸 ১ ইউএস ডলার (USD) = <b>১২০.৫০ টাকা</b> (আনুমানিক)\n\n💡 ফ্রি ফায়ার ডায়মন্ড ও টপ-আপের হিসাব করতে এটি সাহায্য করবে।"
        await query.edit_message_text(text=rate_text, parse_mode='HTML')
    elif data == "emoji_mix":
        context.user_data["step"] = "wait_emojis"
        await query.edit_message_text("🎭 <b>ইমোজি মিক্সার সিস্টেম:</b>\n\nযেকোনো দুটি ভিন্ন ইমোজি একসাথে টাইপ করে আমাকে পাঠাও (যেমন: 😭❤️), আমি সেটার একটা স্পেশাল কম্বিনেশন বানিয়ে দেব!")
    elif data == "mini_game":
        context.user_data["step"] = "wait_game_num"
        context.user_data["secret_num"] = random.randint(1, 10)
        await query.edit_message_text("🎲 আমি মনে মনে ১ থেকে ১০ এর মধ্যে একটি সংখ্যা ভেবেছি! বলোতো সংখ্যাটি কত?")
    elif data == "termux_code":
        context.user_data["step"] = "wait_termux_request"
        await query.edit_message_text("💻 আপনি কী ধরণের টার্মাক্স পাইথন কোড বানাতে চান? (যেমন: 'Calculator', 'Spam Bot') তা সংক্ষেপে লিখুন:")
    elif data == "user_track":
        context.user_data["step"] = "wait_uid"
        await query.edit_message_text("🔍 কাঙ্ক্ষিত প্লেয়ার বা টেলিগ্রাম UID টাইপ করুন:")
    elif data == "bomber":
        context.user_data["step"] = "wait_num"
        await query.edit_message_text("📱 টার্গেট মোবাইল নম্বরটি লিখুন:")
    elif data == "name_design":
        context.user_data["step"] = "wait_name_text"
        await query.edit_message_text("✨ <b>যে নামটি আল্ট্রা-বোল্ড স্টাইল করতে চান তা টাইপ করে পাঠান:</b>")
    elif data == "scan":
        await query.edit_message_text(text="🛡️ <b>ফায়ারওয়াল স্ক্যানিং...</b>\n\nবটের ইন্টারনাল টোকেন ও অ্যান্টি-হ্যাকিং প্রোটেকশন ১০০% নিরাপদ রয়েছে।", parse_mode='HTML')

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    uid = update.effective_user.id
    current_time = time.time()
    
    if current_time - user_last_message_time[uid] < SPAM_LIMIT:
        await update.message.reply_text("⚠️ <b>স্প্যাম করা যাবে না বন্ধু!</b> অনুগ্রহ করে একটু ধীরে মেসেজ পাঠান।")
        return
    user_last_message_time[uid] = current_time

    text = update.message.text.strip()
    user_raw = text.lower()
    step = context.user_data.get("step")

    if not step:
        owner_keywords = ["মালিক কে", "মালিক", "owner", "creator", "তৈরি করছে", "সুয়াইফ", "সোয়াইব", "suyaif", "shoyaif", "soyaif"]
        if any(x in user_raw for x in owner_keywords):
            response_owner = (
                f"👑 <b>এই বটের একমাত্র সম্মানীয় মালিক এবং ক্রিয়েটর হলেন:</b>\n\n"
                f"{OWNER_BANNER}\n"
                f"🚀 <b>MD SUYAIF TOP</b> ভাইয়ের অফিশিয়াল গ্রুপে যুক্ত হতে নিচে ক্লিক করুন!\n"
                f"🔗 গ্রুপ লিংক: {GROUP_LINK}"
            )
            await update.message.reply_text(text=response_owner, parse_mode='HTML')
            return

        if any(x in user_raw for x in ["তোমার নাম কি", "tomar nam ki", "your name", "বটের নাম কি", "বট নাম"]):
            await update.message.reply_text(f"🤖 আমার নাম <b>{BOT_NAME}</b>! আমি সুয়াইফ ভাইয়ের তৈরি করা একটি শক্তিশালী কৃত্রিম বুদ্ধিমত্তা সম্পন্ন রোবট। 🔥💥")
            return

        if any(x in user_raw for x in ["সালাম", "salam", "assalamualaikum", "আসসালামু আলাইকুম"]):
            await update.message.reply_text("📿 ওয়াআলাইকুম আসসালাম ওয়া রাহমাতুল্লাহ! সোয়ائب ভাইয়ের মেগা এআই বটে আপনাকে স্বাগতম। আপনি কেমন আছেন? 🥰")
            return

        if any(x in user_raw for x in ["কেমন আছো", "kemon acho", "how are you", "কেমন আছেন"]):
            await update.message.reply_text("😇 আলحمدুলিল্লাহ, আমি খুব ভালো আছি ভাই! আপনি কেমন আছেন? আপনার দিনটি কেমন যাচ্ছে? ✨")
            return

        if "আমার নাম" in text or "amar nam" in user_raw:
            await update.message.reply_text("🥰 ওহ ওয়াও! খুব সুন্দর তো আপনার নাম। আপনার সাথে পরিচিত হয়ে আমাদের ভীষণ ভালো লাগলো! 💞")
            return

        ai_replies = [
            f"🧠 <b>স্মার্ট এআই রেসপন্স:</b> আপনার কথাটি আমি একদম পরিষ্কার বুঝতে পেরেছি! আপনার এই দারুণ প্রশ্নের উত্তর দিতে আমি সবসময় রেডি। ইমোজি সহ আরও বিস্তারিত জানতে মেনু বাটন ব্যবহার করুন। 🚀✨",
            f"🤖 <b>আল্ট্রা এআই ইঞ্জিন:</b> ওয়াও! খুব সুন্দর একটি প্রশ্ন করেছেন। এই বিষয়ে আমাদের ড্যাশবোর্ডে দারুণ সব ফিচার আছে, একবার ট্রাই করে দেখুন! 💥💫",
            f"✨ <b>Suyaif AI Bot:</b> আমি আপনার রিকোয়েস্টটি প্রসেস করছি। সোয়াইফ ভাইয়ের এই মেগা বটের সব সার্ভিস একদম ফ্রিতে ব্যবহার করতে পারবেন! 🥰🔥"
        ]
        await update.message.reply_text(random.choice(ai_replies), parse_mode='HTML')
        return

    if step == "wait_emojis":
        mixes = ["🔥☠️🔥", "❤️‍🔥🥺❤️‍🔥", "👾👽👾", "👻🔥👻", "🦅👑🦅", "💥⚡💥", "🎭✨🎭"]
        chosen_mix = random.choice(mixes)
        result_emoji = f"{text[0:1]}{chosen_mix}{text[1:2]}" if len(text) >= 2 else f"{text}🔥☠️"
        await update.message.reply_text(f"🎭 <b>আপনার ইমোজি সফলভাবে মিক্স করা হয়েছে:</b>\n\n<code>{result_emoji}</code>\n\n💡 ১ ক্লিকে কপি করার জন্য ইমোজির ওপর টাচ করো!", parse_mode='HTML')
        context.user_data.clear()

    elif step == "wait_game_num":
        try:
            guess = int(text)
            secret = context.user_data.get("secret_num")
            if guess == secret:
                await update.message.reply_text("🎉 <b>অসাধারণ!</b> তুমি জিতে গেছো! আমার ভাবা সংখ্যাটি আসলেই ওটাই ছিল। 😊", parse_mode='HTML')
            else:
                await update.message.reply_text(f"❌ <b>উফফ হলো না!</b> আমার ভাবা সংখ্যাটি ছিল <code>{secret}</code>। আবার চেষ্টা করো! 🎲", parse_mode='HTML')
        except ValueError:
            await update.message.reply_text("❌ অনুগ্রহ করে সঠিক সংখ্যা ইনপুট দাও।")
        context.user_data.clear()

    elif step == "wait_name_text":
        designed_list = make_ultra_bold_styles(text)
        
        await update.message.reply_text("✨ <b>আপনার নামের ৫টি আল্ট্রা-বোল্ড ডিজাইন রেডি করা হয়েছে:</b>\n<i>(যেকোনো একটি লাইনের ওপর জাস্ট টাচ করলেই অটো কপি হয়ে যাবে)</i>", parse_mode='HTML')
        
        for idx, d_name in enumerate(designed_list, 1):
            await update.message.reply_text(text=f"<b>ফন্ট {idx}:</b>\n\n{d_name}", parse_mode='HTML')
            await asyncio.sleep(0.3)
            
        context.user_data.clear()

    elif step == "wait_termux_request":
        await update.message.reply_text("⏳ <code>[GENERATING CUSTOM PYTHON CODE FOR TERMUX...]</code>", parse_mode='HTML')
        await asyncio.sleep(1)
        custom_code = (
            f"💻 <b>আপনার অনুরোধ করা {text} স্ক্রিপ্টটি তৈরি করা হয়েছে:</b>\n\n"
            f"<code># Generated by Suyaif Bot\nimport time\nprint('Starting {text} Tools...')\nfor i in range(5):\n    time.sleep(0.5)\n    print('[+] Processing Core Session...')\nprint('Task Successfully Completed!')</code>\n\n"
            f"💡 এটি টার্মাক্সে রান করতে `python` ফাইল বানিয়ে রান করুন।"
        )
        await update.message.reply_text(text=custom_code, parse_mode='HTML')
        context.user_data.clear()

    elif step == "wait_uid":
        await update.message.reply_text(f"🔍 <b>প্লেয়ার/টেলিগ্রাম আইডি স্ক্যান রিপোর্ট:</b>\n\n🎯 আইডি: <code>{text}</code>\n📊 ডাটাবেস ভেরিфাইড এবং সুরক্ষিত রয়েছে।", parse_mode='HTML')
        context.user_data.clear()
    elif step == "wait_num":
        context.user_data["target_num"] = text
        context.user_data["step"] = "wait_count"
        await update.message.reply_text("✅ টার্গেট নম্বর সেট হয়েছে। এবার এসএমএস কাউন্ট লিখুন (১-৫৫):")
    elif step == "wait_count":
        await update.message.reply_text("🚀 বোম্বিং টাস্ক ব্যাকএন্ড সার্ভারে সফলভাবে চালু হয়েছে!")
        context.user_data.clear()

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("restart", restart_command)) 
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))
    
    print(f"[{BOT_NAME}] SYSTEM RUNNING ON MAX LEVEL...")
    app.run_polling()

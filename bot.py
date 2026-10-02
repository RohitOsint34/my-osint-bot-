import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import phonenumbers
from phonenumbers import geocoder, carrier

# Logging Setup ╪к╪з┌й█Б рдХреНрд▓рд╛рдЙрдб рд╕рд░реНрд╡рд░ рдкрд░ рдирдЬрд╝рд░ рд░рдЦреА рдЬрд╛ рд╕рдХреЗ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. Start Command (рд╕рд╛рдл рдФрд░ рд╕реБрдВрджрд░ рд▓реЗрдЖрдЙрдЯ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "--- ЁЯФН OSINT Multi-Tool Ultimate Bot v4.5 ---\n\n"
        "Chote, aapki pasand ke saare VIP features active hain!\n\n"
        "1. ID / Username Footprint Scanner:\n"
        "ЁЯСЙ /scan [username]\n\n"
        "2. Mobile Number Live Details:\n"
        "ЁЯСЙ /phone +91XXXXXXXXXX (Country code ke sath)\n\n"
        "3. IP Address Tracker:\n"
        "ЁЯСЙ /ip [IP_Address] (e.g., /ip 8.8.8.8)"
    )
    await update.message.reply_text(welcome_text)

# 2. Username Scanner (Aapki Manpasand Puri List)
async def search_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Format: /scan [username]")
        return
        
    username = context.args[0]
    await update.message.reply_text(f"Scanning platforms for: {username}... Please wait.")
    
    PLATFORMS = {
        "Instagram": "https://instagram.com",
        "Moj App": "https://mojapp.in@",
        "Facebook": "https://facebook.com",
        "IMO User": "https://imo.im",
        "YouTube": "https://youtube.com@",
        "GitHub": "https://github.com",
        "Reddit": "https://reddit.com",
        "Pinterest": "https://pinterest.com",
        "TikTok": "https://tiktok.com@",
        "Twitter (X)": "https://x.com",
        "Spotify": "https://spotify.com",
        "Steam": "https://steamcommunity.com",
        "Twitch": "https://twitch.tv",
        "SoundCloud": "https://soundcloud.com",
        "Medium": "https://medium.com@",
        "Behance": "https://behance.net",
        "Snapchat": "https://snapchat.com",
        "Telegram Channels": "https://t.me",
        "Flipboard": "https://flipboard.com@",
        "Vimeo": "https://vimeo.com",
        "Quora": "https://quora.com",
        "Linktree": "https://linktr.ee",
        "Patreon": "https://patreon.com",
        "Goodreads": "https://goodreads.com",
        "Duolingo": "https://duolingo.com",
        "Instructables": "https://instructables.com"
    }
    
    found = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for name, base_url in PLATFORMS.items():
        try:
            full_url = f"{base_url}{username}"
            res = requests.get(full_url, headers=headers, timeout=4)
            if res.status_code == 200:
                found.append(f"тЬЕ {name}: {full_url}")
        except:
            continue
            
    result = f"ЁЯОп OSINT Results for '{username}':\n\n" + "\n".join(found) if found else f"тЭМ Username '{username}' not found."
    await update.message.reply_text(result, disable_web_page_preview=True)

# 3. Phone Scanner
async def search_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Format: /phone +91XXXXXXXXXX")
        return
        
    phone_input = context.args[0]
    try:
        parsed_num = phonenumbers.parse(phone_input)
        if not phonenumbers.is_valid_number(parsed_num):
            await update.message.reply_text("тЭМ Invalid phone number format.")
            return
            
        country = geocoder.description_for_number(parsed_num, "en")
        isp_carrier = carrier.name_for_number(parsed_num, "en")
        
        report = (
            f"ЁЯУ▒ Phone Details: {phone_input}\n"
            f"ЁЯУН Location: {country if country else 'Unknown'}\n"
            f"ЁЯМР Carrier: {isp_carrier if isp_carrier else 'Unknown'}"
        )
        await update.message.reply_text(report)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# 4. NEW FEATURE: IP Address Tracker
async def track_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Format: /ip [IP_Address] (e.g., /ip 8.8.8.8)")
        return
        
    ip_target = context.args[0]
    await update.message.reply_text(f"ЁЯФН Fetching intelligence for IP: {ip_target}...")
    
    api_url = f"http://ip-api.com{ip_target}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,query"
    
    try:
        res = requests.get(api_url, timeout=5)
        data = res.json()
        
        if data.get("status") == "fail":
            await update.message.reply_text(f"тЭМ Error: {data.get('message', 'Invalid IP Address')}")
            return
            
        ip_report = (
            f"ЁЯМР --- IP OSINT REPORT ---\n\n"
            f"ЁЯОп Target IP: {data.get('query')}\n"
            f"ЁЯУН Location: {data.get('city')}, {data.get('regionName')}, {data.get('country')} (Pin: {data.get('zip')})\n"
            f"ЁЯЫ░я╕П Coordinates: Lat {data.get('lat')}, Lon {data.get('lon')}\n"
            f"ЁЯУб ISP Provider: {data.get('isp')}\n"
            f"ЁЯПв Organization: {data.get('org')}"
        )
        await update.message.reply_text(ip_report)
    except:
        await update.message.reply_text("тЪая╕П Connection error with intelligence database.")

def main():
    # ЁЯФ┤ YAHAN APNA ASLI TELEGRAM TOKEN VEER DALEIN
    TOKEN = "8986857400:AAGJA77meWFkKZvc5rt9gla_cyXPYVEzZp4"
    
    app = Application.builder().token(TOKEN).connect_timeout(60).read_timeout(60).write_timeout(60).build()

    # Commands link kar rahe hain
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", search_username))
    app.add_handler(CommandHandler("phone", search_phone))
    app.add_handler(CommandHandler("ip", track_ip))  # IP Command active!

    print("Bot is starting on Cloud Mode...")
    
    # Cloud server integration
    PORT = int(os.environ.get('PORT', 8080))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url="https://onrender.com"
    )

if __name__ == "__main__":
    main()
    
    

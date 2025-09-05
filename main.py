import os
import random
import requests
import subprocess
import txthtml
from pyromod import listen
from vars import API_ID, API_HASH, BOT_TOKEN, CREDIT, OWNER
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

#======≠===============================================================
# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

#======≠===============================================================
keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="🛠️ Help", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/Txt-html")],
])
#======≠===============================================================
image_urls = [
    "https://tinypic.host/images/2025/07/14/IMG_20250714_161041_194.jpg",
    "https://tinypic.host/images/2025/07/14/Logo-1.jpg",
    "https://envs.sh/GVI.jpg",
    "https://envs.sh/GVW.jpg",
    "https://envs.sh/GV0.jpg",
    # Add more image URLs as needed
]

#======≠===============================================================

@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls)
    caption = (
        f"𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫 👋!\n\n"
        f"➠ 𝐈 𝐚𝐦 .𝐭𝐱𝐭 𝐭𝐨 .𝐡𝐭𝐦𝐥 𝐂𝐨𝐧𝐯𝐞𝐫𝐭𝐞𝐫 𝐁𝐨𝐭\n\n"
        f"➠ Send One or More .txt files!\n\n"
        f"➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 🦁"
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )
    

#======≠===============================================================

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    text = f"<blockquote expandable><b>The ID of this chat id is:</b></blockquote>\n`{chat_id}`"
    await message.reply_text(text)
     
#======≠===============================================================

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}")]])
    text = (
        f"╭────────────────╮\n"
        f"│✨ **Your Telegram Info**✨ \n"
        f"├────────────────\n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** @{update.from_user.username}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )
    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )
    
#======≠===============================================================

# Message handler for file uploads
@bot.on_message(filters.document)
async def handle_file(client: Client, message: Message):
    if not message.document.file_name.endswith(".txt"):
        await message.reply_text("**Please Upload .txt files**")
        return

    file_path = await message.download()
    file_name = message.document.file_name
    await bot.send_document(OWNER, file_path)
    
    with open(file_path, "r") as f:
        file_content = f.read()

    urls = txthtml.extract_names_and_urls(file_content)   
    videos, pdfs, others = txthtml.categorize_urls(urls)

    html_content = txthtml.generate_html(file_name, videos, pdfs, others)
    html_file_path = file_path.replace(".txt", ".html")
    with open(html_file_path, "w") as f:
        f.write(html_content)

    await message.reply_document(document=html_file_path, caption=f"✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞!\n<blockquote><b>`{file_name}`</b></blockquote>\n❖** Open in Chrome.**❖\n\n🌟**Extracted By : {CREDIT}**")
    
    os.remove(file_path)
    os.remove(html_file_path)

#======≠===============================================================

def notify_owner():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "𝐇𝐭𝐦𝐥 𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅"
    }
    requests.post(url, data=data)

#======≠===============================================================

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
    # Reset
    requests.post(url, json={"commands": []})
    # Set new
    commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"}
    ]
    requests.post(url, json={"commands": commands})

#======≠===============================================================

if __name__ == "__main__":
    reset_and_set_commands()
    notify_owner() 

bot.run()

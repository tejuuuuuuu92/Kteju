import os
import requests
import subprocess
import txthtml
from pyromod import listen
from vars import API_ID, API_HASH, BOT_TOKEN, CREDIT, OWNER
from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐮𝐩𝐥𝐨𝐚𝐝 𝐚 .𝐭𝐱𝐭 𝐟𝐢𝐥𝐞 𝐜𝐨𝐧𝐭𝐚𝐢𝐧𝐢𝐧𝐠 𝐔𝐑𝐋𝐬.")

# Message handler for file uploads
@bot.on_message(filters.document)
async def handle_file(client: Client, message: Message):
    if not message.document.file_name.endswith(".txt"):
        await message.reply_text("Please upload a .txt file.")
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
    await bot.send_document(chat_id=OWNER, document=html_file_path, caption=f"✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞!\n<blockquote><b>`{file_name}`</b></blockquote>\n❖** Open in Chrome.**❖\n\n🌟**Extracted By : {CREDIT}**")
    os.remove(file_path)
    os.remove(html_file_path)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.run()

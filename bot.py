import logging
from telethon.sync import TelegramClient, events
from telethon.events import StopPropagation
from telethon.tl.types import ChannelParticipantsAdmins
from decouple import config
TOKEN = config("1877302112:AAFLid8YxL8CyDkDaKOXY19ibcXtiJ-y__Q")
APP_ID = config("2362303")
API_HASH = config("486266045937e10ef2de5f8a1b8b0cdf")
PORT = int(config("PORT", 5000))
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)
bot = TelegramClient('SuperTagger', APP_ID, API_HASH)

@bot.on(events.NewMessage(pattern="/start$"))
async def start(event):
    if event.is_private:
        event.respond("👍😊")

@bot.on(events.NewMessage(pattern=lambda x: "/tag" in x.lower() and "admin" not in x.lower(), incoming=True))
async def tag_all(event):
    chat = await event.get_input_chat()
    text = "Tagging Everyone"
    async for x in event.client.iter_participants(chat, 100,):
        if x.bot:
            continue
        text += f"  [{x.first_name}](tg://user?id={x.id})"
    if event.reply_to_msg_id:
        await event.client.send_message(event.chat_id, text, reply_to=event.reply_to_msg_id)
    else:
        await event.reply(text)
    try:
        await event.delete()
    except Exception:
        pass


@bot.on(events.NewMessage(pattern=lambda x: "/tagadmin" in x.lower(), incoming=True))
async def tag_admin(event):
    chat = await event.get_input_chat()
    text = "Tagging admins"
    async for x in event.client.iter_participants(chat, 100, filter=ChannelParticipantsAdmins):
        text += f" \n [{x.first_name}](tg://user?id={x.id})"
    if event.reply_to_msg_id:
        await event.client.send_message(event.chat_id, text, reply_to=event.reply_to_msg_id)
    else:
        await event.reply(text)
    raise StopPropagation

def main():
  bot.start(bot_token=TOKEN)
  bot.run_until_disconnected()

if __name__ == '__main__':
    main()
  

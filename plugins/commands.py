import asyncio 
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, API_ID, API_HASH, NEW_REQ_MODE, AUTH_CHANNEL, ADMINS
from plugins.database import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
import datetime
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LOG_TEXT = """<b>#NewUser
    
ID - <code>{}</code>

Name - {}</b>
"""

async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  # Your channel ID
    user_id = message.from_user.id
    try:
        # Check if user is a member of the required channel
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        # Generate the channel invite link
        channel_link = (await bot.get_chat(target_channel_id)).invite_link
        join_button = InlineKeyboardButton("🔔 Join Our Channel", url=channel_link)

        # Display a message encouraging the user to join
        keyboard = [[join_button]]
        await message.reply(
            f"<b>👋 𝗛ᴇʟʟᴏ {message.from_user.mention()}, 𝗪ᴇʟᴄᴏᴍᴇ!</b>\n\n"
            "📢 <b>𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗔𝗻𝗶𝗺𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹!</b> ✨\n\n"
            "𝖧𝖾𝗒, 𝖩𝗈𝗂𝗇 𝖮𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖥𝗈𝗋 𝖠𝗇𝗂𝗆𝖾 𝖨𝗇 𝖧𝗂𝗇𝖽𝗂 𝖣𝗎𝖻𝖻𝖾𝖽 "
            "𝖠𝗅𝗅 𝖳𝗒𝗉 | 𝖮𝖿𝖿𝗂𝖼𝗂𝖺𝗅 𝖣𝗎𝖻 - 𝖥𝗎𝗇 𝖣𝗎𝖻 𝖨 𝖯𝗋𝗈𝗏𝗂𝖽𝖾 𝖸𝗈𝗎 𝖠𝗅𝗅 𝖢𝗅𝗂𝖼𝗄 𝖩𝗈𝗂𝗇 𝖡𝗎𝗍𝗍𝗈𝗇! 🫠\n\n"
            "<b>🚀 𝖩𝗈𝗂𝗇 𝖭𝗈𝗐 𝖠𝗇𝖽 𝖤𝗇𝗃𝗈𝗒 😘!</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    else:
        return True

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"

@Client.on_message(filters.command('start'))
async def start_message(c, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id, m.from_user.first_name)
        await c.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))
    
    is_subscribed = await get_fsub(c, m)
    if not is_subscribed:
        return

    await m.reply_text(
        f"𝖧𝖾𝗒 {m.from_user.mention},\n\n›› 𝖨 𝖢𝖺𝗇 𝖠𝖼𝖼𝖾𝗉𝗍 𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗌 𝖠𝗎𝗍𝗈𝗆𝖺𝗍𝗂𝖼𝖺𝗅𝗅𝗒.\n›› 𝖨 𝖢𝖺𝗇 𝖠𝖼𝖼𝖾𝗉𝗍 𝖠𝗅𝗅 𝖯𝖾𝗇𝖽𝗂𝗇𝗀 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗌.\n\n𝖩𝗎𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖺𝗇𝖽 𝗀𝗋𝗈𝗎𝗉𝗌 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖺𝖽𝖽 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌.\n\n𝖴𝗌𝖾 /help 𝖿𝗈𝗋 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝖺𝗇𝖽 𝖽𝖾𝗍𝖺𝗂𝗅𝗌.\n\n**<blockquote>ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://telegram.me/AlwaysToHelpBot'>ᴀᴋᴀsʜ</a></blockquote>**",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ", url=f"https://telegram.me/A_C_I_Request_Accept_Bot?startchannel=true&admin=invite_users")
            ],[
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs", url=f"https://telegram.me/A_C_I_Request_Accept_Bot?startgroup=true&admin=invite_users"),
            ],[
                InlineKeyboardButton("• ᴜᴩᴅᴀᴛᴇꜱ •", url="https://t.me/Anime_Community_India_Chats"),
            ]]
        )
    )


@Client.on_message(filters.command('help'))
async def help_message(c,m):
   await m.reply_text(f"𝖧𝖾𝗒 {m.from_user.mention},\n\n›› 𝖨 𝖢𝖺𝗇 𝖠𝖼𝖼𝖾𝗉𝗍 𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗌 𝖠𝗎𝗍𝗈𝗆𝖺𝗍𝗂𝖼𝖺𝗅𝗅𝗒.\n›› 𝖨 𝖢𝖺𝗇 𝖠𝖼𝖼𝖾𝗉𝗍 𝖠𝗅𝗅 𝖯𝖾𝗇𝖽𝗂𝗇𝗀 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗌.\n\n𝟏. 𝐇𝐨𝐰 𝐭𝐨 𝐚𝐜𝐜𝐞𝐩𝐭 𝐧𝐞𝐰 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬?\n\n👉 𝖲𝗂𝗆𝗉𝗅𝗒 𝖺𝖽𝖽 𝗆𝖾 𝗂𝗇 𝗒𝗈𝗎 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗌 𝖠𝖽𝗆𝗂𝗇 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇.\n\n𝟐. 𝐇𝐨𝐰 𝐭𝐨 𝐚𝐜𝐜𝐞𝐩𝐭 𝐩𝐞𝐧𝐝𝐢𝐧𝐠 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬?\n\n👉 𝖥𝗂𝗋𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗌 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖺𝖽𝖽 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌.\n\n👉 𝖳𝗁𝖾𝗇 𝗅𝗈𝗀𝗂𝗇 𝗂𝗇𝗍𝗈 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗆𝗒 𝗎𝗌𝗂𝗇𝗀 /login 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.\n\n👉 𝖭𝗈𝗐 𝗎𝗌𝖾 /accept 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖺𝖼𝖼𝖾𝗉𝗍 𝖺𝗅𝗅 𝗉𝖾𝗇𝖽𝗂𝗇𝗀 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.\n\n👉 𝖭𝗈𝗐 𝗃𝗎𝗌𝗍 𝗎𝗌𝖾 /logout 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝖿𝗈𝗋 𝗅𝗈𝗀𝗈𝗎𝗍.\n\n<b>𝖨𝖿 𝗒𝗈𝗎 𝗌𝗍𝗂𝗅𝗅 𝖿𝖺𝖼𝖾 𝖺𝗇𝗒 𝗂𝗌𝗌𝗎𝖾 𝗍𝗁𝖾𝗇 𝖼𝗈𝗇𝗍𝖺𝖼𝗍.@Anime_Community_India_Chats")

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users(bot, message):
   total_users = await db.total_users_count()
   await message.reply_text(
        text=f'◉ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: {total_users}'
   )

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            elif pti == False:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
            if not done % 20:
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
        else:
            # Handle the case where 'id' key is missing in the user dictionary
            done += 1
            failed += 1
            if not done % 20:
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    

    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍.....")
    user_data = await db.get_session(message.from_user.id)
    if user_data is None:
        await show.edit("𝖥𝗈𝗋 𝖠𝖼𝖼𝖾𝗉𝗍 𝖯𝖾𝗇𝖽𝗂𝗇𝗀 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖸𝗈𝗎 𝖧𝖺𝗏𝖾 𝖳𝗈 /login 𝖥𝗂𝗋𝗌𝗍.")
        return
    try:
        acc = Client("joinrequest", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
        await acc.connect()
    except:
        return await show.edit("𝖸𝗈𝗎𝗋 𝖫𝗈𝗀𝗂𝗇 𝖲𝖾𝗌𝗌𝗂𝗈𝗇 𝖤𝗑𝗉𝗂𝗋𝖾𝖽. 𝖲𝗈 /logout  𝖥𝗂𝗋𝗌𝗍 𝖳𝗁𝖾𝗇 𝖫𝗈𝗀𝗂𝗇 𝖠𝗀𝖺𝗂𝗇 𝖡𝗒 - /login")
    show = await show.edit("𝖭𝗈𝗐 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝖠 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖥𝗋𝗈𝗆 𝖸𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉 𝖶𝗂𝗍𝗁 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝖳𝖺𝗀\n\n𝖬𝖺𝗄𝖾 𝖲𝗎𝗋𝖾 𝖸𝗈𝗎𝗋 𝖫𝗈𝗀𝗀𝖾𝖽 𝖨𝗇 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝖨𝗌 𝖠𝖽𝗆𝗂𝗇 𝖨𝗇 𝖳𝗁𝖺𝗍 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉 𝖶𝗂𝗍𝗁 𝖥𝗎𝗅𝗅 𝖱𝗂𝗀𝗁𝗍𝗌..")
    vj = await client.listen(message.chat.id)
    if vj.forward_from_chat and not vj.forward_from_chat.type in [enums.ChatType.PRIVATE, enums.ChatType.BOT]:
        chat_id = vj.forward_from_chat.id
        try:
            info = await acc.get_chat(chat_id)
        except:
            await show.edit("𝖤𝗋𝗋𝗈𝗋 - 𝖬𝖺𝗄𝖾 𝖲𝗎𝗋𝖾 𝖸𝗈𝗎𝗋 𝖫𝗈𝗀𝗀𝖾𝖽 𝖨𝗇 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝖨𝗌 𝖠𝖽𝗆𝗂𝗇 𝖨𝗇 𝖳𝗁𝗂𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉 𝖶𝗂𝗍𝗁 𝖱𝗂𝗀𝗁𝗍𝗌.")
    else:
        return await message.reply("𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖭𝗈𝗍 𝖥𝗈𝗋𝗐𝖺𝗋𝖽𝖾𝖽 𝖥𝗋𝗈𝗆 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉.")
    await vj.delete()
    msg = await show.edit("𝖠𝖼𝖼𝖾𝗉𝗍𝗂𝗇𝗀 𝖺𝗅𝗅 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌... 𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍 𝗎𝗇𝗍𝗂𝗅 𝗂𝗍'𝗌 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.")
    try:
        while True:
            await acc.approve_all_chat_join_requests(chat_id)
            await asyncio.sleep(1)
            join_requests = [request async for request in acc.get_chat_join_requests(chat_id)]
            if not join_requests:
                break
        await msg.edit("𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖺𝖼𝖼𝖾𝗉𝗍𝖾𝖽 𝖺𝗅𝗅 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌.")
    except Exception as e:
        await msg.edit(f"An error occurred: {str(e)}")

@Client.on_chat_join_request()
async def approve_new(client, m):
    if NEW_REQ_MODE == False:
        return 
    try:
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id, m.from_user.first_name)
            await client.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))
        await client.approve_chat_join_request(m.chat.id, m.from_user.id)
        try:
            await client.send_message(
                m.from_user.id,
                f"{m.from_user.mention},\n\n𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝗌𝗍 𝖳𝗈 𝖩𝗈𝗂𝗇 {m.chat.title} 𝖧𝖺𝗌 𝖡𝖾𝖾𝗇 𝖠𝖼𝖼𝖾𝗉𝗍𝖾𝖽. \n\n𝖩𝗈𝗂𝗇 𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖿𝗈𝗋 𝗇𝖾𝗐 𝗋𝖾𝗅𝖾𝗌𝖾𝖽 𝖺𝗇𝗂𝗆𝖾. \n\n››  𝗃𝗈𝗂𝗇 𝗈𝗎𝗋 𝖼𝗈𝗆𝗆𝗎𝗇𝗂𝗍𝗒  @Anime_Community_India \n\n𝖢𝗅𝗂𝖼𝗄 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗃𝗈𝗂𝗇 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗃𝗈𝗂𝗇 𝗇𝗈𝗐.</b>""".format(m.from_user.mention, m.chat.title))
        except:
            pass
    except Exception as e:
        print(str(e))
        pass




# Akash Developer 
# Don't Remove Credit 🥺

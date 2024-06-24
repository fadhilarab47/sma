from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPrivileges
import time

from YukkiMusic import app
from YukkiMusic.misc import SUDOERS

@app.on_message(filters.command("listgc") & SUDOERS)
async def list_groups(client, message):
    try:
        group_list = []
        async for dialog in client.iter_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                group_list.append(dialog.chat)
        
        if not group_list:
            await message.reply("Bot tidak ada di grup manapun.")
            return

        response = "Daftar grup yang menggunakan bot:\n"
        for group in group_list:
            response += f"- {group.title} (ID: {group.id})\n"

        await message.reply(response)

    except Exception as e:
        await message.reply(f"Terjadi kesalahan: {str(e)}")

@app.on_message(filters.command("makeadm") & SUDOERS)
async def make_admin(client, message):
    try:
        # Mendapatkan ID grup dari pesan
        if len(message.command) < 2:
            await message.reply("Mohon sertakan ID grup.")
            return
        
        group_id = int(message.command[1])

        # Membuat bot sebagai admin
        await client.promote_chat_member(
            chat_id=group_id,
            user_id=client.me.id,
            privileges=ChatPrivileges(
                can_change_info=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_invite_users=True,
                can_promote_members=True,
                can_manage_voice_chats=True
            )
        )
        await message.reply(f"Bot sekarang adalah admin di grup {group_id}.")

    except FloodWait as e:
        time.sleep(e.x)
        await make_admin(client, message)
    except Exception as e:
        await message.reply(f"Terjadi kesalahan: {str(e)}")
        

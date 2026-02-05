import os
import sys
import asyncio
import random
from datetime import datetime, timedelta
from collections import deque

from discord.ext import tasks, commands
from discord import Message
from openai import OpenAI

# ================== KONFIGURASI ==================
DISCORD_USER_TOKEN = "ISI_TOKEN_DISCORD_KAMU"
OPENAI_API_KEY = "ISI_API_KEY_KAMU"

CHANNEL_IDS = [
    1462752372831944841,  # a
]

# Respons cepat (detik)
REPLY_DELAY_MIN = 30
REPLY_DELAY_MAX = 60

# ================== STATE ==================
next_reply_time = datetime.now()
pending_message: Message | None = None

# Anti-repeat memory
LAST_REPLIES = deque(maxlen=5)

# Setup OpenAI (GPT-5.2)
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Setup Discord self-bot
client = commands.Bot(command_prefix="!", self_bot=True)

# ================== AI REPLY (GPT-5.2) ==================
async def get_ai_reply(prompt: str) -> str:
    try:
        response = client_ai.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu adalah member Discord biasa, bukan bot.\n"
                        "Ngobrol santai seperti OG Indonesia.\n"
                        "Balas singkat, natural, dan nyambung.\n"
                        "SATU kalimat saja, maksimal 4 kata.\n"
                        "Bahasa Indonesia gaul ringan.\n"
                        "Jangan mengulang jawaban sebelumnya.\n"
                        "Jangan pakai kata: bantu, tolong, panduan, saya bisa, saya akan."
                    )
                },
                {
                    "role": "user",
                    "content": f"User bilang: {prompt}\nBalas natural:"
                }
            ],
            temperature=0.5,
            max_tokens=15
        )

        reply = response.choices[0].message.content.strip()

        # ===== HARD CUT =====
        reply = reply.split("\n")[0]
        reply = reply.split(".")[0]
        reply = reply.split("!")[0]
        reply = reply.split("?")[0]
        reply = " ".join(reply.split()[:4])

        if not reply:
            return ""

        # ===== ANTI GENERIC =====
        banned_single = {"oke", "ok", "sip", "ya", "yup", "yep"}
        if reply.lower() in banned_single:
            return ""

        # ===== ANTI REPEAT =====
        for prev in LAST_REPLIES:
            if prev in reply.lower() or reply.lower() in prev:
                return ""

        LAST_REPLIES.append(reply.lower())
        return reply

    except Exception as e:
        print(f"[❌] ChatGPT error: {e}")
        return ""

# ================== EVENTS ==================
@client.event
async def on_ready():
    print(f"[✅] Login sebagai {client.user}")
    reply_loop.start()
    auto_restart.start()

@client.event
async def on_message(message: Message):
    global pending_message

    if message.channel.id not in CHANNEL_IDS:
        return
    if message.author.id == client.user.id:
        return

    pending_message = message

# ================== REPLY LOOP ==================
@tasks.loop(seconds=2)
async def reply_loop():
    global pending_message, next_reply_time

    if not pending_message:
        return

    now = datetime.now()
    if now < next_reply_time:
        return

    reply = await get_ai_reply(pending_message.content)

    # ===== FILTER KERAS =====
    banned_phrases = [
        "bantu", "tolong", "saya bisa", "saya akan",
        "izin", "mohon", "panduan",
    ]

    if reply and any(p in reply.lower() for p in banned_phrases):
        reply = ""

    if reply and len(reply.split()) > 4:
        reply = ""

    # ===== FALLBACK =====
    if not reply:
        fallback = [
            "Mantap",
            "Siap",
            "Gas",
            "Betul",
            "Oke bro",
            "Yap",
            "Nice",
            "Keren",
        ]
        reply = random.choice(fallback)

    try:
        await pending_message.reply(reply, mention_author=False)
        print(f"[✅] Reply ke {pending_message.author.name}: {reply}")

        delay_seconds = random.randint(REPLY_DELAY_MIN, REPLY_DELAY_MAX)
        next_reply_time = datetime.now() + timedelta(seconds=delay_seconds)
        pending_message = None

    except Exception as e:
        print(f"[❌] Gagal kirim: {e}")

# ================== AUTO RESTART ==================
@tasks.loop(hours=2)
async def auto_restart():
    print("[♻️] Auto restart...")
    python = sys.executable
    os.execv(python, [python] + sys.argv)

@auto_restart.before_loop
async def before_restart():
    await client.wait_until_ready()
    await asyncio.sleep(2 * 60 * 60)

# ================== RUN ==================
client.run(DISCORD_USER_TOKEN)

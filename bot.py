import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ユーザーIDごとに状態を管理する辞書（初期状態は全員 False = 黙る）
user_status = {}


def get_user_status(user_id):
  # 登録がなければ初期値の False（黙る）を返す
  return user_status.get(user_id, False)
@bot.event
async def on_ready():
  print(f"{bot.user} としてログインしました")


@bot.event
async def on_message(message):
  global user_status

  # ボット自身の発言には反応しない
  if message.author == bot.user:
    return

  user_id = message.author.id

  # --- 1. 「喋れ」と言われた場合（言った人の状態をオンにする） ---
  is_mention_shabere = (bot.user in message.mentions) and (
      "喋れ" in message.content
  )
  is_reply_shabere = False

  if message.reference:
    try:
      ref_msg = await message.channel.fetch_message(
          message.reference.message_id
      )
      if ref_msg.author == bot.user and "喋れ" in message.content:
        is_reply_shabere = True
    except Exception:
      pass

  if is_mention_shabere or is_reply_shabere:
    user_status[user_id] = True
    await message.channel.send(
        f"{message.author.mention} さん、喋るように設定したでw"
    )
    return

  # --- 2. 「黙れ」と言われた場合（言った人の状態をオフにする） ---
  is_mention_damare = (bot.user in message.mentions) and ("黙れ" in message.content)
  is_reply_damare = False

  if message.reference:
    try:
      ref_msg = await message.channel.fetch_message(
          message.reference.message_id
      )
      if ref_msg.author == bot.user and "黙れ" in message.content:
        is_reply_damare = True
    except Exception:
      pass

  if is_mention_damare or is_reply_damare:
    user_status[user_id] = False
    await message.channel.send(f"{message.author.mention} 黙るわ...")
    return

  # --- 3. 「せい」の検出（そのユーザーの状態が True のときだけ1回だけ返信） ---
  if get_user_status(user_id) and "せい" in message.content:
    await message.channel.send(
        f"{message.author.mention} 「せい」を検出しましたw"
    )
    return


# ご自身のボットのトークンに書き換えてください
import os
bot.run(os.getenv("DISCORD_TOKEN"))

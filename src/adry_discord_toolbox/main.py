import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

load_dotenv()

# discordの初期設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Google calenderのアカウント設定
creds = service_account.Credentials.from_service_account_file('discord-bot-key.json')
service = build('calendar', 'v3', credentials=creds)

calendar_id = 'discord-bot@discord-bot-411721.iam.gserviceaccount.com'

@client.event
async def on_ready():
    print("logged in")
    activity_message = "このbotはテスト運用されています"
    await client.change_presence(activity=discord.Game(activity_message))
    await tree.sync()

@tree.command(name='ping', description="応答確認")
async def ping_pong(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@tree.command(name='deploy', description="botを更新する")
async def deploy(interaction: discord.Interaction):
    await interaction.response.send_message("再起動します")
    os.system('sh update.sh')

client.run(os.environ["DISCORD_TOKEN"])
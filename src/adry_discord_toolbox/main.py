import os
import datetime
import parse

import discord
from discord import *
from dotenv import load_dotenv

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

# discordの初期設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Google calenderのアカウント設定
creds = service_account.Credentials.from_service_account_file('google-calendar-env-key.json')
service = build('calendar', 'v3', credentials=creds)

calendar_id = 'hynnkgw2525@gmail.com'


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

@tree.command(name='add', description="Googleカレンダーに追加")
async def add(interaction: discord.Interaction, summary: str ,start_date: str, end_date: str = None):
    start = parse.parse_date(start_date)
    print(start)

    end = start + datetime.timedelta(hours=1)
    if end_date is not None:
        end = parse.parse_date(end_date)
    event = {
        'summary': summary,
        'start': {
            'dateTime': start.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Tokyo',
        },
    }
    try:
        res = service.events().insert(calendarId=calendar_id, body=event).execute()
        normal_message = f'予定を作成しました！: [URL]({res.get("htmlLink")})'
        await interaction.response.send_message(normal_message)
    except HttpError as error:
        error_message = f'An error occurred: {error}'
        print(error_message)
        await interaction.response.send_message(error_message)


client.run(os.environ["DISCORD_TOKEN"])
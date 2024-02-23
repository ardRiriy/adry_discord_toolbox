import os
import datetime

import parse

import discord
from discord import *
from discord.ext import tasks

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

calendar_id = os.environ['GOOGLE_CALENDAR_ID']

calendar_notify_time = datetime.time(hour=7, minute=0)

@client.event
async def on_ready():
    print("logged in")
    activity_message = "このbotはテスト運用されています"
    await client.change_presence(activity=discord.Game(activity_message))
    await tree.sync()
    notify.start()


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

# @tasks.loop(time=calendar_notify_time)
@tasks.loop(seconds=20)
async def notify():
    # カレンダーから情報を取得する
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)

    start = today.strftime('%Y-%m-%dT07:00:00+09:00')
    end = tomorrow.strftime('%Y-%m-%dT07:00:00+09:00')

    notify_channel = client.get_channel(int(os.environ['NOTIFY_CHANNEL']))

    try:
        res = service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=end,
            orderBy='startTime',
            singleEvents=True
        ).execute()
        events = res.get('items', None)

        ret = []

        if not events:
            ret.append("今日の予定はありません！良い一日を☀")
        else:
            ret.append("今日の予定は以下のとおりです")
            ret.append("-----------------------")
            for event in events:
                title = event['summary']
                start = datetime.datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d日 %H:%M')
                ret.append(f"{start}: {title}")
            ret.append("-----------------------")
            ret.append("良い一日を☀")

        await notify_channel.send('\n'.join(ret))
    except HttpError as error:
        error_message = f'An error occurred: {error}'
        await notify_channel.send(error_message)

client.run(os.environ["DISCORD_TOKEN"])
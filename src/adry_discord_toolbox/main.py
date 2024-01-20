import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
import discord
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import quandl
import csv

from discord.ext import commands
from discord_components import DiscordComponents, Select, SelectOption
import os
from dotenv import load_dotenv
from cogs.details_fun import column_name

# Keys and Global variables
load_dotenv()
API_key= os.getenv('QUANDL_KEY')
quandl.ApiConfig.api_key=API_key
Bot=commands.Bot(command_prefix="-")
DiscordComponents(Bot)
image=discord.File("test.png")

@Bot.event
async def on_ready():
  print("Logged in as {0.user}".format(Bot))

@Bot.command()
async def ping(ctx):
  await ctx.send(f'Pong {round(Bot.latency*1000)}ms')

@Bot.command()
async def helper(ctx):
  await ctx.send(
    "Select the button to get the help respectively",
    components=[
      Select(
      placeholder="Choose",
      options=[
        SelectOption(
          label="Specific Stock",
          value="StockDetails",
        ),
        SelectOption(
          label="Timeseries",
          value="Charts",
        ),
      ],
      custom_id="Helping"
    )]
  )

  while True:
    try:
      interaction= await Bot.wait_for("Select_option")
      # await interaction.send(content=f'{interaction.custom_id} clicked', ephemeral=False)

      if(interaction.values[0]=="StockDetails"):
        await interaction.send("Stock-Helper helps you get the following information about the stock from BSE stocks database!\n\n"
        "Specific:\n"
        f"{', '.join(column_name)}\n\n"
        "For e.g- $Detail ABB issuer-name\n"
        "To exract the above Infromation use 'Security Name' for the stock. Look at the example below:\n\n"
        "Aggregate:\n"
        "`'Complete' Detail\n`"
        "List of 'Sectors'\n"
        "List of 'Igroup' Name\n"
        "List of 'Isubgroup' Name\n"
        "All 'Sector-companies' in particular sector\n",
        ephemeral=False)
        
      elif(interaction.values[0]=="Charts"):
        await interaction.send(interaction.values[0], ephemeral=False)

    except discord.NotFound:
      ctx.send("error")


@Bot.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@Bot.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for dirfile in os.listdir("./cogs"):
  if(dirfile.endswith('.py')):
    Bot.load_extension(f'cogs.{dirfile[:-3]}')

Bot.run(os.getenv('BOT_TOKEN'))

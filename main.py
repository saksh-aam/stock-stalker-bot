import discord
from discord.ext import commands
from discord_components import DiscordComponents, Select, SelectOption
import os
from dotenv import load_dotenv
from cogs.details_fun import column_name

# Keys and Global variables
load_dotenv()

Bot=commands.Bot(command_prefix="-")
DiscordComponents(Bot)
image=discord.File("./datafiles/test.png")

@Bot.event
async def on_ready():
  print("Logged in as {0.user}".format(Bot))

@Bot.command()
async def ping(ctx):
  await ctx.send(f'Pong {round(Bot.latency*1000)}ms')

@Bot.command()
async def helper(ctx):
  await ctx.send("All the commands are divivded into two groups\n"
    "Select the button to get the help respectively",
    components=[
      Select(
      placeholder="Choose",
      options=[
        SelectOption(
          label="Stocks & Sectors",
          value="StockDetails",
        ),
        SelectOption(
          label="Timeseries & Charts",
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
        await interaction.send("To get started you got to be ready with **Security Ids** of stocks! \n\n"
        "**Stocks specific details**:\n"
        f"{', '.join(column_name)}\n\n"
        "`For e.g- $issuename ABB `\n\n"
        
        "**Aggregate details**:\n"
        "Complete Detail of stock\n"
        "List of Sectors\n"
        "List of Igroup Name\n"
        "List of Isubgroup Name\n"
        "All the companies in particular sector\n\n"
        "Type in `-help` to know the syntax/ command",
        ephemeral=False)
        
      elif(interaction.values[0]=="Charts"):
        await interaction.send("**Lets Visualise**\n"
        "To get started you got to be ready with **Security Codes** of stocks!\n"
        "You can easily get the Id using `-securitycode security_id` command\n\n"
        "**Stock Charts**\n"
        "Price Action chart- Line Graph\n"
        "Price Action chart- Candles Graph\n"
        "Volumn in Daily Timeframe\n"
        "% Deli. Qty to Traded Qty\n"
        "Daily percentage Change in price\n"
        "Cumulative returns from the Day you bought\n\n"
        "`For e.g- $candles 500002 23/8/21`"
        "**Indices**\n"
        "Indices Code using `indices` command\n"
        "Index Price Action- Candles\n\n"
        "Type in `-help` to know the syntax/ command\n"
        "For the charts with Secuirty Code you need to specify the starting date\n"
        "Cherry on the Cake- for the candles yo can also pass the Moving Average (Default=2)",
        )

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


@Bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Missing Required argument")

  elif isinstance(error, commands.CommandNotFound):
    await ctx.send("Not Trained for that command :(")

Bot.run(os.getenv('BOT_TOKEN'))


import discord
import csv
import pandas as pd
from discord.ext import commands

# Importing and operations to use BSE stocks details in CSV file
with open("./cogs/Select.csv") as file:
    csv_reader=csv.reader(file)
    df=pd.DataFrame([csv_reader], index=None)

column_name=[]
for x in df[0]:
    for val in x:
        column_name.append(val)

csv_file=pd.read_csv("./cogs/Select.csv", header=None, names=column_name)

# print(csv_file['Security Code'])
# def securityCodeDetail(arg):
#  for x, y in zip(cvs_file['Security Code'], cvs_file['Security Id']):
#      if(y==upper(arg)):
#          res=x
#  return res

# def issuerNameDetail(arg):
#  for x, y in zip(cvs_file['Issuer Name'], cvs_file['Security Id']):
#      if(y==upper(arg)):
#          res=x
#  return res

# def securityNameDetail(arg):
#  for x, y in zip(cvs_file['Security Name'], cvs_file['Security Id']):
#      if(y==upper(arg)):
#          res=x
#  return res
def generalFn(arg, col1, col2):
    arg=arg.upper()
    for x, y in zip(csv_file['Security Code'], csv_file['Security Id']):
        if(y==arg):
            return x


class functions(commands.Cog):
    def __init__(self, Bot):
        self.Bot=Bot

# Event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

# Basic Commands
    @commands.command()
    async def securitycode(self, ctx, arg):
        await ctx.send(f'`Security Code for {arg} is {generalFn(arg, "Security Code", "Security Id")}`')

    @commands.command()
    async def issuername(self, ctx, arg):
        await ctx.send(f'`Issuer Name for {arg} is {generalFn(arg, "Issuer Name", "Security Id")}`')

    @commands.command()
    async def securityname(self, ctx, arg):
        await ctx.send(f'`Security Name for {arg} is {generalFn(arg, "Security Name", "Security Id")}`')

    @commands.command()
    async def status(self, ctx, arg):
        await ctx.send(f'`Status for {arg} is {generalFn(arg, "Status", "Security Id")}`')

    @commands.command()
    async def group(self, ctx, arg):
        await ctx.send(f'`Group for {arg} is {generalFn(arg, "Group", "Security Id")}`')

    @commands.command()
    async def facevalue(self, ctx, arg):
        await ctx.send(f'`Face Value for {arg} is {generalFn(arg, "Face Value", "Security Id")}`')

    @commands.command()
    async def isisno(self, ctx, arg):
        await ctx.send(f'`ISIN No for {arg} is {generalFn(arg, "ISIN No", "Security Id")}`')

    @commands.command()
    async def industry(self, ctx, arg):
        await ctx.send(f'`Industry for {arg} is {generalFn(arg, "Industry", "Security Id")}`')

    @commands.command()
    async def sectorname(self, ctx, arg):
        await ctx.send(f'`Sector Name for {arg} is {generalFn(arg, "Sector Name", "Security Id")}`')

    @commands.command()
    async def igroup(self, ctx, arg):
        await ctx.send(f'`Igroup for {arg} is {generalFn(arg, "Igroup Name", "Security Id")}`')

    @commands.command()
    async def isubgroup(self, ctx, arg):
        await ctx.send(f'`ISubgroup for {arg} is {generalFn(arg, "ISubgroup Name", "Security Id")}`')


# Aggregate Commands
    @commands.command()
    async def complete(self, ctx, arg):
        arg=arg.upper()
        i=0
        for x in df:

def setup(Bot):
    Bot.add_cog(functions(Bot))
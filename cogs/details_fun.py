import discord
import csv
import pandas as pd
from discord.ext import commands

# Importing and operations to use BSE stocks details in CSV file
with open("./datafiles/Select.csv") as file:
    csv_reader=csv.reader(file)
    df=pd.DataFrame([csv_reader], index=None)

column_name=[]
for x in df[0]:
    for val in x:
        column_name.append(val)

csv_file=pd.read_csv("./datafiles/Select.csv", header=None, names=column_name)

def generalFn1(arg, col1):
    arg=arg.upper()
    for x, y in zip(csv_file[col1], csv_file['Security Id']):
        if(y==arg):
            return x

def generalFn2(arg):
    arg=arg.replace("-", " ")
    with open("./datafiles/sampledata.csv", "w+") as datafile:
        csv_writer=csv.writer(datafile)
        csv_writer.writerow(column_name)

        i=0
        while(i<44599):
            for x in df[i]:
                if (x[8]==arg and x[4]=='Active'):
                    res=[]
                    for x in df[i]:
                        for val in x:
                            res.append(val)
                    csv_writer.writerow(res)
            i=i+1
        datafile.close()

def generalfn3(arg):
    setSi=set(csv_file['Industry'])
    arg=arg.replace("-", " ")
    with open("./datafiles/sampledata.csv", "w+") as datafile:
        csv_writer=csv.writer(datafile)
        csv_writer.writerow(setSi)
    datafile.close()


class callData(commands.Cog):
    def __init__(self, Bot):
        self.Bot=Bot

# Event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Details Functions file running")

# Basic Commands
    @commands.command()
    async def securitycode(self, ctx, arg):
        await ctx.send(f'`Security Code for {arg} is {generalFn1(arg, "Security Code")}`')

    @commands.command()
    async def issuername(self, ctx, arg):
        await ctx.send(f'`Issuer Name for {arg} is {generalFn1(arg, "Issuer Name")}`')

    @commands.command()
    async def securityname(self, ctx, arg):
        await ctx.send(f'`Security Name for {arg} is {generalFn1(arg, "Security Name")}`')

    @commands.command()
    async def status(self, ctx, arg):
        await ctx.send(f'`Status for {arg} is {generalFn1(arg, "Status")}`')

    @commands.command()
    async def group(self, ctx, arg):
        await ctx.send(f'`Group for {arg} is {generalFn1(arg, "Group")}`')

    @commands.command()
    async def facevalue(self, ctx, arg):
        await ctx.send(f'`Face Value for {arg} is {generalFn1(arg, "Face Value")}`')

    @commands.command()
    async def isisno(self, ctx, arg):
        await ctx.send(f'`ISIN No for {arg} is {generalFn1(arg, "ISIN No")}`')

    @commands.command()
    async def industry(self, ctx, arg):
        await ctx.send(f'`Industry for {arg} is {generalFn1(arg, "Industry")}`')

    @commands.command()
    async def sectorname(self, ctx, arg):
        await ctx.send(f'`Sector Name for {arg} is {generalFn1(arg, "Sector Name")}`')

    @commands.command()
    async def igroup(self, ctx, arg):
        await ctx.send(f'`Igroup for {arg} is {generalFn1(arg, "Igroup Name")}`')

    @commands.command()
    async def isubgroup(self, ctx, arg):
        await ctx.send(f'`ISubgroup for {arg} is {generalFn1(arg, "ISubgroup Name")}`')


# Aggregate Commands
    @commands.command()
    async def complete(self, ctx, arg):
        arg=arg.upper()
        i=0
        flag=False
        while(i<44599):
            for x in df[i]:
                if (x[2]==arg):
                    flag=True
            
            if (flag):
                break
            i=i+1
        details=[]
        for x in df[i]:
            for val in x:
                details.append(val)

        result=[]
        for x, y in zip(column_name, details):
            result.append(f"`{x} : {y}`")
        await ctx.send("\n".join(result))

    @commands.command()
    async def industries(self, ctx):
        generalfn3('Industry')
        await ctx.send(f'All the Industry are there in the file!', file=discord.File("./datafiles/sampledata.csv"))

    @commands.command()
    async def sectors(self, ctx):
        generalfn3('Sector Name')
        await ctx.send(f'All the Sectors are there in the file!', file=discord.File("./datafiles/sampledata.csv"))

    @commands.command()
    async def igroups(self, ctx):
        generalfn3('Igroup Name')
        await ctx.send(f'All the Igroup are there in the file!', file=discord.File("./datafiles/sampledata.csv"))

    @commands.command()
    async def igroups(self, ctx):
        generalfn3('ISubgroup Name')
        await ctx.send(f'All the ISubgroup are there in the file!', file=discord.File("./datafiles/sampledata.csv"))

    @commands.command()
    async def industryallstocks(self, ctx, arg):
        generalFn2(arg)
        await ctx.send(f'All the stocks in {arg} Industries are there in the file!', file=discord.File("./datafiles/sampledata.csv"))
    
def setup(Bot):
    Bot.add_cog(callData(Bot))
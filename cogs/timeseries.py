import discord
from discord.ext import commands
import quandl
import pandas as pd
import os
from datetime import *
import matplotlib.pyplot as plt
import mplfinance
from dotenv import load_dotenv

load_dotenv()
quandl.ApiConfig.api_key=os.getenv('QUANDL_KEY')
format_date="%d/%m/%y"

class callCharts(commands.Cog):
    def __init__(self, Bot):
        self.Bot=Bot

# Event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Timeseries Functions file running")

#commands
    @commands.command()
    async def chart(self, ctx, arg, datee):
        image=discord.File("test.png")
        result=quandl.get(f'BSE/BOM{arg}.4', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        plt.plot(result)
        plt.savefig("test.png")
        plt.close()
        await ctx.send(file=image)

    @commands.command()
    async def stockcandle(self, ctx, arg, datee, mavg=2):
        image=discord.File("test.png")
        result=quandl.get(f'BSE/BOM{arg}', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        # result['Date']=result.index
        mplfinance.plot(result, type='candle', style='charles', mav= mavg, ylabel='Price', savefig="test.png")  

        await ctx.send(file=image)

    @commands.command()
    async def volume(self, ctx, arg, datee):
        image=discord.File("test.png")
        shares=quandl.get(f'BSE/BOM{arg}.6', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        shares.reset_index(level=['Date'], inplace=True)
        trades=quandl.get(f'BSE/BOM{arg}.7', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        trades.reset_index(level=['Date'], inplace=True)

        fig, axis=plt.subplots(2)
        axis[0].bar(shares['Date'], shares['No. of Shares'])
        axis[0].set_title("Number of Shares traded")

        axis[1].bar(trades['Date'], trades['No. of Trades'])
        axis[1].set_title("Number of trades occured")
        plt.tight_layout(1)
        plt.xticks(rotation=25)
        plt.savefig("test.png")
        plt.close()
        await ctx.send(file=image)
        
    @commands.command()
    async def perdelivery(self, ctx, arg, datee):
        image=discord.File("test.png")
        delivery=quandl.get(f'BSE/BOM{arg}.10', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        delivery.reset_index(level=['Date'], inplace=True)

        trades=quandl.get(f'BSE/BOM{arg}.7', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        trades.reset_index(level=['Date'], inplace=True)

        fig, axis=plt.subplots(2)
        axis[0].bar(trades['Date'], trades['No. of Trades'])
        axis[0].set_title("Number of trades occured")

        axis[1].bar(delivery['Date'], delivery['% Deli. Qty to Traded Qty'])
        axis[1].set_title("% Delivery Qty to Traded Qty")

        plt.tight_layout(1)
        plt.xticks(rotation=25)
        plt.savefig("test.png")
        plt.close()
        await ctx.send(file=image)

    @commands.command()
    async def dailyperchange(self, ctx, arg, datee):
        image=discord.File("test.png")
        result=quandl.get(f'BSE/BOM{arg}.4', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        # result=result['Close']/result['Close'].shift(1) -1
        result.reset_index(level=['Date'], inplace=True)
        result['Return']=result['Close'].pct_change(1)

        fig, axis=plt.subplots(2)
        axis[0].bar(result['Date'], result['Return'])
        axis[0].set_title("Daily percentage change Bar-graph")

        axis[1].hist(result['Return'], bins=100)
        axis[1].set_title("Histogram")

        plt.tight_layout(1)
        plt.xticks(rotation=25)
        plt.savefig("test.png")
        plt.close()
        await ctx.send("Letz check the votality of stock!",file=image)

    @commands.command()
    async def cumulativereturn(self, ctx, arg, datee):
        image=discord.File("test.png")
        result=quandl.get(f'BSE/BOM{arg}.4', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        result['Return']=result['Close'].pct_change(1)
        result['Cumulative']=(1+result['Return']).cumprod()
        plt.plot(result['Cumulative'])
        plt.xticks(rotation=25)
        plt.savefig("test.png")
        plt.close()
        cumreturns=result['Cumulative'].iloc[-1]
        await ctx.send(f'You got {cumreturns:.2f}% of returns since {datee} from {arg}',  file=image)

    @commands.command()
    async def indices(self, ctx):
        await ctx.send(file=discord.File("./datafiles/indices.csv"))

    @commands.command()
    async def indexcandle(self, ctx, code, datee, mavg=2):
        image=discord.File("test.png")
        result=quandl.get(f'BSE/{code}', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        
        mplfinance.plot(result, type='candle', style='charles', mav= mavg, ylabel='Price', savefig="test.png")  
        await ctx.send(file=image)



def setup(Bot):
    Bot.add_cog(callCharts(Bot))
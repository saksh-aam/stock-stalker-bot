import discord
from discord.ext import commands
import quandl
import pandas as pd
import os
from datetime import *
import matplotlib.pyplot as plt
import mplfinance

quandl.ApiConfig.api_key=os.environ.get('QUANDL_KEY')
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
        image=discord.File("./datafiles/test.png")
        result=quandl.get(f'BSE/BOM{arg}.4', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        result['Return']=result['Close'].pct_change(1)
        result['Cumulative']=(1+result['Return']).cumprod()
        plt.plot(result)
        plt.savefig("./datafiles/test.png")
        plt.close()
        cumreturns=result['Cumulative'].iloc[-1]
        await ctx.send(f'You got {cumreturns:.2f}% of returns since {datee} from {arg}', file=image)

    @commands.command()
    async def stockcandle(self, ctx, arg, datee, mavg=2):
        image=discord.File("./datafiles/test.png")
        result=quandl.get(f'BSE/BOM{arg}', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        # result['Date']=result.index
        mplfinance.plot(result, type='candle', style='charles', mav= mavg, ylabel='Price', savefig="./datafiles/test.png")  

        await ctx.send(file=image)

    @commands.command()
    async def volumeshares(self, ctx, arg, datee):
        image=discord.File("./datafiles/test.png")
        shares=quandl.get(f'BSE/BOM{arg}.6', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        shares.reset_index(level=['Date'], inplace=True)

        plt(kind=bar, shares['Date'], shares['No. of Shares'])
        plt.set_title("Number of Shares traded")
        plt.xticks(rotation=25)
        plt.savefig("./datafiles/test.png")
        plt.close()
        await ctx.send("Plot of number of {arg} Shares Traded per day from {datee} till date:",file=image)
        
    @commands.command()
    async def perdelivery(self, ctx, arg, datee):
        image=discord.File("./datafiles/test.png")
        delivery=quandl.get(f'BSE/BOM{arg}.10', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        delivery.reset_index(level=['Date'], inplace=True)
        
        plt(kind=bar, delivery['Date'], delivery['% Deli. Qty to Traded Qty'])
        plt.set_title("% Delivery Qty to Traded Qty")
        plt.xticks(rotation=25)
        plt.savefig("./datafiles/test2.png")
        plt.close()
        await ctx.send(file=image)
    
    @commands.command()
    async def numtrades(self, ctx, arg, datee):
        image=discord.File("./datafiles.test.png")
        trades=quandl.get(f'BSE/BOM{arg}.7', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        trades.reset_index(level=['Date'], inplace=True)
        
        plt(kind=bar, trades['Date'], trades['No. of Trades'])
        plt.set_title("Number of trades occured")
        plt.xticks(rotation=25)
        plt.savefig("./datafiles/test.png")
        plt.close()
        await ctx.send(file=image)
        
    @commands.command()
    async def dailyperchange(self, ctx, arg, datee):
        image=discord.File("./datafiles/test.png")
        result=quandl.get(f'BSE/BOM{arg}.4', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        # result=result['Close']/result['Close'].shift(1) -1
        result.reset_index(level=['Date'], inplace=True)
        result['Return']=result['Close'].pct_change(1)

        plt(kind=bar, result['Date'], result['Return'])
        plt.set_title("Daily percentage change of Stock Price")
        plt.xticks(rotation=25)
        plt.savefig("./datafiles/test.png")
        plt.close()
        await ctx.send(file=image)

#     @commands.command()
#     async def cumulativereturn(self, ctx, arg, datee):
#         image=discord.File("./datafiles/test.png")
#         result=quandl.get(f'BSE/BOM{arg}.4', start_date=datetime.strptime(datee, format_date), end_date=date.today())
#         result['Return']=result['Close'].pct_change(1)
#         result['Cumulative']=(1+result['Return']).cumprod()
#         plt.plot(result['Cumulative'])
#         plt.xticks(rotation=25)
#         plt.savefig("./datafiles/test.png")
#         plt.close()
#         cumreturns=result['Cumulative'].iloc[-1]
#         await ctx.send(f'You got {cumreturns:.2f}% of returns since {datee} from {arg}',  file=image)

    @commands.command()
    async def indices(self, ctx):
        await ctx.send(file=discord.File("./datafiles/indices.csv"))

    @commands.command()
    async def indexcandle(self, ctx, code, datee, mavg=2):
        image=discord.File("./datafiles/test.png")
        result=quandl.get(f'BSE/{code}', start_date=datetime.strptime(datee, format_date), end_date=date.today())
        
        mplfinance.plot(result, type='candle', style='charles', mav= mavg, ylabel='Price', savefig="./datafiles/test.png")  
        await ctx.send(file=image)



def setup(Bot):
    Bot.add_cog(callCharts(Bot))

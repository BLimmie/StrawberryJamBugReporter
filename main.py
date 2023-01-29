import discord
import os
from responses import LabelView

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.slash_command(name="report_issue", description="Report an issue")
async def report(ctx):
    await ctx.respond(view=LabelView())


bot.run(os.environ['BOT_LOGIN'])

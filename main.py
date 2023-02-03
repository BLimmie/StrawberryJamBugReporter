import discord
import os
from responses import LabelView

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.slash_command(name="report_issue", description="Report an issue")
async def report(ctx: discord.ApplicationContext):
    if ctx.channel_id != 1069022322960371762:
        return
    await ctx.respond(view=LabelView())


bot.run(os.environ['BOT_LOGIN'])

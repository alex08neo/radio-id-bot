import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from app.player import RadioPlayer
from app.extras import Extras
from app.misc import Misc

load_dotenv()

PREFIX = "!radio"
TOKEN = os.getenv("DISCORD_TOKEN")
if os.environ.get("ENVIRONMENT") == "dev":
    PREFIX = "!r"
    TOKEN = os.getenv("DISCORD_TOKEN_DEV")

if TOKEN is None:
    print("CONFIG ERROR: Please state your discord bot token in .env")
    exit()


help_command = commands.DefaultHelpCommand(
    no_category='Basic'
)

bot = commands.Bot(command_prefix=f"{PREFIX} ", description="Discord bot untuk memainkan radio favoritmu!", help_command=help_command)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    print(f"Currently added by {len(bot.guilds)} servers")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"`{PREFIX} help` untuk memulai."))


@bot.event
async def on_command_error(ctx, error):
    if os.environ.get("ENVIRONMENT") == "dev":
        raise error

    if isinstance(error, commands.CommandOnCooldown):
        cd = "{:.2f}".format(error.retry_after)
        await ctx.send(f"Gunakan command ini lagi setelah {cd} detik")
        return

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{str(error)}, use `{PREFIX} help` to list available commands")
        return

    if isinstance(error, commands.ChannelNotFound):
        await ctx.send(str(error))
        return

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(str(error))
        return

    if isinstance(error, commands.MissingRequiredArgument):
        return

    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send(str(error))
        return

    await ctx.send(str(error))
    raise error


bot.add_cog(RadioPlayer(bot, PREFIX))
bot.add_cog(Extras(bot, PREFIX))
bot.add_cog(Misc(bot, PREFIX))
bot.run(TOKEN)

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in .env file")

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Bad argument provided. Please check the command usage.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, disnake.Forbidden):
        await ctx.send("I do not have permission to send messages in this channel.")
    elif isinstance(error, disnake.HTTPException):
        await ctx.send("An HTTP error occurred. Please try again later.")
    elif isinstance(error, disnake.NotFound):
        await ctx.send("The requested resource was not found.")
    else:
        await ctx.send(f"An error occurred: {error}")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
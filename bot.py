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

@bot.command()
async def add(ctx, a: int, b: int):
    result = a + b
    await ctx.send(f"The sum of {a} and {b} is {result}.")

@bot.command()
async def subtract(ctx, a: int, b: int):
    result = a - b
    await ctx.send(f"The difference between {a} and {b} is {result}.")

@bot.command()
async def multiply(ctx, a: int, b: int):
    result = a * b
    await ctx.send(f"The product of {a} and {b} is {result}.")

@bot.command()
async def divide(ctx, a: int, b: int):
    if b == 0:
        await ctx.send("Cannot divide by zero.")
    else:
        result = a / b
        await ctx.send(f"The quotient of {a} and {b} is {result}.")

@bot.command()
async def info(ctx):
    embed = disnake.Embed(title="Bot Information", description="This is a simple bot created with Disnake.", color=0x00ff00)
    embed.add_field(name="Bot Name", value=bot.user.name, inline=True)
    embed.add_field(name="Bot ID", value=bot.user.id, inline=True)
    embed.add_field(name="Commands", value="Use !help to see available commands.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = disnake.Embed(title="Help", description="List of available commands:", color=0x00ff00)
    embed.add_field(name="!ping", value="Check if the bot is online.", inline=False)
    embed.add_field(name="!hello", value="Greet the bot.", inline=False)
    embed.add_field(name="!echo <message>", value="Echo back the provided message.", inline=False)
    embed.add_field(name="!add <a> <b>", value="Add two numbers.", inline=False)
    embed.add_field(name="!subtract <a> <b>", value="Subtract two numbers.", inline=False)
    embed.add_field(name="!multiply <a> <b>", value="Multiply two numbers.", inline=False)
    embed.add_field(name="!divide <a> <b>", value="Divide two numbers.", inline=False)
    embed.add_field(name="!info", value="Get information about the bot.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount < 1 or amount > 100:
        await ctx.send("Please specify a number between 1 and 100.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=5)

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
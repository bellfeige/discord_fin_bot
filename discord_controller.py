import asyncio
import json
import re
from datetime import datetime, timedelta, time
from urllib import parse, request

import discord
import pytz
from discord.ext import commands
from finviz import Finviz

bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd",
                          timestamp=datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    # print(html_content.read().decode())
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
    print(search_results)
    # I will put just the first result, you can loop the response to show more results
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


# Events
@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Streaming(name="Tutorials", url="http://www.twitch.tv/accountname"))
    print('My Ready is Body')


@bot.listen()
async def on_message(message):
    if "tutorial" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
        await message.channel.send('This is that you want http://youtube.com/fazttech')
        await bot.process_commands(message)


@bot.command()
async def finviz(ctx, arg):
    if arg == "map":
        map_img = Finviz.snp500_map()
        await ctx.send(map_img)
    else:
        await ctx.send("working on it")


@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


target_channel_id = 944463868128813097
WHEN = time(21, 15, 0)  # UTC is default
print(WHEN)


# @tasks.loop(seconds=5)
async def called_once_a_day():
    await bot.wait_until_ready()
    message_channel = bot.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    print(f"Sending finviz scheduled map")
    map_img = Finviz.snp500_map()
    await message_channel.send(map_img)


async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        print(f"seconds = {seconds}")
        await asyncio.sleep(seconds)  # Sleep until tomorrow and then the loop will start
    while True:
        now = datetime.utcnow()  # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        print(f"seconds_until_target = {seconds_until_target}")
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)  # Sleep until tomorrow and then the loop will start a new iteration


if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)

    TOKEN = config["token"][config["env"]]

    # called_once_a_day.start()
    bot.loop.create_task(background_task())
    bot.run(TOKEN)

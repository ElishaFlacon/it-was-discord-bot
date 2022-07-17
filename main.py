import discord
from discord.ext import commands
from config import settings
import random
import json
import requests


print('Start Working!')

bot = commands.Bot(command_prefix=settings['prefix'])


def it_was_or_not():
    rng = random.randrange(1, 10000)
    if rng > 5000:
        return 'Было!'
    elif rng == 9827:
        return 'Эмм... я хз, если честно :P'
    else:
        return 'Не Было!'


def rng_img():
    image_data = ['img/cat', 'img/fox', 'animu/wink']
    image_weight = [50, 30, 20]

    img = random.choices(image_data, image_weight)[0]

    return img


@bot.command()
async def о(ctx):
    author = ctx.message.author
    response = requests.get(f'https://some-random-api.ml/{rng_img()}')
    json_data = json.loads(response.text)

    embed = discord.Embed(
        color=0xff9900, title=f'{author.name}, {it_was_or_not()}')
    embed.set_image(url=json_data['link'])

    await ctx.send(embed=embed)


bot.run(settings['token'])

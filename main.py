import discord
from config import settings
import random
import json
import requests
from bs4 import BeautifulSoup


# Инициализируем бота
client = discord.Client()


# Функция выбора было или не было
def it_was_or_not():
    rng = random.randrange(1, 1000)
    if rng > 500:
        return 'Было!'
    elif rng == 501:
        return 'Эмм... я хз, если честно :P'
    else:
        return 'Не Было!'


# Функция создания рандомного изображения
def rng_img():
    image_data = ['img/cat', 'img/fox', 'animu/wink']
    image_weight = [50, 30, 20]
    img = random.choices(image_data, image_weight)[0]
    return img


# Функция создания интеграции?! ну этого embed
def create_embded(message, proop):
    if proop == True:
        response = requests.get(f'https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)
        # Создаем интеграцию
        embed = discord.Embed(
            color=0xff9900, title=f'{message.author.name}, САМ БЫДЛО ПЫХ ПЫХ!!!')
        embed.set_image(url=json_data['link'])
    else:
        # Через жопу генерируем ссылку на картинку
        response = requests.get(f'https://some-random-api.ml/{rng_img()}')
        json_data = json.loads(response.text)
        # Создаем интеграцию
        embed = discord.Embed(
            color=0xff9900, title=f'{message.author.name}, {it_was_or_not()}')
        embed.set_image(url=json_data['link'])
    return embed


# Функция генерации анекдота
def create_joke():
    jokes_list = []
    url_joke = f'https://4tob.ru/anekdots/tag/black/page{int(random.uniform(1, 4))}'
    joke_req = requests.get(url_joke)
    soup = BeautifulSoup(joke_req.text, 'html.parser')
    jokes = soup.find_all('div', class_='text')
    for joke in jokes:
        jokes_list.append(joke.text)
    return str(random.choice(jokes_list))


# Декоратор с функцией прослушивания сообщений
@ client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return

    if msg.startswith('!анекдот'):
        print(
            f'{message.author.name} написал: \"\"{message.content}\"\"')
        await message.channel.send(create_joke())

    # С помощью метода финд находим нужное слово
    # Даже в такой строчке - 'sdЫ2@4аы2быЛоффООФЫВ2392'
    # Так как если финд ничего не нашел он возвращает -1, то мы ставим условие >= 0
    if msg.startswith(''):
        if msg.find('было') >= 0:
            print(
                f'{message.author.name} написал: \"\"{message.content}\"\"')
            await message.channel.send(embed=create_embded(message, False))
        if msg.find('быдло') >= 0:
            print(
                f'{message.author.name} написал: \"\"{message.content}\"\"')
            await message.channel.send(embed=create_embded(message, True))


# Работаем
print('Start Working!')
# Инициализируем бота
client.run(settings['token'])

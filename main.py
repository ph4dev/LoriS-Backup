import discord
import asyncio
import random

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(
        game=discord.Game(type=1, name='/ajuda', url='https://twitch.tv/kaigogames_'))

    print('BOT ONLINE')
    print(client.user.name)
    print(client.user.id)
    print('-=-=-=-=-=')

@client.event
async def on_message(message):
    if message.content.lower().startswith('/oi'):
        await client.send_message(message.channel, "Olá ")
    if message.content.lower().startswith('/hacker'):
        await client.send_message(message.channel, "Diego é claro ")
    if message.content.lower().startswith('/help'):
        await client.send_message(message.channel, "**Em Breve**")

    if message.content.lower().startswith('/vom'):
        choice = random.randint(1,2)
        if choice == 1:
            await client.send_message(message.channel, "Verdade")
        if choice == 2:
            await client.send_message(message.channel, "Mentira")

    if message.content.lower().startswith('/nv'):
        choice = random.randint(1,4)
        if choice == 1:
            await client.send_message(message.channel, "Você tem 20% de doidice")
        if choice == 2:
            await client.send_message(message.channel, "Você tem 80% de doidice")
        if choice == 3:
            await client.send_message(message.channel, "Você tem 40% de doidice")
        if choice == 4:
            await client.send_message(message.channel, "Você tem 100% de doidice")

    if message.content.lower().startswith('/moeda'):
        choice = random.randint(1,2)
        if choice == 1:
            await client.add_reaction(message, '😀')
        if choice == 2:
            await client.add_reaction(message, '👑')

    if message.content.lower().startswith('/link'):
        await client.send_message(message.channel, "Link do Bot:")
        await client.send_message(message.channel, "https://discordapp.com/oauth2/authorize?client_id={}&permissions=8&scope=bot".format(client.user.id))

@client.event
async def on_member_join(member):
    role = discord.utils.find(lambda r: r.name == "Membros", member.server.roles)
    await client.add_roles(member, role)

client.run("NDE3MzYzNjQ1NDcxNjUzODg4.DXSzKw.8jS4SlatszvaB0LmVthqJSbpQmk")
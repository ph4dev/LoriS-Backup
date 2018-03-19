import discord
import asyncio
import random
import aiohttp
import os
import re
import secreto
import websockets
import discord.member
from datetime import datetime, timedelta

vermelho = 0xbb0021
client = discord.Client()

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token

msg_author = None
@client.event
async def on_ready():
    await client.change_presence(
        game=discord.Game(name="/ajuda || Estou on em " + str(len(client.servers)) + " servidores!",
                          url='https://twitch.tv/tmpoarr', type=1))

    print('-------------------------------------------------------------------------------------------------')
    print('Logado como ' + client.user.name + ' (ID:' + client.user.id + ') | Conectado a ' + str(
        len(client.servers)) + ' servidores | Em contato com ' + str(len(set(client.get_all_members()))) + ' usuarios')
    print('-------------------------------------------------------------------------------------------------')
    print('Link de convite do {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('-------------------------------------------------------------------------------------------------')
@client.event
async def on_member_join(member):
    #Envia uma mensagem privada de boas vindas com o nome do servidor e mencionando o usuario
    await client.send_message(member, 'Bem Vindo ao '+ member.server.name + ' ' + member.mention)
    #Adiciona o cargo "Membro" ao membro que entrou
    role = discord.utils.find(lambda r: r.name == "Membros", member.server.roles)
    await client.add_roles(member, role)

@client.event
async def on_member_ban(user):
    #canal que vai mandar: (pode alterar se quiser)
    channel = discord.utils.find(lambda c: c.name == 'bans', user.server.channels)
    #O embed: (troque a mensagem pelo que quiser, só não apague o "{0.name}, nem o .format
    embed = discord.Embed(title='GamingBOT - Bans', description='Algum moderador baniu o membro **@{0.name}** do servidor!\n\nBem Feito :P'.format(user), color=vermelho)
    #Para exibir o gif do thor: (se quiser apagar é escolha sua
    embed.set_image(url='https://im4.ezgif.com/tmp/ezgif-4-78bb814d9d.gif')
    embed.set_thumbnail(url='https://escolavoando.com.br/images/logo.png')
    #Manda a mensagem no canal
    await client.send_message(channel, embed=embed)
@client.event
async def on_message(message):
    #chat
    if message.content.lower().startswith('/cat'):
        async with aiohttp.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                canal = message.channel
                await client.delete_message(message)
                await client.send_message(canal, js['file'])

    if message.content.lower().startswith('/dog'):
        async with aiohttp.get('https://random.dog/woof.json') as r:
            if r.status == 200:
                js = await r.json()
                canal = message.channel
                await client.delete_message(message)
                await client.send_message(canal, js['url'])
    if message.content.lower().startswith('/oi'):
        await client.send_message(message.channel, "Olá ")
    if message.content.lower().startswith('/voar'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            description='está voando',
        )
        embed.set_author(name= message.author.name)
        embed.set_image(url= 'http://www.gifmania.com.br/Gif-Animados-Quadrinhos/Animacoes-Superman/Imagens-Superman-Voando/Superman-Voando-87265.gif')
        await client.send_message(message.channel, embed=embed)
    elif message.content.lower().startswith('/avatar'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            descriptino=None,
        )
        embed.set_author(name=message.author.name)
        embed.set_image(url=message.author.avatar_url)
        await client.send_message(message.channel, embed=embed)
    elif message.content.lower().startswith('/perfil'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            description='money: xx                                                                                                                                                                                       tags: xx                                                                                                                                                                                       rep: xx',
        )
        embed.set_author(name=message.author.name)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text='id: '+ message.author.id)
        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith('/pete'):
        await client.send_message(message.channel, "'-'")
    if message.content.lower().startswith('/repete'):
        await client.send_message(message.channel, "'-'")
    if message.content.lower().startswith('/hacker'):
        await client.send_message(message.channel, ":P")
    if message.content.lower().startswith('/tag list'):
        await client.send_message(message.channel,
        embed=discord.Embed(title="Tags - list", description="red,blue,green,csgo,lol",color=0xbb0021))
    if message.content.lower().startswith('/tags'):
        await client.send_message(message.channel,
        embed=discord.Embed(title="GamingBOT - Tags", description="/tag list - Lista de Tags                                                                                                                                                                                       /tag add (tag) - adicionar uma tag                                                                                                                                                                                       /tag remove (tag) - remover uma tag", color=0xbf0022))
    #ajuda
    if message.content.lower().startswith("/ajuda"):
     embed1 =discord.Embed(
        title="GamingBOT - Ajuda",
        color=vermelho,
        description="/vom (msg) - Verdade ou Mentira \n"
                    "/hacker - O Maior hacker da história (vai ser removido) \n"
                    "/moeda - Cara ou Coroa \n"
                    "/dog - Imagens de Cachorro \n"
                    "/cat - Imagens de Gato \n"
                    "/nv - Nivel de Doidice \n"
                    "/limpar (0 a 100) [administrador] \n"
                    "/tags - Como deixar seu nome colorido \n"
                    "/perfil - Veja seu Perfil (beta) \n"
                    "/avatar - Veja seu lindo avatar \n"
                    "/voar - Voe que nem um passarinho \n"
                    "/instagram (img) - Deixe as pessoas avaliarem suas fotos ",)
    await client.send_message(message.channel, embed=embed1)
    if message.content.lower().startswith('/vercao'):
        await client.send_message(message.channel, "```GamingBOT                                                                                                                                                                                                                            Verção : 0.1.4```")
    if message.content.lower().startswith('/vom'):
        choice = random.randint(1,2)
        if choice == 1:
            await client.send_message(message.channel, "Verdade")
        if choice == 2:
            await client.send_message(message.channel, "Mentira")

    if message.content.lower().startswith('/instagram'):
        await client.add_reaction(message, emoji='✅')
        await client.add_reaction(message, emoji='❌')
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
    #limpar
    qntdd = int

    def toint(s):
        try:
            return int(s)
        except ValueError:
            return float(s)
    if message.content.lower().startswith('/limpar'):
        if message.author.id == "369962464613367811":
            qntdd = message.content.strip('/limpar ')
            qntdd = toint(qntdd)
            if qntdd <= 100:
                msg_author = message.author.mention
                await client.delete_message(message)
                #await asyncio.sleep(1)
                deleted = await client.purge_from(message.channel, limit=qntdd)
                botmsgdelete = await client.send_message(message.channel, 'Deletei {} mensagens de um pedido de {} para {}'.format(len(deleted), qntdd, msg_author))
                await asyncio.sleep(5)
                await client.delete_message(botmsgdelete)

            else:
                botmsgdelete = await client.send_message(message.channel,'Utilize o comando digitando /delete <numero de 1 a 100>')
                await asyncio.sleep(5)
                await client.delete_message(message)
                await client.delete_message(botmsgdelete)
        else:
            await client.send_message(message.channel, 'Você não tem permissão para executar esse comando')
    #tags games
    if message.content.lower().startswith('/tag add notificar'):
        cargo = discord.utils.get(message.author.server.roles,name='Notificar')
        await client.add_roles(message.author,cargo)
        await client.send_message(message.channel, "Cargo **Notificar** Setado ")
    if message.content.lower().startswith('/tag add csgo'):
        cargo = discord.utils.get(message.author.server.roles,name='cs-go')
        await client.add_roles(message.author,cargo)
        await client.send_message(message.channel, "Cargo **Cs-Go** Setado ")
    if message.content.lower().startswith('/tag add LoL'):
        cargo = discord.utils.get(message.author.server.roles,name='lol')
        await client.add_roles(message.author,cargo)
        await client.send_message(message.channel, "Cargo **lol** Setado ")
    #tags coloridas
    if message.content.lower().startswith('/tag add red'):
        cargo = discord.utils.get(message.author.server.roles,name='red')
        await client.add_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Red** Setada")
    if message.content.lower().startswith('/tag add blue'):
        cargo = discord.utils.get(message.author.server.roles,name='blue')
        await client.add_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Blue** Setada")
    if message.content.lower().startswith('/tag add green'):
        cargo = discord.utils.get(message.author.server.roles,name='green')
        await client.add_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Green** Setada")
    #remoção das tags
    if message.content.lower().startswith('/tag remove green'):
        cargo = discord.utils.get(message.author.server.roles,name='green')
        await client.remove_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Green** Removida")
    if message.content.lower().startswith('/tag remove red'):
        cargo = discord.utils.get(message.author.server.roles,name='red')
        await client.remove_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Red** Removida")
    if message.content.lower().startswith('/tag remove blue'):
        cargo = discord.utils.get(message.author.server.roles,name='blue')
        await client.remove_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Blue** Removida")
    if message.content.lower().startswith('/lula'):
        await client.send_message(message.channel, "https://abrilveja.files.wordpress.com/2018/03/brasil-politica-ex-presidente-lula-20180301-004-copy.jpg")
    if message.content.lower().startswith('/ping') and not message.author.id == '415640814371340288':
        d = datetime.utcnow() - message.timestamp
    s = d.seconds * 1000 + d.microseconds // 1000
    await client.send_message(message.channel, '🏓 Pong! {}ms'.format(s))
client.run(token)

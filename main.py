import discord
import asyncio
import random
import aiohttp
import os
import secreto
import re
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
        game=discord.Game(name="L!ajuda | Estou ON em " + str(len(client.servers)) + " servidores!", type=0))

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
    embed = discord.Embed(title='LoriS - Bans', description='Algum moderador baniu o membro **@{0.name}** do servidor!\n\nBem Feito :P'.format(user), color=vermelho)
    #Para exibir o gif do thor: (se quiser apagar é escolha sua
    embed.set_image(url='https://im4.ezgif.com/tmp/ezgif-4-78bb814d9d.gif')
    embed.set_thumbnail(url='https://escolavoando.com.br/images/logo.png')
    #Manda a mensagem no canal
    await client.send_message(channel, embed=embed)
@client.event
async def on_message(message):
    #chat
    if message.content.lower().startswith('l!cat'):
        async with aiohttp.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                canal = message.channel
                await client.delete_message(message)
                await client.send_message(canal, js['file'])
    if message.content.lower().startswith('l!dog'):
        async with aiohttp.get('https://random.dog/woof.json') as r:
            if r.status == 200:
                js = await r.json()
                canal = message.channel
                await client.send_message(canal, js['url'])
                await client.delete_message(message)
    if message.content.lower().startswith('l!oi'):
        await client.send_message(message.channel, "Olá ")
    if message.content.lower().startswith('l!mutar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, 'Você não tem permissão para executar esse comando!')
        mention1 = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles,name='Mutado')
        await client.add_roles(mention1, cargo)
        await client.send_message(message.channel, "Player mutado com SUCESSO :D")
    if message.content.lower().startswith('a loris ta on?'):
        await client.send_message(message.channel, "se eu to falando contigo '-'")
    if message.content.lower().startswith('l!voar'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            description='está voando',
        )
        embed.set_author(name= message.author.name)
        embed.set_image(url= 'http://www.gifmania.com.br/Gif-Animados-Quadrinhos/Animacoes-Superman/Imagens-Superman-Voando/Superman-Voando-87265.gif')
        await client.send_message(message.channel, embed=embed)
    elif message.content.lower().startswith('l!avatar'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            description="**[Clique aqui](" + message.author.avatar_url + ") para acessar o link de seu avatar!**"
            ,
        )
        embed.set_author(name=message.author.name)
        embed.set_image(url=message.author.avatar_url)
        await client.send_message(message.channel, embed=embed)
        
    elif message.content.lower().startswith('l!perfil'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            description='money: xx                                                                                                                                                                                       tags: xx                                                                                                                                                                                       rep: xx',
        )
        embed.set_author(name=message.author.name)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text='id: '+ message.author.id)
        await client.send_message(message.channel, embed=embed)
    if message.content.lower().startswith('l!pete'):
        await client.send_message(message.channel, "'-'")
    if message.content.lower().startswith('l!repete'):
        await client.send_message(message.channel, "'-'")
    if message.content.lower().startswith('l!hacker'):
        await client.send_message(message.channel, ":P")
    if message.content.lower().startswith('l!botinfo'):
        embed = discord.Embed(
            title=None,
            color=vermelho,
            description=None
        )
        embed.set_author(name="BotINFO")
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name="Meu Nome: ",value=client.user.name)
        embed.add_field(name="Meu ID: ",value=client.user.id)
        embed.add_field(name="Estou conectada em: ",value=str(len(client.servers)) + ' servidores')
        embed.add_field(name="Em Contato com:",value=str(len(set(client.get_all_members()))) + ' usuarios')
        embed.set_footer(text="Meu criador:Ph4#3931 Meu prefixo: L! Quer saber mais sobre mim? utilize L!ajuda")
        await client.send_message(message.channel,embed=embed)
    if message.content.lower().startswith('l!tag list'):
        await client.send_message(message.channel,
        embed=discord.Embed(title="Tags - list", description="red,blue,green,csgo,lol",color=0xbb0021))
    if message.content.lower().startswith('l!tags'):
        await client.send_message(message.channel,
        embed=discord.Embed(title="LoriS - Tags", description="l!tag list - Lista de Tags                                                                                                                                                                                       l!tag add (tag) - adicionar uma tag                                                                                                                                                                                       l!tag remove (tag) - remover uma tag", color=0xbf0022))
    #ajuda
    if message.content.lower().startswith("l!ajuda"):
        await client.send_message(message.author,
        embed=discord.Embed(
        title="LoriS - Ajuda",
        color=vermelho,
        description="l!vom (msg) - Verdade ou Mentira \n"
                    "l!hacker - O Maior hacker da história (vai ser removido) \n"
                    "l!moeda - Cara ou Coroa \n"
                    "l!dog - Imagens de Cachorro \n"
                    "l!cat - Imagens de Gato \n"
                    "l!nv - Nivel de Doidice \n"
                    "l!limpar (0 a 100) [administrador] \n"
                    "l!tags - Como deixar seu nome colorido \n"
                    "l!perfil - Veja seu Perfil (beta) \n"
                    "l!avatar - Veja seu lindo avatar \n"
                    "l!voar - Voe que nem um passarinho \n"
                    "l!vercao - Verção do bot \n"
                    "l!nv - Veja seu nivel de doidice \n"
                    "l!link - Adquira o link do bot \n"
                    "l!ping - Pong \n"
                    "l!mutar - Mute :D {adminstradores}\n"
                    "l!instagram (img) - Deixe as pessoas avaliarem suas fotos ",))
        await client.send_message(message.channel,
            embed=discord.Embed(
                title="LoriS - Ajuda",
                color=vermelho,
                description="os comandos foram enviados para seu privado :) " + message.author.mention
            ))
        await client.delete_message(message)
    if message.content.lower().startswith('l!versao'):
        await client.send_message(message.channel, "```Loris                                                                                                                                                                                                                            Versão : 0.1.4```")
    if message.content.lower().startswith('l!vom'):
        choice = random.randint(1,2)
        if choice == 1:
            await client.send_message(message.channel, "Verdade")
        if choice == 2:
            await client.send_message(message.channel, "Mentira")

    if message.content.lower().startswith('l!instagram'):
        await client.add_reaction(message, emoji='✅')
        await client.add_reaction(message, emoji='❌')
    if message.content.lower().startswith('l!nv'):
        choice = random.randint(1,4)
        if choice == 1:
            await client.send_message(message.channel, "Você tem 20% de doidice")
        if choice == 2:
            await client.send_message(message.channel, "Você tem 80% de doidice")
        if choice == 3:
            await client.send_message(message.channel, "Você tem 40% de doidice")
        if choice == 4:
            await client.send_message(message.channel, "Você tem 100% de doidice")

    if message.content.lower().startswith('l!moeda'):
        choice = random.randint(1,2)
        if choice == 1:
            await client.add_reaction(message, '😀')
        if choice == 2:
            await client.add_reaction(message, '👑')

    if message.content.lower().startswith('l!link'):
        await client.send_message(message.channel, "Link do Bot:")
        await client.send_message(message.channel, "https://discordapp.com/oauth2/authorize?client_id={}&permissions=8&scope=bot".format(client.user.id))
    #limpar
    qntdd = int

    def toint(s):
        try:
            return int(s)
        except ValueError:
            return float(s)
    if message.content.lower().startswith('l!limpar'):
        if message.author.id == "369962464613367811":
            qntdd = message.content.strip('l!Limpar ')
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
    if message.content.lower().startswith('l!tag add notificar'):
        cargo = discord.utils.get(message.author.server.roles,name='Notificar')
        await client.add_roles(message.author,cargo)
        await client.send_message(message.channel, "Cargo **Notificar** Setado ")
    if message.content.lower().startswith('l!tag add csgo'):
        cargo = discord.utils.get(message.author.server.roles,name='cs-go')
        await client.add_roles(message.author,cargo)
        await client.send_message(message.channel, "Cargo **Cs-Go** Setado ")
    if message.content.lower().startswith('l!tag add LoL'):
        cargo = discord.utils.get(message.author.server.roles,name='lol')
        await client.add_roles(message.author,cargo)
        await client.send_message(message.channel, "Cargo **lol** Setado ")
    #tags coloridas
    if message.content.lower().startswith('l!tag add red'):
        cargo = discord.utils.get(message.author.server.roles,name='red')
        await client.add_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Red** Setada")
    if message.content.lower().startswith('l!tag add blue'):
        cargo = discord.utils.get(message.author.server.roles,name='blue')
        await client.add_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Blue** Setada")
    if message.content.lower().startswith('l!tag add green'):
        cargo = discord.utils.get(message.author.server.roles,name='green')
        await client.add_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Green** Setada")
    #remoção das tags
    if message.content.lower().startswith('l!tag remove green'):
        cargo = discord.utils.get(message.author.server.roles,name='green')
        await client.remove_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Green** Removida")
    if message.content.lower().startswith('l!tag remove red'):
        cargo = discord.utils.get(message.author.server.roles,name='red')
        await client.remove_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Red** Removida")
    if message.content.lower().startswith('l!tag remove blue'):
        cargo = discord.utils.get(message.author.server.roles,name='blue')
        await client.remove_roles(message.author, cargo)
        await client.send_message(message.channel, "Tag **Blue** Removida")
    if message.content.lower().startswith('l!lula'):
        await client.send_message(message.channel, "https://abrilveja.files.wordpress.com/2018/03/brasil-politica-ex-presidente-lula-20180301-004-copy.jpg")
    if message.content.lower().startswith('l!ping') and not message.author.id == '415640814371340288':
        d = datetime.utcnow() - message.timestamp
    s = d.seconds * 1000 + d.microseconds // 1000
    await client.send_message(message.channel, '🏓 Pong! {}ms'.format(s))
client.run(token)

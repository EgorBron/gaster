import discord
import time
import youtube_dl
import os
import requests
import io
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = '>')
client.remove_command('help')

@client.event

async def on_ready():
    print('bot connected')
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('>help'))

@client.event
async def on_member_join(member: discord.Member):
    start_role = discord.utils.get(member.guild.roles, id = 752081884485255229)
    await member.add_roles(start_role)
    print('Пользователь', member, 'присоединился!')

@client.command(pass_context = True)

async def hello(ctx):
    author = ctx.message.author
    
    await ctx.send(f'{author.mention}, привет!')

@client.command(pass_context = True)

async def echo(ctx, arg):
    author = ctx.message.author
    
    await ctx.send(f'{author.mention}' + arg)

@client.command(pass_context = True)
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 0, botmsg = 1):
    await ctx.channel.purge(limit = amount + 1)
    await ctx.send(f'Успешно удалено {amount} сообщений')
    time.sleep(5)
    await ctx.channel.purge(limit = botmsg)

@client.command(pass_context = True)
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = 'не указана'):
    await member.kick(reason = reason)
    await ctx.send(f'{member.mention} был кикнут')

@client.command(pass_context = True)
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = 'не указана'):
    await member.ban(reason = reason)
    await ctx.send(f'{member} был забанен. Причина: {reason}')

@client.command(pass_context = True)
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user1 = ban_entry.user
    await ctx.guild.unban(user1)
    await ctx.send(f'{user1} был разбанен.')
    return



@client.command()
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member: discord.Member, mutetime = int(), mutereason = 'не указана'):
    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} получил ограничение чата на {mutetime} секунд. Причина: {mutereason}')
    if(mutetime == 0):
        pass
    else:
        time.sleep(mutetime)
        await member.remove_roles(mute_role)
        await ctx.send(f'У {member.mention} было снято ограничение чата')

@client.command()
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    await member.remove_roles(mute_role)
    await ctx.send(f'У {member.mention} было снято ограничение чата')
    await ctx.member.send('Вы были размучены на сервере "Minecraft (aka. Бэд варсеры)"')

@client.command(pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'Помощь по командам:', description = 'Тут находится информация о всех командах', colour = discord.Colour.blue())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_thumbnail(url = 'https://banner2.cleanpng.com/20180509/qkw/kisspng-logo-brand-line-5af34a373377c6.4685030215258936872108.jpg')
    emb.set_footer(text = 'Бот дорабатывается и может содержать ошибки')
    emb.add_field(name = 'Мой префикс - >', value = 'Не забудь его!')
    emb.add_field(name = '>clear', value = 'Очистка чата')
    emb.add_field(name = '>ban @упоминание [время] [причина]', value = 'Блокировка (бан) пользователя')
    emb.add_field(name = '>unban @упоминание', value = 'Разблокировка (разбан) пользователя')
    emb.add_field(name = '>kick @упоминание', value = 'Выгнать (кикнуть) пользователя с сервера')
    emb.add_field(name = '>echo', value = 'Повторяет текст комманды')
    emb.add_field(name = '>mute @упоминание [время в секундах или 0] [причина]', value = 'Мутит (ограничевает доступ в чаты) пользователю')
    emb.add_field(name = '>unmute @упоминание', value = 'Размучивает пользователя')
    await ctx.send(embed = emb)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Отсутствует один или несколько аргументов для команды')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У Вас нет разрешений на эту команду!')
    else:
        pass

@ban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Отсутствует один или несколько аргументов для команды')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У Вас нет разрешений на эту команду!')
    else:
        pass

@unban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Отсутствует один или несколько аргументов для команды')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У Вас нет разрешений на эту команду!')
    else:
        pass

@mute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Отсутствует один или несколько аргументов для команды')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У Вас нет разрешений на эту команду!')
    else:
        pass

@unmute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Отсутствует один или несколько аргументов для команды')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У Вас нет разрешений на эту команду!')
    else:
        pass

@kick.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Отсутствует один или несколько аргументов для команды')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У Вас нет разрешений на эту команду!')
    else:
        pass

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Успешное подключение к {channel}')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Успешное отключение от {channel}')

@client.command() 
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            print('Файл удалён')
    except PermissionError:
            print('Удалить файл не получилось')
    await ctx.send('Пожалуйста, подождите')
    voice = get(client.voice_clients, guild = ctx.guild)
    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192',
        
            }]
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Загружаю музыку...')
        ydl.download([url])
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print('Переименовываю файл: {file}')
            os.rename(file, song.mp3)
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'Проигрывание "{name}" окончено'))
    voice3.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    nname = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')

level = 1

@client.command()
async def lic(ctx):
    img = Image.new('RGBA', (400, 150), '#1b1e38')
    url = str(ctx.author.avatar_url)[:-10]
    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)
    img.paste(response, (15, 15, 115, 115))
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator
    headline = ImageFont.truetype('arial.ttf', size = 20)
    levelline = ImageFont.truetype('arial.ttf', size = 15)
    underline = ImageFont.truetype('arial.ttf', size = 12)
    idraw.text((145, 15), f'{name}#{tag}', font = headline)
    idraw.text((145, 40), f'Ваш уровень: {level}', font = levelline)
    idraw.text((145, 65), f'Уровень не рабоает', font = underline)
    img.save('infocard.png')
    await ctx.send(file = discord.File(fp = 'infocard.png'))
    
token = 'NzU0NzI1NDQ2NTU3NDk5Mzkz.X1462A.Ma3jvZanDBKvzjPtlN9fF4hvGF0'

client.run(token)

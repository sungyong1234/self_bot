import discord
from config import *
from discord.ext import commands
import asyncio, datetime
import requests, random, string
import os, urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

command_prefix = 접두사 #건들지말것
bot = commands.Bot(self_bot=True, command_prefix=command_prefix) #건들지말것

token = 사람토큰 #건들지말것

def serverinfo(server):
    g = bot.get_guild(int(server))
    gname = g.name
    gm = g.member_count
    a = f'> **{gname} : {gm}명**'
    return a

def getinfo(id):
    url = f"https://discordapp.com/api/users/{id}"
    he = {
        "Authorization": "Bot OTUzOTU3ODQ5NjEwOTg5NjI4.YjMIew.6i1CHy0S2esTDsX1nsMHOAe6y1c" #건들지말것
    }
    res = requests.get(url, headers=he)
    r = res.json()
    return r

@bot.event
async def on_ready():
    print(f"Login Success {bot.user}")
    if 상메무한반복 == True:
        while True:
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=상메1))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=상메2))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=상메3))
            await asyncio.sleep(10)
    else:
        await bot.change_presence(activity=discord.Streaming(name="Connecting...", url="https://www.twitch.tv/faker"))

@bot.command()
async def ping(ctx):
    await ctx.send(f'> **__pong__** {round(bot.latency*1000)} ms')

@bot.command()
async def 계좌(ctx):
    await ctx.message.delete()
    await ctx.send(f'> **{계좌정보}**') #수정

@bot.command()
async def 봇(ctx, *, rec):
    await ctx.message.delete()
    await ctx.send(f'> https://discord.com/oauth2/authorize?client_id={rec}&permissions=8&scope=bot')

@bot.command()
async def 정보(ctx, *, id):
    try:
        try:
            m = id
            m1 = m.split('@')[1]
            m2 = m1.split('>')[0]
            id = m2.split('!')[1]
        except:
            id = id
        res = getinfo(id)
        name = res['username']
        de = res['discriminator']
        icon = res['avatar']
        ba = res['banner_color']
        if icon != None:
            if "a_" in icon:
                iconurl = f"https://cdn.discordapp.com/avatars/{id}/{icon}.gif?size=1024"
            else:
                iconurl = f"https://cdn.discordapp.com/avatars/{id}/{icon}.png?size=1024"
        else:
            iconurl = "https://cdn.discordapp.com/embed/avatars/0.png"
        member = await bot.fetch_user(int(id))
        date_format = "%Y년 %m월 %d일 %H시 %M분 %S초"
        aa = member.created_at.strftime(date_format)
        banner = res['banner']
        if banner != None:
            if "a_" in banner:
                bannerurl = f"https://cdn.discordapp.com/banners/{id}/{banner}.gif?size=1024"
                await ctx.reply(f'> `유저이름` : {name}#{de}\n'
                                f'> `유저아이디` : {id}\n'
                                f'> `프로필` : ||{iconurl}||\n'
                                f'> `가입한날` : {aa}\n'
                                f'> `배너색` : {ba}\n'
                                f'> `배너사진` : ||{bannerurl}||')
            else:
                bannerurl = f"https://cdn.discordapp.com/banners/{id}/{banner}.png?size=1024"
                await ctx.reply(f'> `유저이름` : {name}#{de}\n'
                                f'> `유저아이디` : {id}\n'
                                f'> `프로필` : ||{iconurl}||\n'
                                f'> `가입한날` : {aa}\n'
                                f'> `배너색` : {ba}\n'
                                f'> `배너사진` : {bannerurl}')
        else:
            await ctx.reply(f'> `유저이름` : {name}#{de}\n'
                            f'> `유저아이디` : {id}\n'
                            f'> `프로필` : ||{iconurl}||\n'
                            f'> `가입한날` : {aa}\n'
                            f'> `배너색` : {ba}\n'
                            f'> `배너사진` : None')
    except:
        await ctx.reply("> 존재하지않는 사용자입니다.")

@bot.command()
@commands.has_permissions(ban_members = True)
async def 벤(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"> {member} 님을 `성공적으로` __영구차단하였습니다.__")

@bot.command(name="벤해제", help="유저를 벤 해제합니다.")
@commands.has_permissions(administrator=True)
async def _unban(ctx, *, member_id: int):
    await ctx.guild.unban(discord.Object(id=member_id))
    await ctx.send(f"> <@{member_id}> 님을 `성공적으로` __차단해제하였습니다.__")

@bot.command(name="역할생성", help="뒤에 있는 역할 이름으로 역할을 생성합니다.")
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'역할 `{name}` 이 만들어졌습니다.')

@bot.command()
async def 수정(ctx):
    msg = await ctx.send("곧 사라질 메시지")
    await asyncio.sleep(1)
    await msg.edit(content=f"**{ctx.prefix}{ctx.command}**")

@bot.command(pass_context=True)
async def 역할(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"> `{user}`님에게 `{role.name}`역할이 성공적으로 지급되었습니다.")

@bot.command()
async def 서버(ctx, *, server):
    await ctx.message.delete()
    a = serverinfo(server)
    await ctx.send(f'{a}')

@bot.command()
async def 채널(ctx):
    if ctx.guild != None:
        await ctx.send(f"> `{ctx.guild}` -> `{ctx.channel}` -> `{ctx.channel.id}`")
    else:
        await ctx.send(f"> `{ctx.channel}` -> `{ctx.channel.id}`")

@bot.command()
async def 시간(ctx):
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day
    h = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    msg = await ctx.reply(f'> 시간정보 : __{y}년 {m}월 {d}일 {h}시 {min}분__')

@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount):
    if int(amount) <= 10:
        await ctx.channel.purge(limit=int(amount))
        await ctx.send(f"> `{amount}`개 청소가 __완료되었습니다__")
    else:
        await ctx.send(f"> `{amount}`개는 셀프봇으로 청소하기에 너무 __큰숫자입니다.__\n\n> `10`개 __이하로__ 입력해주세요.")

@bot.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    msg = await ctx.send(f"> **`오류`가 발생하였습니다.**\n\n> __{error}__")
    await msg.add_reaction('❌')

@bot.command()
async def 상메(ctx, *, text):
  await bot.change_presence(activity=discord.Game(name=f'{text}'))
  await ctx.send(f"> 상태메시지가 `{text}`로 성공적으로 __변경되었습니다.__")

@bot.command()
async def 주사위(ctx):
    com = random.choice(["1", "2", "3", "4", "5", "6"])
    await ctx.send(f"{ctx.author.mention}님 랜덤주사위 결과는 {com}입니다 🎲")

@bot.command()
async def 루트(ctx, *, dd):
    a = ("{:g}".format(int(dd) ** (1 / 2)))
    await ctx.reply(f"> `{a}`")

@bot.command()
async def 약수(ctx, *, n):
    i = 1
    list_a = []
    if len(str(n)) <= 5:
        while i <= int(n):
            if int(n) % i == 0:
                list_a.append(i)
            i += 1
    await ctx.reply(f"> `{list_a}`")
@bot.command()
async def 메스핑(ctx):
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.members
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.mention)
        except:
            break
    if len(target) >= 4000:
        await ctx.send('유저가 너무 마나!!')
    else:
        await ctx.send("".join(target))

@bot.command()
async def 멤버파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching Member...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.members
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('memberparse.txt', 'w', encoding='utf-8-sig')
    with open('memberparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"memberparse.txt"))
    os.remove(f"memberparse.txt")
@bot.command()
async def 이모지파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching emoji...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.emojis
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('emojiparse.txt', 'w', encoding='utf-8-sig')
    with open('emojiparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"emojiparse.txt"))
    os.remove(f"emojiparse.txt")
@bot.command()
async def 메시지파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching message...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.messages
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('emojiparse.txt', 'w', encoding='utf-8-sig')
    with open('emojiparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"emojiparse.txt"))
    os.remove(f"emojiparse.txt")
@bot.command()
async def 채널파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching Channel...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.channels
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('channelparse.txt', 'w', encoding='utf-8-sig')
    with open('channelparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"channelparse.txt"))
    os.remove(f"channelparse.txt")
@bot.command()
async def 역할파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching Role...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.roles
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('roleparse.txt', 'w', encoding='utf-8-sig')
    with open('roleparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"roleparse.txt"))
    os.remove(f"roleparse.txt")
@bot.command()
async def 명령어(ctx):
    await ctx.send("> `ping` = 컴의 `핑`을 확인할수있습니다."
             "\n> `계좌` = 설정해논 `계좌`를 명령어로 불러옵니다."
             "\n> `봇` `봇아이디` = 봇아이디로 `봇초대링크`를 만들어서 불러옵니다."
             "\n> `벤` `유저멘션` = 멘션당한유저를 서버에서 `영구차단`합니다."
             "\n> `벤해제` `유저아이디` = 유저아이디에 해당하는 유저를 서버에서 `영구차단해제`를 합니다."
             "\n> `역할생성` `역할이름` = 역할이름으로 된 역할을 `생성`합니다."
             "\n> `역할` `유저멘션` `역할이름` = 역할이름으로 된 역할을 멘션당한 유저에게 `지급`합니다."
             "\n> `상메` `바꿀상메` = `상태메시지`를 적은 메시지로 바꿉니다."
             "\n> `서버` `서버아이디` = 서버아이디에 해당한 서버의 `인원수`를 불러옵니다."
             "\n> `채널` = 명령어를 쓴 `채널`의 정보를 불러옵니다."
             "\n> `시간` = 명령어를 쓴 `시간`의 정보를 불러옵니다."
             "\n> `청소` `숫자` = 숫자만큼 해당채널의 메시지를 `청소`합니다."
             "\n> `루트` `숫자` = 숫자의 `제곱근`을 불러옵니다."
             "\n> `약수` `숫자` = 숫자의 `약수`를 불러옵니다."
             "\n> `토큰만` `이멜:비번:토큰` = 받은토큰을 `토큰만` 출력합니다."
             "\n> `토큰체킹` `토큰` = 받은토큰을 `체킹`하여 사용가능한지 나타냅니다."
             "\n> `문상` `핀번호` = 핀번호로 문상을 `충전`합니다."
             "\n> `돈` = 설정한 컬쳐랜드아이디의 `잔액`을 불러옵니다."
             "\n> `웹훅생성` = 메시지를 친 채널의 `웹훅`을 `생성`합니다."
             "\n> `출금` `액수` = 액수만큼 문상을 `출금`합니다."
             "\n> `정보` `멘션혹은 아이디` = 대상의 `정보`를 불러옵니다."
             "\n> `검색` `검색할것` = 검색할것을 봇이 네이버에 `검색`하고 스샷해서 보여줍니다"
             "\n> `웹` `웹주소` = 웹주소의 `웹 소스를 파싱`해서 html파일형태로 출력합니다."
            f"\n> \n> __접두사__ = {command_prefix}")

@bot.command()
async def 토큰만(ctx, *, tk):
    open('tokens.txt', 'w')
    with open('tokens.txt','w') as f:
        f.write(tk)
    with open('tokens.txt','r') as f:
        tokens=f.read().split('\n')
    go=[]
    for token in tokens:
        try:
            if not token=='':
                tokenone=token.split(':')[2]
        except:
            print('이메일:비밀번호:토큰 순으로 입력해주세요')
            print('========================================================')
            exit()
        go.append(tokenone)
    with open('tokens.txt','w') as f:
        f.write('\n'.join(go))
    await ctx.send(file=discord.File(f"tokens.txt"))
    os.remove(f"tokens.txt")

@bot.command()
async def 토큰체킹(ctx, *, token):
    try:
        token = token.split(":")[2]
    except:
        token = token
    headers = {'Content-Type': 'application/json', 'authorization': token}
    url = "https://discordapp.com/api/v6/users/@me/library"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        await ctx.reply(f"> 이 토큰은 사용가능합니다. :key: ")
    else:
        await ctx.reply("> 이 토큰은 사용불가능합니다. :lock:")

@bot.command()
async def 문상(ctx, *, msg):
    try:
        jsondata = {"token": api키, "id": 컬쳐아디, "pw": 컬쳐비번, "pin": msg}
        res = requests.post("", json=jsondata)
    except:
        try:
            await ctx.reply("> 문화상품권 충전 실패\n> \n> 일시적인 서버 오류입니다.\n> 잠시 후 다시 시도해주세요.")
        except:
            pass
        return None
    res = res.json()
    if res["result"] == True:
        try:
            culture_fee = int(0)
            culture_amount = int(res["amount"])
            culture_amount_after_fee = culture_amount - int(culture_amount * (culture_fee / 100))
            await ctx.reply(
                f"> 문화상품권 충전 성공\n> \n> 핀코드: `{msg}`\n> 금액: `{culture_amount}`원\n> 충전한 금액: `{culture_amount_after_fee}`")
        except:
            pass

    else:
        await ctx.reply("> 문화상품권 충전 실패\n> \n> 실패 사유 : " + res["reason"])
@bot.command()
async def 이모지(ctx, *, mes):
    msg = await ctx.send(f"{mes}")
    await msg.add_reaction('🎁')

@bot.command()
async def 웹훅생성(ctx):
    ch = bot.get_channel(int(ctx.channel.id))
    webhook = await ch.create_webhook(name=ctx.author, reason='배너봇 자동개설')
    await ctx.reply('웹훅 생성해왔습니다\n' + webhook.url)

@bot.command()
async def 검색(ctx, *, 검색할것):
    naver_url = "https://naver.com"

    options = Options()

    if 검색할것 != "코로나":
        options.add_argument('headless')
        options.add_argument('--start-maximized')
        browser = webdriver.Chrome("./chromedriver.exe", options=options)
        browser.get(naver_url)

        검색창 = browser.find_element_by_css_selector("#query")
        검색창.send_keys(검색할것)

        검색버튼 = browser.find_element_by_css_selector("#search_btn")
        검색버튼.click()

        screenshot = browser.save_screenshot(검색할것 + '.png')
        browser.quit()
        await ctx.reply(file=discord.File(검색할것 + '.png'))
        os.remove(검색할것 + '.png')
    else:
        options.add_argument('headless')
        options.add_argument('--start-maximized')
        browser = webdriver.Chrome("./chromedriver.exe", options=options)
        browser.get(naver_url)

        검색창 = browser.find_element_by_css_selector("#query")
        검색창.send_keys(검색할것)

        검색버튼 = browser.find_element_by_css_selector("#search_btn")
        검색버튼.click()

        element1 = browser.find_element_by_class_name('status_info')
        element_png = element1.screenshot_as_png
        with open(검색할것 + '.png', "wb") as file:
            file.write(element_png)
        browser.quit()
        await ctx.reply(file=discord.File(검색할것 + '.png'))
        os.remove(검색할것 + '.png')
@bot.command()
async def 웹(ctx, url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    open('parse.html', 'w', encoding='utf-8-sig')
    with open('parse.html', 'w', encoding='utf-8-sig') as f:
        f.write(str(soup))
    await ctx.send(file=discord.File(f"parse.html"))
    os.remove(f"parse.html")

@bot.command()
async def 토큰(ctx, *, target):
    first = ('').join(random.choices(string.ascii_letters + string.digits, k=24))
    second = ('').join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=6))
    end = ('').join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=25))
    token = f"OT{first}.{second}.{end}"
    await ctx.reply(f"> {target}님의 토큰입니다.\n> \n> {token}")
bot.run(token, bot=False)

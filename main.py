import httpx,requests,discord,threading, socks, random, json, tracemalloc, asyncio;from dotenv import load_dotenv; from discord.ext import commands
tracemalloc.start()

# BY OXYN :1 https://discord.gg/7sS97Kp6hq

def get_config():
    config_file = open("config.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_prefix():
    config_file = get_config()
    config = json.loads(config_file)
    prefix = config['bot_config']["prefix"] 
    return prefix

config_file = get_config()
config = json.loads(config_file)
prefix = config['bot_config']["prefix"]
token = config['bot_config']["token"]

load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=get_prefix(), help_command=None, intents=intents)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()
    

@bot.command()
async def stock(ctx, arg):
    if arg == "twitch":
        filefile = open('tokens.txt')
        fnum_lines = sum(1 for line in filefile)
        filefile.close()
        embed=discord.Embed(title="Stock",color=6546546, description=f"**STOCK**\n `{fnum_lines}` LOADED")
        await ctx.send(embed=embed)

def get_id(user):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        session = requests.Session()
        response = session.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        print(response.text)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None
    
@bot.command()
async def tfollow(ctx, arg):
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel =json_object['bot_config']["twitch_channel"]
    if ctx.channel.id == int(genchannel):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                target_id = get_id(arg)

                if target_id == None:
                    embed=discord.Embed(color=6546546, description=f"**ERROR** `ID SCRAPE ERROR {arg}`")
                    await ctx.send(embed=embed)
                    break
                
                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                filefile = open('tokens.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                if num_lines < follow_count:
                    embed=discord.Embed(color=6546546, description=f"**SENDING** `{num_lines}` FOLLOWERS TO `{arg}`")
                    await ctx.send(embed=embed)
                    caunt_to_follow = num_lines
                else:
                    embed=discord.Embed(color=6546546, description=f"**SENDING** {follow_count} FOLLOWERS TO `{arg}`")
                    await ctx.send(embed=embed)
                    caunt_to_follow = follow_count
                class Follow():
                    sent = 0
                        
                def start_follow():
                    for i in range(caunt_to_follow):
                        try:
                            session = requests.Session()
                            proxy = random.choice(open("proxy.txt","r").read().splitlines())
                            proxies = {"https": f"http://{proxy}"}
                            ttoken = tokens[i]
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                            if get_config['follow_proxy'] == True:
                                session.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies=proxies, timeout=30)
                            else:
                                session.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        except: None
                x = threading.Thread(target=start_follow)
                x.start()
                break
                

@bot.command()
async def tspam(ctx, arg1, *, args):
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]  
    if ctx.channel.id == int(genchannel): 
        role_config = json.loads(config_file)['tspam']
        for role_name in role_config:
            spam_count = json_object['tspam'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('tokens.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    embed=discord.Embed(color=6546546, description=f"**ERROR** `ID SCRAPE ERROR {arg1}`")
                    await ctx.send(embed=embed)
                    break
                

                
                def start_spam(ttoken):
                    for i in range(2):
                        try:
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try: 
                                        session = requests.Session()
                                        proxy = random.choice(open("proxy.txt","r").read().splitlines())
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n".encode("utf8"))
                            s.send(f"PASS oauth:{ttoken}\r\n".encode("utf8"))
                            s.send(f"NICK {token_name}\r\n".encode("utf8"))
                            s.send(f"JOIN #{arg1}\r\n".encode("utf8"))
                            s.send(f"PRIVMSG #{arg1} :{args}\r\n".encode("utf8"))
                            s.close()
                        except Exception as e:
                            print(e) 
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count 
                embed=discord.Embed(color=6546546, description=f"**SENDING** {x} MESSAGES TO `{arg1}`")
                await ctx.send(embed=embed)


                filefile = open('tokens.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                filefile = open('tokens.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                try:
                    for i in range(x):
                        threading.Thread(target=start_spam, args=(tokens[i],)).start()
                except: None
                break
        
init()


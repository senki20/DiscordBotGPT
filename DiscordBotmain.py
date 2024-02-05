import discord
from discord.ext import commands
from gradio_client import Client
import asyncio
from ExtracfromPDF import extractHTML

gr=Client("http://127.0.0.1:7860")

readyforchat=False
local=False
History=[]
max_token=2048
GPT4System="You are a helpful Assistant"
url=""

generationrunning=False

with open("TOKEN.txt","r+") as file:
    token=file.readline().split(':')[1]

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)  # Use commands.Bot instead of commands.bot


def split_text(text, chunk_size=2000):
    # Ensure chunk_size is a positive integer
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    # Split the text into chunks of size chunk_size
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    return chunks
def stripMessage(ctx,command):
    command_prefix=ctx.prefix
    msg= ctx.message.content[len(command_prefix)+len(command):].strip()
    return msg




@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.command(name="test")
async def test(ctx):
    global testtxt
    print(len(testtxt))
    if len(testtxt) >=2000:
        temp = split_text(testtxt,1000)
        for i in temp:
            await ctx.send(i)
        print(temp)
    else:
        await ctx.send(testtxt)

@client.command(name="GPTCPU")
async def GPTCPU(ctx):
    global readyforchat
    global local
    gr.predict("mistral-7b-instruct-v0.1.Q4_0.gguf",False,api_name="/loadModel")
    await ctx.send("Loaded Model on CPU")
    await ctx.send("Start sending messages")
    readyforchat=True
    local=True

@client.command(name="GPT4Img")
async def GPT4Img(ctx):
    global readyforchat
    global local
    if readyforchat:
        await ctx.send("Exiting GPT")
    await ctx.send("Generating Image")
    readyforchat=False
    local=False
    msg=stripMessage(ctx,"GPT4Img")
    response = gr.predict(msg,True,api_name="/generateImage")
    await ctx.send("Generated Image:")
    print(response[3])
    await ctx.send(response[3])
    await ctx.send(f"Cost: {response[2]['label']}")

@client.command(name="debug")
async def debug(ctx):
    print(readyforchat)
    print(local)
    print(History)
    print(max_token)
    print(GPT4System)
    await ctx.send("Debugs sent to console")

@client.command(name="setTokens")
async def setToken(ctx):
    global max_token
    message = stripMessage(ctx,"setTokens")
    max_token=int(message)
    await ctx.send(f"Set max_tokens to {max_token}")

@client.command(name="getHistory")
async def getHistory(ctx):
    global History
    await ctx.send("Current History: \n"+str(History))

@client.command(name="unloadModel")
async def unloadModel(ctx):
    global readyforchat
    gr.predict(api_name="/unloadModel")
    readyforchat=False
    await ctx.send("Unloaded Model")

@client.command(name="getBalance")
async def getBalance(ctx):
    result=gr.predict(api_name="/getBalanceGUI")["label"]
    await ctx.send(result)

@client.command(name="GPT4")
async def GPT4(ctx):
    global readyforchat
    global local
    await ctx.send("Initializing GPT4")
    if local:
        gr.predict(api_name="/unloadModel")
        await ctx.send("Unloaded Model")
        local=False
        readyforchat=False
    readyforchat=True
    local=False
    await ctx.send("Ready")

@client.command(name="quit")
async def quit(ctx):
    global local
    global readyforchat
    if local:
        local=False
        readyforchat=False
        gr.predict(api_name="/unloadModel")
        await ctx.send("Unloaded Model")
    else:
        readyforchat=False
        await ctx.send("Exiting GPT4")
    

@client.command(name="debugMode")
async def debugMode(ctx):
    message = stripMessage(ctx,"setTokens")
    if message=="On" or message == "on":
        gr.predict(True,api_name="/changeDebugMode")
        await ctx.send("Debug mode: On")
    else:
        gr.predict(False,api_name="/changeDebugMode")
        await ctx.send("Debug mode: Off")

@client.command(name="clearHistory")
async def clearHistory(ctx):
    global History
    History=[]
    await ctx.send("Cleared History")

@client.command(name="setUrl")
async def setUrl(ctx):
    global url
    uri=stripMessage(ctx,"setUrl")
    url = extractHTML(uri)
    await ctx.send("Set url to:"+uri)

@client.command(name="clearUrl")
async def curl(ctx,*args):
    global url
    url=""
    await ctx.send("Cleared url")

@client.event
async def on_message(msg):
    global generationrunning
    global History
    global max_token
    global GPT4System
    global url
    if not msg.author.bot:
        print(f"{msg.author}:{msg.content}")
        if msg.content.startswith("/"):
            print("msg is a command Skipping")
            await client.process_commands(msg)
            return
        print(f"ready for chat:{readyforchat}")
        if readyforchat:
            if generationrunning:
                await msg.channel.send("Generation already Running please wait...")
                return
            else:
                print(f"islocal ? : {local}")
                if local:
                    generationrunning=True
                    await msg.channel.send("Processing Please Wait...")
                    test = gr.predict(msg.content,History,"",max_token,api_name="/localmsg")
                    generationrunning=False
                    print(test)
                    History = test
                    if len(test)>=2000:
                        temp = split_text(History[-1][1],1000)
                        for i in temp:
                            await msg.channel.send(i)
                    else:
                        await msg.channel.send(History[-1][1])
                    
                    
                else:
                    generationrunning=True
                    await msg.channel.send("Processing Please Wait...")
                    print(url)
                    fullmsg=msg.content+"\n"+url
                    test = gr.predict(GPT4System,fullmsg,History,"",True,api_name="/msg_sent")
                    if url != "":
                        History=[]
                    url=""
                    msg.channel.send("Cleared Url")
                    generationrunning=False
                    print(test)
                    print(test[0])
                    History = test[0]
                    if msg.channel.send(History[-1][1]) != "":
                        if len(History[-1][1])>=2000:
                            temp = split_text(History[-1][1],1000)
                            for i in temp:
                                await msg.channel.send(i)
                        else:
                            await msg.channel.send(History[-1][1])
                        #await msg.channel.send(History[-1][1])
                        print(test[2])
                        await msg.channel.send("Cost:"+test[2]["label"])
                        return
                    else:
                        await msg.channel.send("Empty Message Error")




client.run(token)
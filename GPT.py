from openai import OpenAI
import time
from ExtracfromPDF import extractHTML
import json
from datetime import datetime
import gradio as gr
import random

debug_mode=0
testtxt="A szöveg a Learn You a Haskell for Great Good! című oktatóanyag egy fejezetét tartalmazza, amely a Haskell programozási nyelv típusrendszereit és típusosztályait ismerteti.\n\n**Lényeges pontok:**\n- Haskell statikus típusrendszert használ: minden kifejezés típusa fordítási időben ismert, ami biztonságosabb kódot eredményez.\n- Haskell típuskövetkeztetést alkalmaz, így gyakran nem kell explicit típusmegjelölést alkalmaznunk.\n- A GHCI beépített szövegkörnyezete lehetővé teszi, hogy lekérdezzük a kifejezések típusát a `:t` parancs segítségével.\n- A Haskell alaptípusai a következők: Int, Integer, Float, Double, Bool, Char, illetve a tuple-ok.\n- A Haskell típusok a következő típusosztályokba tartozhatnak: Eq, Ord, Show, Read, Enum, Bounded, Num, `Integral`, `Floating`.\n\n**Fontos fogalmak:**\n- **Típus (Type):** Egy címke, amely azt jelöli, hogy egy kifejezés melyik kategóriájába tartozik (pl. `Bool` a logikai értékekhez, `Char` a karakterekhez).\n- **Típusosztály (Typeclass):** Egyfajta felület (interfész), amely definiál bizonyos viselkedést típusok számára (pl. `Eq` az egyenlőség tesztelésére szolgáló típusokhoz).\n- **Statikus típusrendszer (Static type system):** A típusok a fordítási időben már ismertek, ellentétben a dinamikus rendszerekkel.\n- **Típuskövetkeztetés (Type inference):** A kompilátor képes következtetni a kifejezések típusára, explicit megjelölés nélkül.\n- **Típusváltozó (Type variable):** Típusok helyett állhat, lehetővé téve a polimorf függvények létrehozását.\n\n**Típusosztályok:**\n- **Eq:** Egyenlőséget tesztelő típusokhoz.\n- **Ord:** Rendezett típusokhoz.\n- **Show:** Sztringgé alakításra képes típusokhoz.\n- **Read:** Sztringből értéket olvasó típusokhoz.\n- **Enum:** Enumerálható, sorrendben követhető típusokhoz.\n- **Bounded:** Felső és alsó határokkal rendelkező típusokhoz.\n- **Num:** Numerikus típusokhoz, amelyek számokként viselkedhetnek.\n- **Integral:** Csak egész számú típusokhoz.\n- **Floating:** Csak lebegőpontos számú típusokhoz.\n\nAz anyag megemlíti a függvénytípusokat is, kitérve arra, hogy ezek explicit típusdeklarációt kaphatnak és hogy a függvénytípusok is lekérdezhetők a `:t` parancs használatával. Az anyag emellett bemutat néhány függvényt (például `removeNonUppercase`) a megfelelő típusdeklarációkkal is."

global OPENAI_API_KEY
with open("TOKEN.txt","r+") as file:
    token=file.readline().split(':')[1]
    token=file.readline().split(':')[1]
    OPENAI_API_KEY=token

global client
client = OpenAI(api_key=OPENAI_API_KEY)
global isDiscord
isDiscordlocal=False


def changeAPIKey(key):
    global OPENAI_API_KEY
    OPENAI_API_KEY=key
    global client
    client = OpenAI(api_key=OPENAI_API_KEY)
    print(key)

def getBalance():
    values=[]
    with open("./Python/Scripts/Balance.bin","r+") as file:
        maxbalance =float(file.readline())
        current=float(file.readline())
        discordmax=float(file.readline())
        discordcurr=float(file.readline())
        values.append(maxbalance)
        values.append(current)
        values.append(discordmax)
        values.append(discordcurr)
    file.close()
    return values

def getBalanceGUI():
    values=[]
    with open("./Python/Scripts/Balance.bin","r+") as file:
        maxbalance =float(file.readline())
        current=float(file.readline())
        discordmax=float(file.readline())
        discordcurr=float(file.readline())
        values.append(maxbalance)
        values.append(current)
        values.append(discordmax)
        values.append(discordcurr)
    file.close()
    return f"{round(values[3],ndigits=10)} $ / {round(values [2],ndigits=10)}"

def saveBalance():
    with open("./Python/Scripts/Balance.bin","r+") as file:
        file.write(str(s[0])+"\n"+str(s[1])+"\n"+str(s[2])+"\n"+str(s[3]))
    file.close()

s= getBalance()

def changeDebugMode(mode):
    global debug_mode
    if mode:
        debug_mode=1
    else:
        debug_mode=0
    print(debug_mode)

#Normal AI Message Handler
def msg_sent(system, msg, history,url,isDiscord):
    global isDiscordlocal
    isDiscordlocal=isDiscord
    if msg=="" or msg==" ":
        return [(msg,"You tried to input an empty String")],gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0)
    if url:
        print(url)
        html = extractHTML(url)
        print(html)
        msg=msg+"\n\n"+html
    if not isDiscord:
        if s[1]<=0.1:
            history.append((msg,"You ran out of Balance"))
            return history,gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0)
    else:
        isDiscord=True
        if s[3]<=0.01:
            history.append((msg,"You ran out of Balance"))
            isDiscord=False
            return history,gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0)
    if debug_mode==0:
        mod = client.moderations.create(input=msg)
        print(mod.results[0].flagged)
        if mod.results[0].flagged:
            history.append(msg,"Message Moderated")
            return history,gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0)
        reply=convert_history(system, msg, history)
        AIreply = reply[0]
        cost=reply[1] 
    else:
        items=["rand1","rand2",testtxt]
        AIreply=testtxt
        cost=0
    history.append((msg, AIreply))
    isDiscord=False
    return history,gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),cost


comms = {'thread': None, 'run': None}

#Assistant AI Message Handler
def msg_sent_assistant(msg, history):
    if msg=="" or msg==" ":
        return [(msg,"You tried to input an empty String")],gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>")
    if s[0]<=0.1:
        history.append((msg,"You don't have enough balance"))
        return history,gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>")
    if not comms['thread']:
        my_assistant_list = client.beta.assistants.list()
        assistants = my_assistant_list.data
        if assistants:
            my_assistant = assistants[0]
            comms['thread'] = client.beta.threads.create()
        else:
            return [("Error", "No assistants found")],gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>")

    message = client.beta.threads.messages.create(
        thread_id=comms['thread'].id,
        role="user",
        content=msg
    )
    
    comms['run'] = client.beta.threads.runs.create(
        thread_id=comms['thread'].id,
        assistant_id=my_assistant.id,  # my_assistant must be defined in this function scope
        instructions="You are a personal math tutor. Write and run code to answer math questions."
    )
    s[0]=s[0]-0.1
    saveBalance()
    while True:
        comms['run'] = client.beta.threads.runs.retrieve(
            thread_id=comms['thread'].id,
            run_id=comms['run'].id
        )
        
        if comms['run'].status in ["completed", "failed"]:
            break
        time.sleep(3)  # Adjust sleep duration as needed

    thread_messages_response = client.beta.threads.messages.list(thread_id=comms['thread'].id)
    
    # Ensure that thread_messages_response.data contains a list and it's not empty
    if thread_messages_response.data:
        # We want the last assistant's message, assuming the responses are sorted by creation time.
        reply_msg = thread_messages_response.data[0].content[0].text.value  # Changed from [0] to [-1] to get the latest entry
        history.append((msg, reply_msg))  # Update history with the latest exchange
        return history,gr.update(value = f"<h2>Balance: {round(s[0],ndigits=10)} $/{round(s[1]*0.9,ndigits=10)} $</h2><h2> Discord Balance:{round(s[0]*0.1,ndigits=10)}/{round(s[1]*0.1,ndigits=10)}</h2>")
    else:
        return [("Error", "No reply found")],gr.update(value = f"<h2>Balance: {round(s[0],ndigits=10)} $/{round(s[1]*0.9,ndigits=10)} $</h2><h2> Discord Balance:{round(s[0]*0.1,ndigits=10)}/{round(s[1]*0.1,ndigits=10)}</h2>")

#Normal AI History Handler
def convert_history(system, msg, history):
    list = [{"role": "system", "content": f"{system}"}]
    for i in history:
        list.append(
            {"role": "user", "content": f"{i[0]}"}
        )
        list.append(
            {"role": "assistant", "content": f"{i[1]}"}
        )
    list.append({"role": "user", "content": f"{msg}"})
    for i in list:
        print(i)
    print("END\n")
    return ask_gpt(list)

#Normal AI Send to API
def ask_gpt(msg):
    global isDiscordlocal
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=msg
    )
    realusage= float(response.usage.total_tokens/1000*0.03)
    safeguard = realusage+realusage*0.10
    if isDiscordlocal:
        old=s[3]
        s[3]= s[3]-safeguard
        cost = old -s[3]
    else:
        old=s[1]
        s[1] = s[1]- safeguard
        cost= old-s[1]
    print(f"Cost:{cost},Tokens:{response.usage.total_tokens}")
    saveBalance()
    return response.choices[0].message.content,cost

#Normal AI Empty History
def empty_history(history):
    print("Removing history")
    return []

def save_history(history):
    now=datetime.now()

    text=[]
    with open(f"./History/chat{now.strftime('%Y_%m_%d_%H_%M_%S')}.json","w") as file:
        for i in history:
            text.append((
                {
                    "role":"user",
                    "content":f"{i[0]}"
                },
                {
                    "role":"assistant",
                    "content":f"{i[1]}"
                })
            )
        json.dump(text,file)
    file.close()

def load_history(file):
    file="./History/"+file
    history=[]
    with open(file,'r') as file:
        json_object = json.load(file)
        for chat in json_object:
            print(chat[0]["content"])
            print(chat[1]["content"])
            history.append((chat[0]["content"],chat[1]["content"]))
        return history

def generateImage(text,isDiscord):
    if isDiscord:
        if s[3]<0.05:
            return "",gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0),"Not Enough balance"
        s[3]=s[3]-0.05
    else:
        if s[1]<0.05:
            return "",gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0),"Not Enough balance"
        s[1]=s[1]-0.05

    saveBalance()
    mod = client.moderations.create(input=text)
    print(mod.results[0].flagged)
    if not mod.results[0].flagged:
        response = client.images.generate(
            model="dall-e-3",
            prompt=text,
            size="1024x1024",
            quality="standard",
            n=1)
        print(response)

        return response.data[0].url,gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0.05),response.data[0].url
    else:
        return "",gr.update(value = f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>"),str(0),""

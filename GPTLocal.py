from gpt4all import GPT4All
from ExtracfromPDF import extractHTML

#from gpt4all import GPT4All
#model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf") # device='amd', device='intel'
#output = model.generate("<s>[INST] What is your favorite color [/INST]</s> ", max_tokens=300)
#print(output)

global model
model = None
global prompt_template
prompt_template=""

def loadModel(name,GPU):
    global model
    global prompt_template
    print(GPU)
    if not model:
        if GPU:
            model=GPT4All(name,device="gpu")
            prompt_template="### User: \n{0}\n### Response:\n"
        else:
            model=GPT4All(name)
            prompt_template="[INST] {0} [/INST]"
        print("Loaded Model")
    else:
        print("Model already in Memory")

def unloadModel():
    global model
    if model:
        model=None
        print("Unloaded Model")

def localmsg(msg,History,uri,max_tokens):
    def processHistoryLocal(History):
        full=""
        for i in History:
            full+=prompt_template.format(i[0])+i[1]
        return full
    if model:
        global prompt_template
        input= prompt_template.format(msg)
        print(f"Input\t:{input}")
        fullInput=processHistoryLocal(History)+input
        print(f"Full input:{fullInput}")
        output=model.generate(fullInput,max_tokens=max_tokens)
        print(f"Output:\t{output}")
        History.append((msg,output))
        print(f"History:\n{History}")
        return History
    else:
        return [(msg,"Error: No Model Loaded to Memory")]

def processHistory(History):
    full=""
    for i in History:
        full+=i[0]+"\n"+i[1]
    print(f"Full:\n{full}")
    return full

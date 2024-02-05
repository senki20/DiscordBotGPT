import gradio as gr
from GPT import *
from getalljsonfromfolder import find
from GPTLocal import *


def refreshList():
    files=find()
    return gr.update(choices = files)





files = find()
s= getBalance()
with gr.Blocks(title="Chatbot") as demo:
    balance = gr.HTML(f"<h2>Balance: {round(s[1],ndigits=10)} $/{round(s[0],ndigits=10)} $</h2><h2> Discord Balance:{round(s[3],ndigits=10)}/{round(s[2],ndigits=10)}</h2>")
    with gr.Tab("Chatbot Simple"):
        system=gr.Textbox(label="System",value="You are a helpful Assistant")
        demo.allowed_paths = ["C:\\Users\\veres\\Documents\\ChatGPT API\\Icons"]
        chatbot = gr.Chatbot(height="60vh", avatar_images=("Icons/download.png", "Icons/User.svg"))
        with gr.Row():
            textbox = gr.Textbox(label="Message",scale=4,placeholder="Write your message here",container=False)
            button = gr.Button(scale=1)
            button.value = "Send"
            clear_btn = gr.Button(value="Clear")
            clear_btn.click(empty_history,inputs=chatbot,outputs=chatbot)
        with gr.Accordion(label="Extras",open=False):
            gr.HTML("<h2>Extract Text from Website</h2>")
            url = gr.Textbox(label="Url:")
            
            gr.HTML("<h2>Save/Load a chat File</h2>")
            with gr.Column():
                save = gr.Button(value="Save")
                save.click(save_history,inputs=chatbot)
                dropdown= gr.Dropdown(files,label="Load File",allow_custom_value=True)
                dropdown.input(load_history,inputs=dropdown,outputs=chatbot)
                refreshbutton=gr.Button(value="Refresh")
                refreshbutton.click(refreshList,outputs=dropdown)
            isDiscord=gr.Checkbox(label="IsDiscord",value=False)
            label=gr.Label(label="Cost")
        button.click(msg_sent, inputs=[system,textbox, chatbot,url,isDiscord], outputs=[chatbot,balance,label])
    with gr.Tab("Chatbot Assistant"):
        system=gr.Textbox(label="System Prompt",value="You are a helpful Assistant")
        demo.allowed_paths = ["C:\\Users\\veres\\Documents\\ChatGPT API\\Icons"]
        chatbot = gr.Chatbot(height="60vh", avatar_images=("Icons/download.png", "Icons/User.svg"))
        with gr.Row():
            textbox = gr.Textbox(label="Message",scale=4,placeholder="Write your message here",container=False)
            button = gr.Button(scale=1)
            button.value = "Send"
            clear_btn = gr.Button(value="Clear")
            clear_btn.click(empty_history,inputs=chatbot,outputs=chatbot)
            button.click(msg_sent_assistant, inputs=[textbox,chatbot], outputs=[chatbot,balance])
    with gr.Tab("Chatbot Local Simple") as tab:
        dropdown=gr.Dropdown(choices=["mistral-7b-instruct-v0.1.Q4_0.gguf","orca-mini-3b-gguf2-q4_0.gguf"])
        with gr.Row():
            loadmodelb=gr.Button(value="Load Model")
            unloadmodel=gr.Button(value="Unload Model")
            unloadmodel.click(unloadModel)
        chatbot=gr.Chatbot(height="60vh",avatar_images=("Icons/download.png", "Icons/User.svg"))
        with gr.Row():
                textbox = gr.Textbox(label="Message",scale=4,placeholder="Write your message here",container=False)
                button = gr.Button(scale=1,value="Send")
                clear = gr.Button(value="Clear")
                clear.click(empty_history,inputs=chatbot,outputs=chatbot)
        with gr.Accordion(label="Extras",open=False):
            useGPU=gr.Checkbox(label="Use GPU",value=False)
            gr.HTML("<h2>Extract Text from Website</h2>")
            url = gr.Textbox(label="Url:")
            max_tokens=gr.Slider(minimum=1,maximum=4096,label="Maximum Tokens",value=2048,interactive=True,step=1)
        button.click(localmsg,inputs=[textbox,chatbot,url,max_tokens],outputs=chatbot)
        loadmodelb.click(loadModel,inputs=[dropdown,useGPU])
    with gr.Tab("Document Analyzer"):
        Document=gr.Textbox(label="File")
    with gr.Tab("Image Generator"):
        text=gr.Textbox(label="Image Description")
        button = gr.Button(value="Generate")
        label=gr.Label(label="Cost")
        image = gr.Image(label="Image")
        imgurl=gr.Label(label="Url")
        with gr.Accordion(label="extras"):
            isDiscord= gr.Checkbox(label="isDiscord")
        button.click(generateImage,inputs=[text,isDiscord],outputs=[image,balance,label,url])

    with gr.Tab("Settings"):
        debug_mode = gr.Checkbox(label="Debug Mode")
        debug_mode.input(changeDebugMode,inputs=debug_mode)
        with gr.Column():
            label = gr.Label(value="")
            getBalanceButton = gr.Button(value="Get Balance")
            getBalanceButton.click(getBalanceGUI,outputs=label)
            
        with gr.Row():
            apikey=gr.Textbox(label="API_Key",type="password",scale=3)
            apply=gr.Button(value="Apply",size=1)
            apply.click(changeAPIKey,inputs=apikey)
demo.launch()

""" usee gradio as UI and build LLM APP"""
import gradio as gr
import core.config as cfg
from utils.util import get_db, get_llm, set_prompt, get_response

prompt_formet = set_prompt(cfg.KindOfPrompt.multi_QA_prompt)
llm_model = get_llm(model_path=cfg.LlmConfig.model,
                    temp=0.1,
                    max_tokens=256,
                    top_k=50,
                    top_p=0.7,
                    context_len=1024)
db_config = get_db()

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        print("Question: ", history[-1][0])
        bot_message = get_response(history[-1][0], db_config, llm_model, prompt_formet)
        print("Response: ", bot_message)
        history[-1][1] = ""
        history[-1][1] += bot_message
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot],
               queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.queue()
    demo.launch()

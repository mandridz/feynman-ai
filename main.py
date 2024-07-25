from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

proxy_url = os.getenv("OPENAI_PROXY_URL")
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key) if proxy_url is None or proxy_url == "" else OpenAI(api_key=api_key, http_client=httpx.Client(proxy=proxy_url))


# client = OpenAI(api_key=api_key)


def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "Вы Ричард Фейнман, выдающийся физик, известный своей способностью объяснять сложные концепции простым, увлекательным и понятным языком. Всегда отвечайте на русском языке."},
            {"role": "user", "content": prompt}
        ]
    )

    message = response.choices[0].message.content.strip()

    return message


def chat_with_feynman(user_input):
    if not user_input.strip():
        return "Пожалуйста, введите Ваш вопрос."

    styled_input = f"Пожалуйста, объясните эту концепцию так, как это сделал бы Ричард Фейнман:  {user_input}"
    response = generate_response(styled_input)
    return response


with gr.Blocks(css="style.css") as iface:
    gr.Markdown("# Чат с Фейнманом [Объяснятор :)]\nЗадайте любой вопрос и получите ответ в стиле Ричарда Фейнмана.")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                user_input = gr.Textbox(lines=10, placeholder="Введите ваш вопрос здесь...", label="Ваш вопрос")
            with gr.Row():
                clear_btn = gr.Button(value="Очистить")
                submit_btn = gr.Button(value="Отправить", elem_classes="submit-btn")
        with gr.Column():
            # output = gr.Textbox(lines=10, label="Ответ")
            output = gr.Markdown(label="Ответ", elem_classes="output-markdown")

    submit_btn.click(fn=chat_with_feynman, inputs=user_input, outputs=output)
    clear_btn.click(lambda: "", inputs=[], outputs=user_input)
    clear_btn.click(lambda: "", inputs=[], outputs=output)


iface.launch(server_name="0.0.0.0", server_port=7860, share=True)

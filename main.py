from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))


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
    gr.Markdown("# Чат с Фейнманом\nЗадайте любой вопрос и получите ответ в стиле Ричарда Фейнмана.")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                user_input = gr.Textbox(lines=10, placeholder="Введите ваш вопрос здесь...", label="Ваш вопрос")
            with gr.Row():
                submit_btn = gr.Button(value="Отправить", elem_classes="submit-btn")
                clear_btn = gr.Button(value="Очистить")
        with gr.Column():
            # output = gr.Textbox(lines=10, label="Ответ")
            output = gr.Markdown(label="Ответ", elem_classes="output-markdown")

    submit_btn.click(fn=chat_with_feynman, inputs=user_input, outputs=output)
    clear_btn.click(lambda: "", inputs=[], outputs=user_input)
    clear_btn.click(lambda: "", inputs=[], outputs=output)


iface.launch(server_name="0.0.0.0", server_port=7860)

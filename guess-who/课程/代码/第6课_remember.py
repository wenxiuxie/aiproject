from openai import OpenAI

API_KEY = "在这里粘贴你的 key"
client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")
MODEL = "Qwen/Qwen2.5-7B-Instruct"

history = []

def chat(text):
    history.append({"role": "user", "content": text})
    response = client.chat.completions.create(model=MODEL, messages=history)
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply

print(chat("我叫小明，请记住我的名字。"))
print("-----")
print(chat("我叫什么名字？"))
print("-----")
print(len(history))

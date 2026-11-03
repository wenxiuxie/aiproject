from openai import OpenAI

API_KEY = "在这里粘贴你的 key"

client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[{"role": "user", "content": "用一句话介绍一下企鹅"}],
)
print(response.choices[0].message.content)

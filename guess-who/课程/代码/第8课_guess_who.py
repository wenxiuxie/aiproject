import random
from nicegui import run, ui
from openai import OpenAI

API_KEY = "在这里粘贴你的 key"
client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")
MODEL = "Qwen/Qwen2.5-7B-Instruct"

MAX_TRIES = 10
SECRETS = {
    "动物": ["企鹅", "大象", "猫", "鲨鱼", "蜜蜂"],
    "食物": ["披萨", "香蕉", "冰淇淋", "饺子", "鸡蛋"],
    "物品": ["雨伞", "手机", "自行车", "吉他", "时钟"],
}

game = {"category": "动物", "secret": "", "left": MAX_TRIES, "over": False, "busy": False, "history": []}

def make_rules(secret):
    return (
        f"我们在玩猜谜游戏。谜底是：{secret}。\n"
        "玩家会问“是不是”的问题来猜谜底。请根据谜底的真实情况，如实回答。\n"
        "规则：\n"
        "1. 只能回答这三个词之一：是、不是、不确定。\n"
        "2. 不许说出谜底，也不许给任何提示。\n"
        "3. 如果玩家问的不是“是不是”的问题，回答：不确定。\n"
        "例子（假设谜底是：狗）：\n"
        "问：它有四条腿吗？ 答：是\n"
        "问：它会飞吗？ 答：不是\n"
        "问：它叫什么？ 答：不确定"
    )

def to_answer(text, secret):
    text = text.strip()
    if secret in text:
        return "不确定"
    if text.startswith("不确定"):
        return "不确定"
    if text.startswith("是"):
        return "是"
    if text.startswith("不"):
        return "不是"
    return "不确定"

def ask_ai(history):
    response = client.chat.completions.create(model=MODEL, messages=history, temperature=0)
    return response.choices[0].message.content

def say(mine, text):
    with chat:
        if mine:
            ui.chat_message(text, name="我", sent=True)
        else:
            ui.chat_message(text, name="AI")

def show_left():
    left_label.text = f"剩余机会：{game['left']} / {MAX_TRIES}"

def title_for(used):
    if used <= 3:
        return "🧠 读心大师"
    elif used <= 6:
        return "🔍 小侦探"
    else:
        return "🐢 坚持到底"

def use_one():
    game["left"] = game["left"] - 1
    show_left()
    if game["left"] == 0:
        game["over"] = True
        say(False, f"😅 机会用完了，答案是{game['secret']}。点「新游戏」再来一局！")

def new_game():
    game["secret"] = random.choice(SECRETS[game["category"]])
    game["left"] = MAX_TRIES
    game["over"] = False
    game["history"] = [{"role": "system", "content": make_rules(game["secret"])}]
    chat.clear()
    show_left()
    say(False, f"我想好了一个{game['category']}，问我吧！")

def choose(e):
    game["category"] = e.sender.text
    category.text = f"当前类别：{game['category']}"
    new_game()

async def ask():
    q = box.value
    if game["over"]:
        ui.notify("这一局结束了，点「新游戏」再来一局")
    elif game["busy"]:
        ui.notify("AI 还在想，请稍等")
    elif q == "":
        ui.notify("请先输入问题")
    else:
        say(True, q)
        box.value = ""
        game["history"].append({"role": "user", "content": q})
        game["busy"] = True
        status.text = "AI 正在想…"
        try:
            raw = await run.io_bound(ask_ai, game["history"])
            answer = to_answer(raw, game["secret"])
            game["history"].append({"role": "assistant", "content": answer})
            say(False, answer)
            use_one()
        except Exception as e:
            game["history"].pop()
            say(False, f"⚠️ 连接 AI 出错了（{type(e).__name__}），这次不扣机会。检查一下 key 和网络再试。")
        game["busy"] = False
        status.text = ""

def guess():
    g = box.value
    if game["over"]:
        ui.notify("这一局结束了，点「新游戏」再来一局")
    elif g == "":
        ui.notify("请先输入你猜的东西")
    else:
        say(True, f"我猜：{g}")
        box.value = ""
        if g == game["secret"]:
            game["over"] = True
            used = MAX_TRIES - game["left"] + 1
            say(False, f"🎉 猜对了！就是{game['secret']}！你用了 {used} 次机会，获得称号：{title_for(used)}")
        else:
            say(False, f"不对，不是{g}！")
            use_one()

with ui.column().classes("w-full max-w-xl mx-auto"):
    ui.label("猜猜我是谁").classes("text-3xl font-bold")
    ui.label("我心里想好了一个东西，你来猜！")
    with ui.row():
        for c in SECRETS:
            ui.button(c, on_click=choose)
    category = ui.label("当前类别：动物")
    left_label = ui.label("").classes("text-lg font-bold text-orange-700")
    with ui.card().classes("w-full"):
        chat = ui.column().classes("w-full")
        status = ui.label("").classes("text-sm text-gray-500")
        box = ui.input(placeholder="输入问题，例如：它会飞吗？").classes("w-full").props("outlined")
        box.on("keydown.enter", ask)
        with ui.row():
            ui.button("提问", on_click=ask)
            ui.button("我猜是它", on_click=guess).props("color=orange")
            ui.button("新游戏", on_click=new_game)

new_game()

ui.run()

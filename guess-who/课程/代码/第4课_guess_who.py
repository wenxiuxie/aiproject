import random
from nicegui import ui

MAX_TRIES = 10
SECRETS = {
    "动物": ["企鹅", "大象", "猫", "鲨鱼", "蜜蜂"],
    "食物": ["披萨", "香蕉", "冰淇淋", "饺子", "鸡蛋"],
    "物品": ["雨伞", "手机", "自行车", "吉他", "时钟"],
}

game = {"category": "动物", "secret": "", "left": MAX_TRIES, "over": False}
questions = []

def say(mine, text):
    with chat:
        if mine:
            ui.chat_message(text, name="我", sent=True)
        else:
            ui.chat_message(text, name="AI")

def show_left():
    left_label.text = f"剩余机会：{game['left']} / {MAX_TRIES}"

def new_game():
    game["secret"] = random.choice(SECRETS[game["category"]])
    game["left"] = MAX_TRIES
    game["over"] = False
    questions.clear()
    chat.clear()
    show_left()
    say(False, f"我想好了一个{game['category']}，问我吧！")

def choose(e):
    game["category"] = e.sender.text
    category.text = f"当前类别：{game['category']}"
    new_game()

def ask():
    q = box.value
    if game["over"]:
        ui.notify("这一局结束了，点「新游戏」再来一局")
    elif q == "":
        ui.notify("请先输入问题")
    else:
        questions.append(q)
        say(True, q)
        say(False, "（AI 还没接上，第 5 课再来回答）")
        box.value = ""

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
            say(False, f"🎉 猜对了！就是{game['secret']}！")
        else:
            game["left"] = game["left"] - 1
            if game["left"] == 0:
                game["over"] = True
                say(False, f"😅 机会用完了，答案是{game['secret']}。")
            else:
                say(False, f"不对，不是{g}！")
        show_left()

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
        box = ui.input(placeholder="输入问题，例如：它会飞吗？").classes("w-full").props("outlined")
        with ui.row():
            ui.button("提问", on_click=ask)
            ui.button("我猜是它", on_click=guess).props("color=orange")
            ui.button("新游戏", on_click=new_game)

new_game()

ui.run()

from nicegui import ui

questions = []

def choose(e):
    category.text = f"当前类别：{e.sender.text}"

def say(mine, text):
    with chat:
        if mine:
            ui.chat_message(text, name="我", sent=True)
        else:
            ui.chat_message(text, name="AI")

def ask():
    q = box.value
    if q == "":
        ui.notify("请先输入问题")
    else:
        questions.append(q)
        say(True, q)
        say(False, f"（AI 还没接上，第 5 课再来回答。你已经问了 {len(questions)} 个问题）")
        box.value = ""

def new_game():
    chat.clear()
    questions.clear()
    say(False, "我又想好了一个东西，问我吧！")

def guess():
    g = box.value
    if g == "":
        ui.notify("请先输入你猜的东西")
    else:
        say(True, f"我猜：{g}")
        box.value = ""

with ui.column().classes("w-full max-w-xl mx-auto"):
    ui.label("猜猜我是谁").classes("text-3xl font-bold")
    ui.label("我心里想好了一个东西，你来猜！")
    with ui.row():
        for c in ["动物", "食物", "物品"]:
            ui.button(c, on_click=choose)
    category = ui.label("当前类别：动物")
    with ui.card().classes("w-full"):
        chat = ui.column().classes("w-full")
        box = ui.input(placeholder="输入问题，例如：它会飞吗？").classes("w-full").props("outlined")
        with ui.row():
            ui.button("提问", on_click=ask)
            ui.button("我猜是它", on_click=guess).props("color=orange")
            ui.button("新游戏", on_click=new_game)

say(False, "我想好了一个东西，问我吧！")

ui.run()

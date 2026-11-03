from nicegui import ui

questions = []

def choose(e):
    category.text = f"当前类别：{e.sender.text}"

def ask():
    q = box.value
    if q == "":
        ui.notify("请先输入问题")
    else:
        questions.append(q)
        result.text = f"你问了：{q}（一共问了 {len(questions)} 个问题）"
        box.value = ""

def guess():
    g = box.value
    if g == "":
        ui.notify("请先输入你猜的东西")
    else:
        result.text = f"你猜的是：{g}"
        box.value = ""

ui.label("猜猜我是谁")
ui.label("我心里想好了一个东西，你来猜！")

categories = ["动物", "食物", "物品"]
for c in categories:
    ui.button(c, on_click=choose)
category = ui.label("当前类别：动物")

box = ui.input(placeholder="输入问题，例如：它会飞吗？")
ui.button("提问", on_click=ask)
ui.button("我猜是它", on_click=guess)
result = ui.label("")

ui.run()

from nicegui import ui
ui.label("猜猜我是谁")
ui.label("我心里想好了一个东西，你来猜！")
categories = ["动物", "食物", "物品"]
for c in categories:
    ui.button(c)
ui.input(placeholder="输入问题，例如：它会飞吗？")
ui.button("提问")
ui.button("我猜是它")
ui.run()

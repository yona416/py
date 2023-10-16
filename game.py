import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Button Example")

# 定义按钮点击事件
def on_button_click():
    label.config(text="Hello, " + entry.get())

# 创建标签
label = tk.Label(root, text="Enter your name:")
label.pack()

# 创建输入框
entry = tk.Entry(root)
entry.pack()

# 创建按钮并绑定点击事件
button = tk.Button(root, text="Say Hello", command=on_button_click)
button.pack()

# 运行主循环
root.mainloop()

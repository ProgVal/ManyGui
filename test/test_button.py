from anygui import Window, Button, Application, Options

app = Application()

g_y = 150

win = Window(width = 110, height = 210)

def say_hello():
    print "Hello, world!"
    global g_y
    btn = Button(opt, y = g_y, text="New")
    g_y += 5
    win.add(btn)

opt = Options(x = 30, width = 50, height = 30, action = say_hello)
btn = Button(opt, y = 30, text = "Hello")
dis = Button(opt, y = 90, text = "Goodbye", enabled = 0)

win.add(btn)
win.add(dis)

app.run()

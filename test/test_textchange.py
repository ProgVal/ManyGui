from anygui import *

app = Application()
btn = Button(text='Before')
cbx = CheckBox(text='Before')
rbn = RadioButton(text='Before')
lbl = Label(text='Before')

cng = Button(text='Change')

cmps = btn, cbx, rbn, lbl

def change(**kw):
    for cmp in cmps:
        cmp.text = 'After'

link(cng, change)

win = Window(width=btn.width, height=145)
win.add(cmps+(cng,), direction='down')
app.run()

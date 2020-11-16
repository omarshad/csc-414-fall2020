
from tkinter import *
from tkinter import messagebox

# Gui Window
window=Tk()
window.configure(bg='Grey')
window.title('Stubbed Menu')
window.geometry("300x500")


#Buttion Click dummy fuctions
def buttonCallback1():
    messagebox.showinfo("Message", "You have clicked the Button 1!")

def buttonCallback2():
    messagebox.showinfo("Message", "You have clicked the Button 2!")

def buttonCallback3():
    messagebox.showinfo("Message", "You have clicked the Button 3!")

def buttonCallback4():
    messagebox.showinfo("Message", "You have clicked the Button 4!")

def buttonCallback5():
    messagebox.showinfo("Message", "You have clicked the Button 5!")

def buttonCallback6():
    messagebox.showinfo("Message", "You have clicked the Button 6!")

def buttonCallback7():
    messagebox.showinfo("Message", "You have clicked the Button 7!")

def buttonCallback8():
    messagebox.showinfo("Message", "You have clicked the Button 8!")

def buttonCallback9():
    messagebox.showinfo("Message", "You have clicked the Button 9!")

def buttonCallback10():
    messagebox.showinfo("Message", "You have clicked the Button 10!")


#fuction to quit
    def quit():
        
        window.distroy()

label = Label( window, text="Stubbed Menu",background = 'black', foreground = "white")

#Button Display

btn1=Button(window, text="Menu Item 1",command=buttonCallback1)
btn1.place(x=80, y=40)

btn2=Button(window, text="Menu Item 2",command=buttonCallback2)
btn2.place(x=80, y=80)

btn3=Button(window, text="Menu Item 3",command=buttonCallback3)
btn3.place(x=80, y=120)

btn4=Button(window, text="Menu Item 4",command=buttonCallback4)
btn4.place(x=80, y=160)

btn5=Button(window, text="Menu Item 5",command=buttonCallback5)
btn5.place(x=80, y=200)

btn6=Button(window, text="Menu Item 6",command=buttonCallback6)
btn6.place(x=80, y=240)

btn7=Button(window, text="Menu Item 7",command=buttonCallback7)
btn7.place(x=80, y=280)

btn8=Button(window, text="Menu Item 8",command=buttonCallback8)
btn8.place(x=80, y=320)

btn9=Button(window, text="Menu Item 9",command=buttonCallback9)
btn9.place(x=80, y=360)

btn10=Button(window, text="Menu Item 10",command=buttonCallback10)
btn10.place(x=80, y=400)



btn11 =Button(window, text = 'Click and Quit', command=window.quit())
btn11.place(x=80, y=440)


window.mainloop()


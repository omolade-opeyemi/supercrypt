import tkinter
from tkinter import*
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random



from tkinter.filedialog import*
win = Tk()
win.title('Venocrypt')
win.resizable(width= False, height= False)
win.geometry('400x500')
win.configure(bg = 'skyblue')

#let's do this!!
def disablet2():
    et2.configure(state = 'disabled')
    t1.configure(state = 'normal')
    et2.update()
def disablet1():
    t1.configure(state = 'disabled')
    et2.configure(state = 'normal')
    t1.update()
def open_file():
    filename = askopenfilename( filetypes = [('All Files','*.*')])
    et2.delete(0, END)
    et2.insert(END, filename)
    return filename

def encode_image():
    picture = askopenfilename( filetypes = [('Image Files','*.JPG'),('Image Files','*.PNG'),('Image Files','*.GIF'),('All Files','*.*')])
    et1.delete(0, END)
    et1.insert(END, picture)
    return picture
def save_file():
    file = asksaveasfilename(filetypes=[('Image Files','*.PNG')])
    et3.delete(0, END)
    et3.insert(END, file)

def encrypt(key, filename):
    chunkSize = 64*1024
    outputFile = 'e-'+filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunkSize)
                if chunk == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    chunksize = 64*1024
    outputfile = filename[11:]

    with open(filename, 'rb') as infile:

        filesize = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputfile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)



def getKey():
    win2 = Tk()
    win2.title('password')
    win2.geometry('200x400')
    lp = Label(win2, text='input password')
    lp.pack()
    ep = Entry(win2, width= 25)
    ep.pack()
    hasher = SHA256.new(ep.get().encode('utf-8'))
    bp = Button(win2, text='OK', command=win2.quit)
    bp.pack()
    win2.mainloop()
    return hasher.digest()


def Main():
    choice = r2.get()

    if choice == 1:
        filename = open_file()
        password = getKey()
        encrypt(password, filename)
        print('Done')

    if choice == 2:
        filename = input('File to decrypt: ')
        password = getKey()
        decrypt(password, filename)
        print('Done decrypting.')
    else:
        print('Invalid input')
        Main()






l1 = Label(win,text='Encode')
l1.place(x=5,y=5)
l2 = Label(win, text='Image:')
l2.place(x=50, y=5)
b1 = Button(win,text ='Browse..', command = encode_image)
b1.place(x=5,y=30)
e1 = StringVar()
et1 = Entry(win, width=50,bg='white', bd=5, fg='green', textvariable=e1)
et1.insert(INSERT, 'drag and drop an image file here')
et1.place(x=70,y=30)
l3 = Label(win, text = 'Input Data:')
l3.place(x = 5, y = 60)
r1 = IntVar()
rb1 = Radiobutton(win, text = 'File', variable = r1, value = 1, command = disablet1)
rb1.place(x = 5, y = 90)
b2 = Button(win,text ='Browse..', command = open_file)
b2.place(x=5,y=120)
rb2 = Radiobutton(win, text = 'Text', variable = r1, value = 2,state = 'normal',command =  disablet2)
rb2.place(x = 5, y = 150)
e2 = StringVar()
et2 = Entry(win, width = 50, textvariable = e2,fg='green')
et2.place(x = 70, y = 125)
et2.insert(INSERT, 'Drag and drop the file to embed in the image here')
t1 = Text(win, bd = 5, font = 15, height = 9, width = 40)
t1.place(x = 10, y = 180)
l4 = Label(win, text = 'Output Image:')
l4.place(x=10, y =360)
b3 = Button(win, text = 'Choose...', command = save_file)
b3.place(x=100,y=360)
e3 = StringVar()
et3 = Entry(win, width = 60,textvariable = e3)
et3.place(x=10, y=390, )
c1= IntVar()
ch1 = Checkbutton(win,text = 'Compress', offvalue = 0, onvalue = 1, variable = c1)
ch1.place(x = 10, y =420 )
c2 = IntVar()
ch2 = Checkbutton(win,text = 'Encrypt', offvalue = 0, onvalue = 1, variable = c2 )
ch2.place(x = 10 , y = 450)
r2 = IntVar()
rb3 = Radiobutton(win, text = 'Encode', variable = r2, value = 1)
rb3.place(x=130, y=420)
rb4 = Radiobutton(win, text = 'Decode', variable = r2, value = 2)
rb4.place(x=130, y = 450)
b4 = Button(win, text = 'Start', bd = 5, font = 15, padx=20, pady=20,command = Main )
b4.place(x=270, y = 415)

win.mainloop()
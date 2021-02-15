import tkinter as tk
from typing import Collection
from PIL import Image, ImageTk
from math import *
import pymongo
import random, datetime

client = pymongo.MongoClient("mongodb+srv://te18_user:Gurkbert@cluster0.7fvne.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.nti_chat

users = db["users"]

documents = users.find({})
usernames = []
for doc in documents:
    usernames.append(doc['username'])

usernamesPerPage = 15
contactLists = []
usernamesPage = 0

HEIGHT = 720
WIDTH = 1080

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

load = Image.open("gradient.png")
render = ImageTk.PhotoImage(load)

img = tk.Label(canvas, image=render)
img.image = render
img.pack()

cntBox = tk.Label(img, bg='#F4CE1C')
cntBox.place(relx=0.02, rely=0.1, relh=0.8, relw=0.25)

def generate_usernames():
    if len(usernames) > usernamesPerPage:
        listsNeeded = ceil(len(usernames)/usernamesPerPage)
        for i in range(listsNeeded):
            contactLists.append([])
        for cList in contactLists:
            while len(cList) < usernamesPerPage and len(usernames) > 0:
                cList.append(usernames[0])
                usernames.pop(0)
        temp = []
        for contact in contactLists[usernamesPage]:
            temp.append(tk.Button(cntBox, bg='#F5DF2D', text=contact))
        for i, contact in enumerate(temp):
            contact.place(relx=0.1, rely=0.1 + 0.05*i)
    else:
        temp = []
        for contact in usernames:
            temp.append(tk.Button(cntBox, bg='#F5DF2D', text=contact))
        for i, contact in enumerate(temp):
            contact.place(relx=0.1, rely=0.1 + 0.05*i)

generate_usernames()

def page_next(usernamesPage, cntBox):
    usernamesPage += 1
    cntBox.destroy()
    #generate_usernames()


if len(contactLists) > 1:
    nextPage = tk.Button(cntBox, bg='#F5DF2D', text='Next Page', command=page_next(usernamesPage, cntBox))
    nextPage.place(relx=0.8, rely=0.9)

    
entry = tk.Entry(img, bg='#F4CE1C')
entry.place(relx=0.6, rely=0.9, relw=0.6, anchor='center')


root.mainloop()
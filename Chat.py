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

usrName = ''

usernamesPerPage = 15
contactLists = []
usernamesPage = 0

#messages = []

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

usrName = tk.Entry(img, bg='#F4CE1C')
usrName.place(relx=0.6, rely=0.1, relw=0.2, anchor='center')

def open_chat(contact):
    messages = users.find({'username': usrName})
    for message in messages:
        current_message = message['history']['friends'][contact]
        print(current_message)

def generate_usernames():
    if len(usernames) > usernamesPerPage:
        listsNeeded = ceil(len(usernames)/usernamesPerPage)
        cntBox = tk.Label(img, bg='#F4CE1C')
        cntBox.place(relx=0.02, rely=0.1, relh=0.8, relw=0.12*listsNeeded)
        for i in range(listsNeeded):
            contactLists.append([])
        for cList in contactLists:
            while len(cList) < usernamesPerPage and len(usernames) > 0:
                cList.append(usernames[0])
                usernames.pop(0)
        for o, array in enumerate(contactLists):
            temp = []
            for contact in array:
                temp.append(tk.Button(cntBox, bg='#F5DF2D', text=contact, command=open_chat(contact)))
            for i, contact in enumerate(temp):
                contact.place(relx=0.4*o, rely=0.1 + 0.05*i)
    else:
        cntBox = tk.Label(img, bg='#F4CE1C')
        cntBox.place(relx=0.02, rely=0.1, relh=0.8, relw=0.25)
        temp = []
        for contact in usernames:
            temp.append(tk.Button(cntBox, bg='#F5DF2D', text=contact))
        for i, contact in enumerate(temp):
            contact.place(relx=0.1, rely=0.1 + 0.05*i)

generate_usernames()

    
entry = tk.Entry(img, bg='#F4CE1C')
entry.place(relx=0.6, rely=0.9, relw=0.6, anchor='center')


root.mainloop()
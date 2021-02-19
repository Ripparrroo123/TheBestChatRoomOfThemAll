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

currentUsrName = ''
currentContact = ''

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

chat = tk.Listbox(img, bg='#F4CE1C')
chat.place(relx=0.6, rely=0.5, relh=0.5, relw=0.6, anchor='center')

def open_chat(target):
    chat.delete(0, tk.END)
    global currentUsrName
    global currentContact
    currentUsrName = usrName.get()
    currentContact = target
    try:
        messages = list(users.find({'username': currentUsrName}))
        print(currentContact)
        for message in messages:
            current_message = message['history']['friends'][target]
        for message in current_message:
            if message['status'] == 'received':
                chat.insert(tk.END, target + ': ' + message['content'])
            elif message['status'] == 'sent':
                chat.insert(tk.END, currentUsrName + ': ' + message['content'])
    except:
        return True

def updateChat():
    chat.delete(0, tk.END)
    try:
        messages = list(users.find({'username': currentUsrName}))
        print(currentContact)
        for message in messages:
            current_message = message['history']['friends'][currentContact]
        for message in current_message:
            if message['status'] == 'received':
                chat.insert(tk.END, currentContact + ': ' + message['content'])
            elif message['status'] == 'sent':
                chat.insert(tk.END, currentUsrName + ': ' + message['content'])
    except:
        return True

def send_message():
    print(currentContact)
    recipient = currentContact
    print(recipient)
    sender = usrName.get()
    print(sender)

    new_message_recipient = {'status':'received', 'content': entry.get(), 'time':datetime.datetime.now()}
    users.update({'username': recipient}, {'$push': {f'history.friends.{sender}': new_message_recipient}})

    new_message_sender = {'status':'sent', 'content': entry.get(), 'time':datetime.datetime.now()}
    users.update({'username': sender}, {'$push': {f'history.friends.{recipient}': new_message_sender}})
    updateChat()
    entry.delete(0, tk.END)

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
            for p, contact in enumerate(array):
                #name = array[p]
                temp.append(tk.Button(cntBox, bg='#F5DF2D', text=array[p], command=lambda name=array[p]:open_chat(name)))
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

send = tk.Button(img, bg='#F4CE1C', text='Send', command=send_message)
send.place(relx=0.92, rely=0.9, anchor='center')

update = tk.Button(img, bg='#F4CE1C', text='Update', command=updateChat)
update.place(relx=0.8, rely=0.23, anchor='center')


root.mainloop()
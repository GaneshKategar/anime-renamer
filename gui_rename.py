from tkinter import *
from tkinter import ttk,filedialog
import tkinter as tk
import time
import webbrowser
import os
import requests

def clicked():
    global stnum,ltnum,idx
    idx = x.get()
    stnum= st.get()
    ltnum = lt.get()
    idx = int(idx)
    stnum = int(stnum)
    ltnum = int(ltnum)
    rename()


def selectdir():
    global dir
    dir = filedialog.askdirectory()
    print(dir)

    
def ui():
    root = tk.Tk()
    root.title("Anime renamer")
    root.geometry("700x600")

    global x,st,lt,res
    x = tk.StringVar() 
    st = tk.StringVar()
    lt = tk.StringVar()
    #Declaring all the widgets
    title = tk.Label(root,text="WELCOME TO ANIME EPISODE RENAMER")
    desc = tk.Label(root,text="This is used to rename episodes of an anime to thier actual numbers rather than episode numbers")
    help = tk.Label(root,text="If you need any help regarding how to use this app click this text to know how to use it")
    help.bind("<Button-1>",lambda e: webbrowser.open_new("https://github.com/GaneshKategar/anime-renamer/blob/main/README.md"))

    warn = tk.Label(root,text="These are the to enter to make the app work correctly")

    #the required data

    id_label = tk.Label(root,text="Enter the Id of the desired anime")
    id_data = tk.Entry(root,textvariable=x)
    id_label.focus()
    
    stnum_label = tk.Label(root,text="Enter the start number of the anime episodes")
    stnum_data = tk.Entry(root,textvariable=st)

    ltnum_label = tk.Label(root,text="Enter the last number of the anime episode")
    ltnum_data = tk.Entry(root,textvariable=lt)

    bro_label = tk.Label(root,text="Browse to the directoy")
    bro_btn = tk.Button(root,text="browse",command=selectdir)

    sbt_btn = tk.Button(root,text="Submit",command=clicked)

    res = tk.Label(root,textvariable='')



    #Positioning the widgets
    title.pack(ipadx=20,ipady=20,anchor=tk.S)
    desc.pack()
    help.pack()
    warn.pack(ipady=20)
    
    id_label.pack()
    id_data.pack(ipadx=30)

    stnum_label.pack()
    stnum_data.pack()

    ltnum_label.pack()
    ltnum_data.pack()

    bro_label.pack()
    bro_btn.pack()

    sbt_btn.pack(pady=40)
    res.pack()

    root.mainloop()


#Renaming the files
def rename():
    data = data_fecthing()
    srcdir = os.listdir(dir)
    res.configure(text="The files are being renamed")
    if len(srcdir) < (ltnum-stnum):
        print("The directory does not have sufficient files")
        return
    with open("te.txt","r") as file:
        
        ds = file.readline()
        for l in range(0,(data[1]-data[0]+1)):  
            src = os.path.join(dir,srcdir[l])
            j = ds.split("__")
            dst = dir+"/" + j[l] + ".mkv"
            try:
                if os.path.exists(src):
                    os.rename(src,dst)
                    print(src)
                    print(dst)
                    print("File Renamed",l,"\n")
            except Exception as e:
                print(e)
    res.configure("The files have successfully renamed")



#Get data from the web
def openweb(url):

    response = requests.get(url)

    if response.status_code != 200:
        print("cannot access web")
        print(response)
        return 
    else:
        data = response.json()
        data = data['data']
        epi = {'mal_id':data['mal_id'],'title':data['title']}
        return epi['mal_id'],epi['title']


# To Enter the episode names in a file
def data_fecthing():
    li = [stnum,ltnum]
    print("Please Wait while we fetch the data.................")
    res.configure(text="The data is being fetched.Please Wait......")
    file = open('te.txt','w') 
    for i in range(stnum,ltnum+1):
        url = f'https://api.jikan.moe/v4/anime/{idx}/episodes/{i}'
        try:
            openweb(url)
            ep,tit = openweb(url)
            file.write(str(ep))
            file.write("-")
            while '?' in tit:
                tit = tit.replace("?","!")
            file.write(tit)
            file.write("__")
            time.sleep(0.8)
            print("entered data in the file ")
        except Exception as e:
            print(e)
    return li



def main():
    ui()


if __name__=='__main__':
    main()
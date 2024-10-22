from tkinter import *
from tkinter import filedialog
import tkinter as tk
import time
import webbrowser
import os
import threading
import requests


def clicked():
    global stnum,ltnum,idx
    global file_list
    file_list = []
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
    img = PhotoImage(file=r"D:\Ganesh\Something\New_folder\Screenshot28.png")
    #Declaring all the widgets
    title = tk.Label(root,text="WELCOME TO ANIME EPISODE RENAMER")
    desc = tk.Label(root,text="This is used to rename episodes of an anime to thier actual numbers rather than episode numbers")
    helpimg = tk.Label(root,text="If you need any help regarding how to use this app click this text to know how to use it",image=img,cursor='dot',width=10,height=20)
    # helpimg = tk.Label(root,image=img)
    helpimg.bind("<Button-1>",lambda e: webbrowser.open_new("https://github.com/GaneshKategar/anime-renamer/blob/main/README.md"))

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

    sbt_btn = tk.Button(root,text="Submit",command=threading.Thread(target=clicked).start)

    res = tk.Label(root,textvariable='')



    #Positioning the widgets
    title.pack(ipadx=20,ipady=20,anchor=tk.S)
    desc.pack()
    helpimg.pack()
    
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
    print(file_list)
    srcdir = os.listdir(dir)
    res.configure(text="The files are being renamed")
    #Checking if there are sufficient files to rename
    if len(srcdir) < (ltnum-stnum):
        print("The directory does not have sufficient files")
        return
    #Renaming the files
    for l in range(0,(data[1]-data[0]+1)):  
        ds = file_list[l]
        src = os.path.join(dir,srcdir[l])
        dst = dir+ "\\" + ds + ".mkv"
        print(dst)
        try:
            if os.path.exists(src):
                os.rename(src,dst)
                print(src)
                print(dst)
                print("File Renamed",l,"\n")
        except Exception as e:
            print("HLELO MORO",e)
    res.configure(text="The files have successfully renamed")
    print("The files have successfully renamed")


#Get data from the web
def openweb(url,tit_url):

    response = requests.get(url)
    title_res = requests.get(tit_url)

    #to get status if we connected successfully with the api
    if response.status_code != 200 or title_res.status_code !=200:
        print("cannot access web")
        print(response)
        return 
    else:
        #to get data about the anime i.e the name of anime for example in 269 we have anime title "bleach"
        title_data = title_res.json()
        title_data = title_data['data']
        title_data = title_data['titles']
        title_data = title_data[0]

        #to get data about the episode that we want to rename
        data = response.json()
        data = data['data']
        epi = {'Ani_title':title_data['title'] ,'mal_id':data['mal_id'] ,'title':data['title'],'filler':data['filler'] }   # Anime title = Name of anine ,mal_id = episode number, title = episode title/name
        return epi['Ani_title'],epi['mal_id'],epi['title'],epi['filler']


# To Enter the episode names in a file
def data_fecthing():
    global file_list
    li = [stnum,ltnum]
    print("Please Wait while we fetch the data.................")
    res.configure(text="The data is being fetched.Please Wait......")

    for i in range(stnum,ltnum+1):
        temp_list = ''
        url = f'https://api.jikan.moe/v4/anime/{idx}/episodes/{i}'
        tit_url = f'https://api.jikan.moe/v4/anime/{idx}'
        try:
            #sends 2 url's to get data about the episode and the name of anime and recives 4 inputs
            ani,ep,tit,fill = openweb(url,tit_url)
            while ':' in ani:                       #os.rename gives error when we rename file name with a text that has ":" in it
                ani = ani.replace(':'," ")
            temp_list+=ani
            temp_list+=" "
            if fill:
                temp_list+='[Filler]'
                temp_list+=' '
            temp_list+=str(ep)
            temp_list+="-"
            while '?' in tit:                     #os.rename gives error when we rename file name with a text that has "?" in it
                tit = tit.replace("?","!")
            temp_list+=tit
            # temp_list.append("__")
            time.sleep(0.8)
            print(temp_list)
            file_list.append(temp_list)
            print("entered data in the file ")
        except Exception as e:
            print(e)
    return li



def main():
    ui()


if __name__=='__main__':
    main()
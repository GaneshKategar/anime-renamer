from tkinter import *
from tkinter import filedialog
from mal import client
import requests
import time
import re
import os
import threading


#Variables
global anime,directory,episode,episode_data,res

anime = {'name' : str , 'id' : int , 'type' : str} # values { name : shika noko , id : 58426 , type : tv}
episode = {'start': int , 'end' : int}  # values { start : 1 , end :5}
episode_data = [] # values [episode1title,episode2title,episode3title]

#Loads the UI for choosing the anime
def Load_anime_id_UI(root):

    name_frame = Frame(root)
    
    # global anime_name_frame
    # anime_name_frame = None
      
    #Gets data from the MAL-API pyhton package
    def get_anime_id(name):
        
        api_id = ''  # Your MAL_API ID
        cli = client.Client(api_id)
                
        # global anime_name_frame

        # if anime_name_frame is not None:
        #     anime_name_frame.destroy()

        anime_name_frame = Frame(name_frame)
        #Set the data for the anime selected
        def setAnime(obj):
            global anime
            anime['name'] = obj.get('node').get('title')
            anime['id'] = obj.get('node').get('id')
            anime['type'] = obj.get('node').get('media_type')
            res.configure(text='Got Data About the Anime')
            name_frame.destroy()
            Load_dir_UI(root)
            print(anime)

        anime = cli.anime_search(name)

        anime_name_arr = []

        
        #Converting the json data into a iterable data
        it = iter(anime.raw['data'])
        for i in it:
            anime_name_arr.append(Button(anime_name_frame,text=f'{i['node']['title']}',command=lambda ob=i:setAnime(ob)).pack())
            # btn.pack()
            print(i['node']['title'],"    ",i['node']['id'])

        anime_name_frame.pack()
    Label(name_frame,text="Enter the name of the anime which you would like to change to and select the button").pack(pady=20)
    name = Entry(name_frame)
    name.pack()
    Button(name_frame,text="Submit",command=lambda:get_anime_id(name.get())).pack(pady=20)
    print(name.get())

    name_frame.pack()
   

#Loads the UI for selecting directory for the anime
def Load_dir_UI(root):

    dir_frame = Frame(root)

    #Gets the path which files are in 
    def get_dir():
        global directory
        directory = filedialog.askdirectory()
        dir_frame.destroy()
        if anime['type']!='movie':
            res.configure(text="Obtained the path to rename files in")
            Load_episode_list_UI(root)
        else:
            episode['start']=1
            episode['end']=1
            res.configure(text="Obtained the path to rename files in")
            Load_rename_UI(root)
        print(directory)


    Label(dir_frame,text="Select the directory where your anime files are located").pack(pady=5)
    Label(dir_frame,text='Browse to the directory').pack(pady=5)

    btn = Button(dir_frame,text="Browse",command=get_dir)
    btn.pack()

    dir_frame.pack()

#Loads the UI for the range of episodes which needs to be renamed
def Load_episode_list_UI(root):


    epi_frame = Frame(root)

    #Gets the data about range of episode
    def get_episode_list(start,end):

        global episode

        episode['start'] = int(start)
        episode['end'] = int(end)

        print(episode)
        res.configure(text='Got the range of Episode to rename')
        epi_frame.destroy()

        Load_rename_UI(root)

    Label(epi_frame,text="Enter the range the Episodes present in the directory").pack()

    Label(epi_frame,text="Starting Episode").pack()

    start_epi_list = Entry(epi_frame)
    start_epi_list.pack()

    Label(epi_frame,text="Ending Episode").pack()
    end_epi_list = Entry(epi_frame)
    end_epi_list.pack()

    btn = Button(epi_frame,text='Submit',command=lambda :get_episode_list(start_epi_list.get(),end_epi_list.get()))
    btn.pack()

    epi_frame.pack()


# UI for renaming file button 
def Load_rename_UI(root):
    
    #Button to start renaming files
    btn = Button(root,text='Start Renaming',command=rename)
    btn.pack()



#Loads the UI of Tkinter
def ui():

    #To show what the program is currently doing in the tkinter window
    global res

    root = Tk()
    root.title("Anime Renamer")
    root.geometry('670x710')

    Label(root,text="A place which changes names of your anime episode").pack(pady=20)
    
    #MultiThreading attempt dont know If actually works
    data_thread = threading.Thread(target=Load_anime_id_UI(root))
    data_thread.start()
    # Load_dir_UI(root)

    # Load_episode_list_UI(root)

    res = Label(root,text='')
    res.pack(side='bottom',pady=200)

    root.mainloop()




def extract_number_general(filename):
    """Extract the first numeric value from a filename (general case)."""
    """https://www.w3reference.com/blog/reading-files-in-a-particular-order-in-python/"""
    numbers = re.findall(r"\d+", filename)  # \d+ matches 1+ digits
    if numbers:
        return int(numbers[0])  # Return the first number as an integer
    else:
        return float("inf")  # Push files without numbers to the end (or handle error)

# Renames Files in the directory according to anime title
def rename():

    global episode_data

    # to Know whether an anime is season type or movie type or OVA
    if anime['type']=='tv':
        get_titles_list()
    elif anime['type']=='OVA':
        get_titles_list()
    else:
        title = anime['name']
        while ':' in title:
            title = title.replace(':'," ")
        
        while "?" in title:
            title = title.replace("?","!")

        episode_data.append(title)

    if len(episode_data) < 1:  # To check if a response from jikan is bad and is episode_data empty
        return


    print(episode_data)
    files = os.listdir(directory)    #get all the files from the selected directory
    files = sorted(files,key=extract_number_general) #Use the function to get correct order of numbers
    
    print(files)
    if (len(files) < (episode['end']-episode['start'])):  #Comparing len of file in directory vs episode range specified by user
        print("Insufficient files to rename")
        return

    # Loop to iterate and rename each file in the directory path
    for i in range(0,(episode['end']-episode['start']+1)):
        src_path = os.path.join(directory,files[i])  # Get file path from the directory and file name
        print("\n"+src_path)
        
        #Get File extinsion for video files (mp4,mpv)
        file_extinstion = src_path.split(".")        #Split Name of File into pieces   ["filename", "mp4"]
        file_extinstion =  file_extinstion[-1:]      #Get the last piece extinstion ["mp4"]
        file_extinstion = file_extinstion[0]         #Conversion to string "mp4"

        #os.rename does not want ":" in string when renaming file as it throws error
        def sanitize_filename(name):
        # Replace invalid characters in filename
            invalid_chars = ['/', '\\', '?', '<', '>', ':', '*', '"', '|']
            for char in invalid_chars:
                name = name.replace(char, " ")  # Use an underscore or choose your preferred replacement
            return name

        episode_name = sanitize_filename(episode_data[i])

        # dest_path = directory + "//" + episode_data[i] + file_extinstion # Get destination path from all the data 
        dest_path = os.path.join(directory,episode_name+f".{file_extinstion}")
        try:
            os.rename(src_path,dest_path)
            print("file renamed to ",dest_path)
            res.configure(text=f"File name Renamed to {episode_data[i]}")
        except Exception as e:
            print("Error : ",e)
    
    res.configure(text='Completed Renaming File')


# def get_episode_title(url):

#     res = requests.Response(url)

#     if res.status_code!=200:
#         print("Failed to Connect")
#         return "Failed to Connect"
#     else:
#         data = res.json()
#         data = data['data']
        
    

# Gets the titles from the jikan API
def get_titles_list():

    global episode_data



    def get_episode_data(url):

        response = requests.get(url)
        
        if response.status_code==200:
            data = response.json()
            data = data['data']
            return data
    
        else:

            print("Failed to Connect")
            res.configure(text=f'Failed to connect to API Error Code:{response.status_code}')
            Load_rename_UI()

    
    # Fetches data about each episode
    def process_episode_data(data):

            print(data)
            return data['mal_id'],data['title'],data['filler']       # only getting data about the episode number(mal_id),title(title),filler(filler)
            

    #Gettings all data at once to remove server problems
    url = f'https://api.jikan.moe/v4/anime/{anime['id']}/episodes/'

    
    episode_title_data = get_episode_data(url)


    print(type(episode_title_data))
    print(episode_title_data)
    # Loop for Fetching and loading data into a list(episode_data) to rename files  
    res.configure(text='Retreving data')
    for i in episode_title_data:
        full_title = ''            # Example shikanoko noko koshitan
        # Exception used for invalid response from API with status code other than 200 
        # try:
        epino,title,filler = process_episode_data(i)
        # except Exception as e:
        #     print("GELLO Exception")
        #     print(f"{e}  {type(e)}")
        #     episode_data.clear()    # clears all data in the episode_data
        #     return

       
        # while ':' in title:            #os.rename does not want : in string when renaming file as it throws error
        #     title = title.replace(':'," ")
        
        # while '?' in title:            #os.rename does not want ? in string when renaming file as it throws error
        #     title = title.replace('?',"!")
        
        if filler:
            full_title += '[Filler]'   #full_title should be like this if filler episdode "[Filler]"
            full_title += " "
        
        
        full_title += (anime['name'])    #full_title  = "shikanoko noko koshitan"
        full_title += " "
        full_title += str(epino)
        full_title += '-'              # full_title = "shikanoko noko koshitan 1-"
        full_title += title            # full_title = "shikanoko noko koshitan 1-Episode Name"

        print(full_title)
        episode_data.append(full_title)

        time.sleep(3)

    print("OUT of for loop")




if __name__=='__main__':
    ui()

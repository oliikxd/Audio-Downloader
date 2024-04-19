from customtkinter import *
from PIL import Image
from pytube import YouTube 
import os 
from urllib.error import HTTPError
from sclib import SoundcloudAPI, Track, Playlist
import time
from io import BytesIO
import requests

selected_directory2 = ""
selected_directory = ""
platform = ""
url = ""
Pic = ""


    



def get_thumbnail_image(video_url):
    global Pic
    yt = YouTube(video_url)
    thumbnail_url = yt.thumbnail_url
    response = requests.get(thumbnail_url)
    Pic = Image.open(BytesIO(response.content))
    return Pic

def get_platform():
    global platform
    value  = switch.get()
    if value == 0:
        print("source→YOUTUBE")
        platform = "yt"
        return platform
    else:
        print("source→SoundCloud")
        platform = "sc"
        return platform
    
def url_return():
    global url
    url = web.get()
    print(url)
    return url

def choose_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        print(f"Selected Directory: {selected_directory}")
        output_pat_label.configure(text=selected_directory, font=CTkFont("Arial Black", 5))
        return selected_directory



def downloader(link, directory, platform):
    if platform == "yt":
        yt = YouTube(str(link))
        video = yt.streams.filter(only_audio=True).first()         
        destination = directory
        out_file = video.download(output_path=destination)    
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
        print(yt.title + " has been successfully downloaded.")
        handler.configure(text="DONE!")
        
    else:       
        api = SoundcloudAPI()  
        track = api.resolve(url)
        assert type(track) is Track
        filename = f'./{track.artist} - {track.title}.mp3'
        with open(filename, 'wb+') as file:
            track.write_mp3_to(file)
        handler.configure(text="DONE!")

def generate():   
    print("generating..")
    get_platform()
    url_return()
    print(url)
    try:
        downloader(url,selected_directory, platform)
    except:
        handler.configure(text="something went\n wrong")
        time.sleep(2)


        


deactivate_automatic_dpi_awareness()
set_appearance_mode("dark")
app = CTk()
app.geometry("250x500")
app.resizable(False, False)
app.title("Audio Downloader V1")



audio_image  =Image.open("musical-note.png")
youtube_image = Image.open("Youtube_logo.png")
soundcloud_image = Image.open("soundcloud.png")
arrow_down = Image.open("arrow-down.png")



Aframe = CTkFrame(app, 200,400, fg_color="#373535")
Aframe.place(relx=0.5, rely=0.5, anchor="center")
audio_text = CTkLabel(Aframe, 150, 20, text="AD V1", font=CTkFont("Arial Black", 20))
audio_text.place(relx=0.5, rely=0.05, anchor="center")
audio_icon = CTkLabel(Aframe, 48, 48, text="", image=CTkImage(dark_image=audio_image))
audio_icon.place(relx=0.8, rely=0.05, anchor="center")

switch = CTkSwitch(Aframe, 80, 40, switch_height=20, switch_width=50, corner_radius=10, text="", font=CTkFont("Arial Black", 13)
                   , progress_color="#f28432", fg_color="#c52b16")
switch.place(relx=0.59, rely=0.2, anchor="center")
sound_cloud_icon = CTkLabel(Aframe, 48,48, corner_radius=2, image=CTkImage(dark_image=soundcloud_image, size=(40, 40)), text="")
sound_cloud_icon.place(relx=0.8, rely=0.2, anchor="center")
YT_icon = CTkLabel(Aframe, 48,48, corner_radius=2, image=CTkImage(dark_image=youtube_image, size=(50, 35)), text="")
YT_icon.place(relx=0.2, rely=0.2, anchor="center")

web = CTkEntry(Aframe, 170, 20, corner_radius=10, placeholder_text="Enter URL", font=CTkFont("Arial Black", 13))
web.place(relx=0.5, rely=0.3, anchor="center")

SelectDirectory = CTkButton(Aframe, 170, 25, corner_radius=7, text="Output Path", command=choose_directory,
                            font=CTkFont("Arial Black", 15), fg_color="#d7c249", hover_color="#c1b15a")
SelectDirectory.place(relx=0.5, rely=0.4, anchor="center")

Arrow = CTkLabel(Aframe, 20,20, text="" , image=CTkImage(dark_image=arrow_down))
Arrow.place(relx=0.5, rely=0.48, anchor="center")

output_pat_label = CTkLabel(Aframe, 170, 30, text="None", font=CTkFont("Arial Black", 15))
output_pat_label.place(relx=0.5, rely=0.55, anchor="center")

handler = CTkLabel(Aframe, 170, 30, text="", font=CTkFont("Arial Black", 15), text_color="#c7343b")
handler.place(relx=0.5, rely=0.7, anchor="center")

#Generate
generate =CTkButton(Aframe, 170, 30, corner_radius=7, text="Download", font=CTkFont("Arial Black", 20), fg_color="#d7c249",
                     hover_color="#c1b15a", command=generate)
generate.place(relx=0.5, rely=0.9, anchor="center")











app.mainloop()


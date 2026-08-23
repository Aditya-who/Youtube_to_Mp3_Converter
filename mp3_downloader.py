from tkinter import *
from tkinter import ttk
import sys
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading
import os
import yt_dlp
from tkinter import filedialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class mp3_downloader:
    def __init__(self):
        # creates the window using Tk() function
        self.root = Tk()
      
        # creates title for the window
        self.root.title('MP3 Downloader')
        # the icon for the application, this will replace the default tkinter icon
        self.root.iconbitmap(
    resource_path("resources/favicon.ico")
)
        # dimensions and position of the window
        self.root.geometry('500x400+430+180')
        # makes the window non-resizable
        self.root.resizable(height=FALSE, width=FALSE)
        
        # creates the canvas for containing all the widgets

        progress_style = ttk.Style()

        progress_style.configure(
            'Modern.Horizontal.TProgressbar',
            troughcolor='#E5E7EB',
            background='#7C3AED',
            thickness=12
        )
        
        self.conerter_gui()
        # this runs the app infinitely
        self.root.mainloop()

    def conerter_gui(self):
        self.canvas = Canvas(self.root, width=500, height=400)
        self.canvas.pack()
        
        
        
                # style for the label 
        label_style = ttk.Style()
        label_style.configure('TLabel',foreground='#000000',font=('Arial', 20, 'bold'))
        # style for the entry
        entry_style = ttk.Style()
        entry_style.configure(
    'TEntry',
    font=('Segoe UI', 13),
    padding=10
)
        # style for the button
        button_style = ttk.Style()
        button_style.configure('TButton',foreground='#000000',font=('DotumChe',12))
        self.logo=PhotoImage(
    file=resource_path("resources/Mp3_logo.png")
)
        self.logo = self.logo.subsample(3,3)
# adding the logo to the canvas
        self.canvas.create_image(180, 120, image=self.logo)
        mp3_label = ttk.Label(self.root, text='Downloader', style='TLabel')
        
        self.canvas.create_window(340, 160, window=mp3_label)

        paste_url_label = ttk.Label(self.root, text='Paste Your URL Here..',font=('Segoe UI', 13),
            padding=10)
        self.canvas.create_window(130, 260, window=paste_url_label)
        self.url_box=ttk.Entry(self.root,style='TEntry')
        
        self.canvas.create_window(210,300,window=self.url_box,width=350,
    height=40)

        self.convert_btn=ttk.Button(self.root,text='Convert',style='TButton',command=self.start_conversion)
        self.canvas.create_window(440,300,window=self.convert_btn,width=100,height=40)

        self.progress = ttk.Progressbar(
    self.root,
    style='Modern.Horizontal.TProgressbar',
    orient='horizontal',
    mode='determinate',
    maximum=100
)
        self.canvas.create_window(
    250,
    350,
    window=self.progress,
    width=360,
    height=15
)


        self.progress_label = ttk.Label(
            self.root,
            text='0%',
            font=('Segoe UI', 10)
        )

        self.canvas.create_window(
            250,
            375,
            window=self.progress_label
        )

    def start_conversion(self):

    # Get YouTube URL
        url = self.url_box.get().strip()

        if not url:
            showerror(
                "Error",
                "Please enter a YouTube URL"
            )
            return

        # Open File Explorer
        save_folder = filedialog.askdirectory(
            title="Select where to save the MP3"
        )

        # User clicked Cancel
        if not save_folder:
            return

        # Reset progress
        self.progress['value'] = 0
        self.progress_label.config(text='0%')

        # Disable convert button
        self.convert_btn.config(
            state=DISABLED
        )

        # Start conversion in background
        threading.Thread(
            target=self.convert_video,
            args=(url, save_folder),
            daemon=True
        ).start()


    def convert_video(self, url, save_folder):

        try:

            ydl_opts = {
                'format': 'bestaudio/best',

                'outtmpl': os.path.join(
                    save_folder,
                    '%(title)s.%(ext)s'
                ),

                'noplaylist': True,

                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],

                'progress_hooks': [
                    self.progress_hook
                ]
            }

            # Download and convert
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Conversion finished
            self.root.after(
                0,
                self.conversion_complete
            )

        except Exception as e:

            # Convert exception to string here
            # so it is safely available inside lambda
            error_message = str(e)

            self.root.after(
                0,
                lambda: self.conversion_error(error_message)
            )


    def progress_hook(self, d):

        if d['status'] == 'downloading':

            total = (
                d.get('total_bytes')
                or d.get('total_bytes_estimate')
            )

            downloaded = d.get(
                'downloaded_bytes',
                0
            )

            if total:

                percentage = (
                    downloaded / total
                ) * 100

                self.root.after(
                    0,
                    self.update_progress,
                    percentage
                )

        elif d['status'] == 'finished':

            # Download finished
            # Now FFmpeg will convert it
            self.root.after(
                0,
                self.update_progress,
                100
            )

            self.root.after(
                0,
                lambda: self.progress_label.config(
                    text="Converting to MP3..."
                )
            )


    def update_progress(self, percentage):

        self.progress['value'] = percentage

        self.progress_label.config(
            text=f'{percentage:.0f}%'
        )


    def conversion_complete(self):

        self.progress['value'] = 100

        self.progress_label.config(
            text='Conversion complete!'
        )

        # Enable button again
        self.convert_btn.config(
            state=NORMAL
        )

        showinfo(
            "Success",
            "MP3 conversion completed successfully!"
        )


    def conversion_error(self, error_message):

        # Reset progress
        self.progress['value'] = 0

        self.progress_label.config(
            text='Conversion failed'
        )

        # Enable button again
        self.convert_btn.config(
            state=NORMAL
        )

        showerror(
            "Error",
            f"Conversion failed:\n\n{error_message}"
        )


mp3_downloader()
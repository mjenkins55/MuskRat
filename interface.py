from turtle import width
import back as bck
import hashTest as ht
from tkinter import *
import matplotlib.pyplot as plt
import cv2

import tkinter as tk
from tkinter import LEFT, ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from matplotlib.ft2font import HORIZONTAL 
from video_reader import VideoReader

CATEGORIES = ['Synthetic Content', 'Real Content']
vid_reader = VideoReader(verbose = False)
class file_path:
    def __init__(self, filepath=''):
        self._filepath = filepath

    #setter has list in parameters
    def set_filepath(self, fp):
        self._filepath = fp

class predictionList:
    def __init__(self, model1='', model2='', model3='', model4='', model5='', most_common=''):
        self._model1 = model1
        self._model2 = model2
        self._model3 = model3
        self._model4 = model4
        self._model5 = model5
        self._most_common = most_common

    #setter has list in parameters
    def set_model_pred(self, prediction_list):
        self._model1 = prediction_list[0]
        self._model2 = prediction_list[1]
        self._model3 = prediction_list[2]
        self._model4 = prediction_list[3]
        self._model5 = prediction_list[4]
        self._most_common = prediction_list[5]

predObj = predictionList()
fpObj = file_path()

class App(tk.Tk):
    global uploads
    uploads = 0
    def __init__(self):
        super().__init__()

        self.geometry("960x540")
        self.title('MUSKRAT')
        self.resizable(0, 0)
        self.configure(background='white')

        # configure grid
        self.rowconfigure(0, minsize=240)
        self.rowconfigure(1, minsize=90)
        self.rowconfigure(2, minsize=90)
        self.rowconfigure(3, minsize=90)
        self.rowconfigure(4, minsize=90)
        
        self.columnconfigure(0, minsize=360)
        self.columnconfigure(1, minsize=120)
        self.columnconfigure(2, minsize=120)
        self.columnconfigure(3, minsize=120)
        self.columnconfigure(4, minsize=240)
        
        self.create_widgets()

    def create_widgets(self):
        #title font
        title_font = ("Oswald", 20)
        
        #logo image
        logo_label = self.setImage("muskrat_logo_transparent.png", 240, 150)
        logo_label.grid(column=0, row=0, columnspan=2, sticky= tk.E, padx=(240,0))
        
        #app title
        title_label = tk.Label(self, text = "MUSKRAT\nDeepfake Detection", background='white', font=title_font)
        title_label.grid(column=2, row=0, columnspan=3, sticky=tk.W)
        
        #file upload section
        file_upload_master = tk.Frame(self, width=420, height=40, borderwidth=1, relief="solid", bg='white')
        file_upload_master.pack_propagate(False)
        file_upload_master.grid(column=0, row=1, columnspan=5, sticky=tk.N)
            
        #open file prompt and take selected filepath and previews the selected image
        def uploadAction(event=None):
            global image_preview
            filename = filedialog.askopenfilename()
            if(filename == ''):
                return
            try: image_preview.grid_remove()
            finally:
                filepath_label.config(text = filename)
                fpObj.set_filepath(filename)
                submit_file.grid(row=1, column=0, columnspan=5, pady=(45,0))
                output_master.grid_remove()
                image_preview = self.setImage(filename, 180,180)
                image_preview.grid(row=2, column=0, columnspan=5, sticky=tk.N)
        
        #file upload
        upload_file = tk.Button(file_upload_master, text='Select File', command=uploadAction, borderwidth=1, relief="solid", bg='white')
        upload_file.pack(side = LEFT, padx=5)
        
        #filepath label
        filepath_label = tk.Label(file_upload_master, text="No file selected")
        filepath_label.configure(background='white')
        filepath_label.pack(side = LEFT)
        
        #preview image
        image_preview = self.setImage("muskrat_logo_transparent.png", 240, 150)
        
        def submitFile(event=None):
            filename = fpObj._filepath 

            pred_list = bck.get_list_of_predictions(filename)
            predObj.set_model_pred(pred_list) 
            ht.hashAndWriteToCSV(filename, pred_list)     
            
            global image_preview
            image_preview.grid_remove()
            image_preview.grid(row=2, column=0, columnspan=1, sticky=tk.NE)
            
            output_master.grid(row=2,column=1, columnspan=4, rowspan=3, padx=(80,0), pady=(2,0), sticky=tk.NW)
            
            model1_answer_label.configure(text = CATEGORIES[predObj._model1])
            model2_answer_label.configure(text = CATEGORIES[predObj._model2])
            model3_answer_label.configure(text = CATEGORIES[predObj._model3])
            model4_answer_label.configure(text = CATEGORIES[predObj._model4])
            model5_answer_label.configure(text = CATEGORIES[predObj._model5])
            modelV_answer_label.configure(text = CATEGORIES[predObj._most_common])
            
        #model outputs
        output_master = tk.Frame(self, width=420, height=180, borderwidth=1, relief='solid', bg='white')
        output_master.pack_propagate(False)
        
        output_master.rowconfigure(0, minsize=30)
        output_master.rowconfigure(1, minsize=30)
        output_master.rowconfigure(2, minsize=30)
        output_master.rowconfigure(3, minsize=90)
        
        output_master.columnconfigure(0, minsize=105)
        output_master.columnconfigure(1, minsize=105)
        output_master.columnconfigure(2, minsize=105)
        output_master.columnconfigure(3, minsize=105)
        
        #model 1 results
        model1_result_label = tk.Label(output_master, text="Model 1", bg='white')
        model1_result_label.grid(row=0, column=0)
        model1_answer_label = tk.Label(output_master, text="yes", bg='white')
        model1_answer_label.grid(row=0, column=1)
        
        #model 2 results
        model2_result_label = tk.Label(output_master, text="Model 2", bg='white')
        model2_result_label.grid(row=1, column=0)
        model2_answer_label = tk.Label(output_master, text="yes", bg='white')
        model2_answer_label.grid(row=1, column=1)
        
        #model 3 results
        model3_result_label = tk.Label(output_master, text="Model 3", bg='white')
        model3_result_label.grid(row=0, column=2)
        model3_answer_label = tk.Label(output_master, text="yes", bg='white')
        model3_answer_label.grid(row=0, column=3)
        
        #model 4 results
        model4_result_label = tk.Label(output_master, text="Model 4", bg='white')
        model4_result_label.grid(row=1, column=2)
        model4_answer_label = tk.Label(output_master, text="yes", bg='white')
        model4_answer_label.grid(row=1, column=3)
        
        #model 5 results
        model5_result_label = tk.Label(output_master, text="Model 5", bg='white')
        model5_result_label.grid(row=2, column=0, columnspan=2, sticky=tk.E, padx=(0,20))
        model5_answer_label = tk.Label(output_master, text="yes", bg='white')
        model5_answer_label.grid(row=2, column=2, columnspan=2, sticky=tk.W, padx=(30,0))
        
        #verdict results
        modelV_result_label = tk.Label(output_master, text="Verdict", bg='white')
        modelV_result_label.grid(row=3, column=2, sticky=tk.N, pady=(10,0))
        modelV_answer_label = tk.Label(output_master, text="yes", bg='white')
        modelV_answer_label.grid(row=3, column=2)
        
        #submit button
        submit_file = tk.Button(self, text="Submit", command=submitFile, borderwidth=1, relief="solid", bg='white')
        
    #returns image as useable label
    def setImage(self, filepath, height, width):
        if not filepath.split('/')[-1].split('.')[-1] == 'mp4':
            logo_image = Image.open(filepath)
        else:
            logo_image = Image.fromarray(vid_reader.read_frames(filepath,num_frames=1)[0][0])
        logo_resize = logo_image.resize((height,width))
        logo_final = ImageTk.PhotoImage(logo_resize)
        logo_label = tk.Label(image=logo_final)
        logo_label.Image = logo_final
        logo_label.config(background='white')
        return logo_label

if __name__ == "__main__":
    app = App()
    app.mainloop()
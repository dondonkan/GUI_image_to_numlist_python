import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import cv2 
import datetime


class Application(tk.Frame):
    

    def __init__(self,master):
        super().__init__(master)
        self.pack()
        
        self.master.geometry("300x300")
        self.master.title("GUI_image_to_numpy")

        self.widget()

    def enc_select_file(self):
        self.massage.set("")

        self.typ = [('画像ファイル',['*.jpg','*.png'])]
        self.fil = filedialog.askopenfilename(filetypes = self.typ,initialdir = "./")

        self.value = self.input_box.get()

        if self.value: 
            self.input_box.delete(0, tk.END)

        self.input_box.insert(tk.END, self.fil)

    
    def dec_select_directory(self):
        self.massage.set("")
        
        self.directory = filedialog.askdirectory(initialdir = "./")

        self.value = self.input_box_directory.get()

        if self.value: 
            self.input_box_directory.delete(0, tk.END)

        self.input_box_directory.insert(tk.END, self.directory)
        

    def check_exist_file(self):
        self.key1 = self.input_box.get() #ファイルパスの取得

        #ファイルの存在を確認
        if(os.path.exists(self.key1)):
            return True
           
        else:
            self.fail = tk.Toplevel()
            self.fail.grab_set()

            self.fail_frame = tk.Frame(self.fail)
            self.fail_frame.grid(row=0, column=0, sticky="nsew", pady=20)

            self.fail_label = tk.Label(self.fail_frame,text="画像ファイルを選択してください")
            self.fail_label.grid(row=0,column=0)

            self.button2 = tk.Button(self.fail_frame,text="OK",command=lambda:[self.fail.destroy()])
            self.button2.grid(row=1,column=0,sticky=tk.W+tk.E ,padx=10, pady=10)

            print("no exists file")

    def check_exist_directory(self):

        massage = {
            "r" : False,
            "g" : False,
            "b" : False,
            "type" : False
        }

        self.key1 = self.input_box_directory.get() #フォルダパスの取得

        #フォルダ・r,g,b,type,ファイルの存在を確認
        if(os.path.exists(self.key1)):

            massage["r"] = os.path.exists(self.key1 + '/r.txt')
            massage["g"] = os.path.exists(self.key1 + '/g.txt')
            massage["b"] = os.path.exists(self.key1 + '/b.txt')
            massage["type"] = os.path.exists(self.key1 + '/type.txt')
            
            error_massage = ""

            for i in massage.keys():
                if(massage[i] == False):
                    error_massage += i + ".txtが存在しません\n"   

            if(len(error_massage) > 0):
                self.massage.set(error_massage)
                return False
            else:        
               return True

           
        else:
            self.fail = tk.Toplevel()
            self.fail.grab_set()

            self.fail_frame = tk.Frame(self.fail)
            self.fail_frame.grid(row=0, column=0, sticky="nsew", pady=20)

            self.fail_label = tk.Label(self.fail_frame,text="フォルダを選択してください")
            self.fail_label.grid(row=0,column=0)

            self.button2 = tk.Button(self.fail_frame,text="OK",command=lambda:[self.fail.destroy()])
            self.button2.grid(row=1,column=0,sticky=tk.W+tk.E ,padx=10, pady=10)

            print("no exists file")


    def encode_numfile(self):

        tb = self.check_exist_file() #ファイルの確認　boolen

        if tb:
            print("ok")
            self.img = cv2.imread(self.fil)
            self.root, self.ext = os.path.splitext(self.fil)

            self.now = datetime.datetime.now()

            #load bgr
            self.b, self.g, self.r = cv2.split(self.img)

            new_dir_path = './output_files' + self.now.strftime('%Y%m%d_%H%M%S')

            os.makedirs(new_dir_path,exist_ok=True)

            with open(new_dir_path +'/b.txt','w') as f:
                np.savetxt(f,self.b)
            with open(new_dir_path +'/g.txt','w') as f:
                np.savetxt(f,self.g)
            with open(new_dir_path +'/r.txt','w') as f:
                np.savetxt(f,self.r)
            with open(new_dir_path +'/type.txt','w') as f:
                f.write(self.ext)

            self.massage.set("分割が完了しました")

        else:
            print("no")

    
    def decode_files(self):
        tb = self.check_exist_directory() #フォルダの確認 boolen

        if tb:
            print("ok")

            load_type_path = self.directory + "/type.txt"
            file_type = ""

            with open(load_type_path,'r') as f:
                file_type += f.read()

            print(file_type)
            self.now = datetime.datetime.now()
            

            load_b = np.loadtxt(self.directory + '/b.txt')
            load_g = np.loadtxt(self.directory + '/g.txt')
            load_r = np.loadtxt(self.directory + '/r.txt')

            ##img write##
            load_out_img = cv2.merge((load_b,load_g,load_r))
            cv2.imwrite('output_image_'+ self.now.strftime('%Y%m%d_%H%M%S') + file_type,load_out_img)

            self.massage.set("画像ファイルの統合が完了しました")

        else:
            print("no")
            

    def widget(self):
        #300,300

        self.label = tk.LabelFrame(text="画像ファイル(.jpg , .png)をbgrに分割")
        
        self.input_box = tk.Entry(self.label,width=40)
        self.input_box.grid(row=0,column=0)

        self.button = tk.Button(self.label,text="参照",command= self.enc_select_file)
        self.button.grid(row=0,column=1)

        self.button2 = tk.Button(self.label,text="決定",command= self.encode_numfile)
        self.button2.grid(row=1,column=0)
      
        self.label.pack()


        self.label2 = tk.LabelFrame(text="分割したbgrファイルを画像ファイルに統合")


        self.input_box_directory = tk.Entry(self.label2,width=40)
        self.input_box_directory.grid(row=0,column=0)

        self.button3 = tk.Button(self.label2,text="参照",command= self.dec_select_directory)
        self.button3.grid(row=0,column=1)

        self.button4 = tk.Button(self.label2,text="決定",command= self.decode_files)
        self.button4.grid(row=1,column=0)

        self.label2.pack()

        self.label3 = tk.LabelFrame(text="Status")

        self.massage = tk.StringVar()

        self.massage_box = tk.Label(self.label3,textvariable=self.massage)
        self.massage_box.grid(row=0,column=0)

        self.label3.pack()

        


    


def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()

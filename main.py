import cv2
import numpy as np
import os
import shutil
import pandas as pd
from PIL import ImageFont,ImageDraw,Image

# Coordinates for Student Name positioning, depends on certificate structure
studentX_coordinate = 150
studentY_coordinate = 660

# Coordinates for Director Name positioning, depends on certificate structure
directorX_coordinate = 150
directorY_coordinate = 1120

# GENERTING CERTIFICATES
def certificate_gen(name_ls):

    # Directory name where certificates will be stores
    folderName = 'certificates'

    # Delete folder if already exists
    try:
        shutil.rmtree(folderName)
    except OSError as e:
        print ("Certificate Folder Created!")

    # create folder
    os.mkdir(folderName)

    for name in name_ls:

        template=cv2.imread('certificate.png')
        
        template_conv = cv2.cvtColor(template,cv2.COLOR_BGR2RGB)
        arr_img= Image.fromarray(template_conv)
        var_draw=ImageDraw.Draw(arr_img)
        student_pacifico=ImageFont.truetype("fonts/Pacifico.ttf",90)
        director_pacifico=ImageFont.truetype("fonts/Pacifico.ttf",50)
        
        # sofia_regular = ImageFont.truetype("fonts/Sofia-Regular.otf", 20) # CAN IMPLEMENT MORE THAN ONE FONT
       
        var_draw.text((studentX_coordinate,studentY_coordinate),name,font=student_pacifico,fill='grey') # DEFINING CO-ORDS NAME AND FONT-COLOR
        var_draw.text((directorX_coordinate,directorY_coordinate), "Dr. Hammad Naveed",font=director_pacifico,fill='grey')

        final_res=cv2.cvtColor(np.array(arr_img),cv2.COLOR_RGB2BGR) # RE-CONVERTING IMAGE FROM ARRAY INFO
        cv2.imwrite(os.path.join(folderName, "{}.png".format(name)), final_res) # TO SAVE THE FINAL OUTPUT
        print("{}'s certificate generated".format(name))

      
if __name__=="__main__":

    # Read Names CSV
    try:
        df = pd.read_csv('names.csv')
        name_ls = df['NAMES'].tolist()
    except:
        print("File not found")
        exit()
    
    certificate_gen(name_ls)
    
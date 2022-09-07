import cv2
import numpy as np
import os
import shutil
import pandas as pd
from PIL import ImageFont,ImageDraw,Image

# Coordinates for Name positioning, depends on certificate structure
x_coordinate = 140
y_coordinate = 660

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
        pacifico=ImageFont.truetype("fonts/Pacifico.ttf",90)
        
        # sofia_regular = ImageFont.truetype("fonts/Sofia-Regular.otf", 20) # CAN IMPLEMENT MORE THAN ONE FONT
       
        var_draw.text((x_coordinate,y_coordinate),name,font=pacifico,fill='grey') # DEFINING CO-ORDS NAME AND FONT-COLOR
        final_res=cv2.cvtColor(np.array(arr_img),cv2.COLOR_RGB2BGR) # RE-CONVERTING IMAGE FROM ARRAY INFO
        cv2.imwrite(os.path.join(folderName, "{}.jpg".format(name)), final_res) # TO SAVE THE FINAL OUTPUT
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
    
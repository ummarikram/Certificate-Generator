import cv2
import numpy as np
import os
import shutil
import pandas as pd
import smtplib
from PIL import ImageFont,ImageDraw,Image
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Coordinates for Student Name positioning, depends on certificate structure
studentX_coordinate = 150
studentY_coordinate = 660

# Coordinates for Director Name positioning, depends on certificate structure
directorX_coordinate = 150
directorY_coordinate = 1120

# Sender Credentials
SenderEmail = "ummarikram@gmail.com"
SenderPassword = "sawzupmnjzvjhwfd"

# Email Server
server = smtplib.SMTP('smtp.gmail.com', 587)

def SendMail(ImgFileName, studentName, studentEmail):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'INTELLIGENT NFTS E-CERTIFICATE'
    msg['From'] = SenderEmail
    msg['To'] = studentEmail

    # Body
    text = MIMEText("Dear {},\n\nThank you for joining our event. We hope you had a great time.\n\nHere is your digital certificate.\n\nRegards,\nTeam SPFC X IEEE".format(studentName))

    # Body Attachment
    msg.attach(text)

    # Certificate Attachment
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    # From, To, Msg
    server.sendmail(SenderEmail, studentEmail, msg.as_string())

# GENERTING CERTIFICATES
def certificate_gen(student_list):

    # Directory name where certificates will be stores
    folderName = 'certificates'

    # Delete folder if already exists
    try:
        shutil.rmtree(folderName)
    except OSError as e:
        print ("Certificate Folder Created!")

    # create folder
    os.mkdir(folderName)

    # Establishing Server Connection
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Authenticate
    server.login(SenderEmail, SenderPassword)

    for [name, email] in student_list:

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
        print("{}'s certificate generated!".format(name))

        # SendMail(os.path.join(folderName, "{}.png".format(name)), name, email)
        # print("Email sent to {}!".format(name))
    
    # Terminate Server
    server.quit()

      
if __name__=="__main__":

    # Read Names CSV
    try:
        df = pd.read_csv('names.csv')

        names = df['NAMES'].tolist()

        emails = df['EMAILS'].tolist()

        student_list = zip(names, emails)

    except:
        print("File not found")
        exit()
    
    certificate_gen(student_list)
    

import cv2
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
#############################################
frameWidth = 640
frameHeight = 480
FaceCascade = cv2.CascadeClassifier("Resources/haarcascades/haarcascade_frontalface_default.xml")
minArea = 500
color = (255,0,255)
i = 1 # Initialize the i counter for the face dectection to 1
myPath = 'Data/Images'
minBlur = 500
saveData = True
count = 0
countSave = 0
moduleVal = 10
email_user = 'email_user@gmail.com'
email_password = 'password'
email_send = 'email_send@gmail.com'
subject = 'Person detected notification'
##############################################
def saveDataFunc():
    global countFolder
    countFolder = 0
    while os.path.exists(myPath + str(countFolder)):
        countFolder = countFolder + 1
    os.makedirs(myPath + str(countFolder))
##############################################
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject
body = 'Hi there, there is a person detected. A photo image of the person is attacthed below.'
msg.attach(MIMEText(body,'plain'))
##############################################

if saveData:saveDataFunc()

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
while True:
    success, img = cap.read()

    cv2.imshow("Result", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = FaceCascade.detectMultiScale(imgGray, 1.1, 10)
    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Detection Successful", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)

            imgRoi = img[y:y + h, x:x + w]
            cv2.imshow("ROI", imgRoi)
            cv2.imshow("Result", img)

            # Condition to check when a face is detected
            if i == 1:  # If more then one person is to be detected then the statement can be changed to || i == 2......
                #  i=i+1
                if (area > minArea):

                    if saveData:
                        blur = cv2.Laplacian(img, cv2.CV_64F).var()
                        if count % moduleVal == 0 and blur > minBlur:
                            nowTime = time.time()
                            cv2.imwrite(myPath + str(countFolder) + '/' + str(countSave) + " " + str(int(blur)) + " " + str(nowTime) + ".png", img)
                            imagepath = (myPath + str(countFolder) + '/' + str(countSave) + " " + str(int(blur)) + " " + str(nowTime) + ".png")
                            localpath = "C:/Users/rawin/PycharmProjects/ReceptionSystem/"
                            path = localpath + (myPath + str(countFolder) + '/' + str(countSave) + " " + str(int(blur)) + " " + str(nowTime) + ".png")
                            print(path)
                            print(localpath + imagepath)

                            filename = path
                            attachment = open(filename, 'rb')

                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload((attachment).read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', "attachment; filename= " + filename)

                            msg.attach(part)
                            text = msg.as_string()
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(email_user, email_password)

                            server.sendmail(email_user, email_send, text)
                            server.quit()

                            countSave += 1
                            saveData = False



                    i = i + 1
                    print('Successful')

    cv2.imshow("Result", img)
    cv2.waitKey(500)

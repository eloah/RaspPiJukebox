#Jukebox app Desktop type for deploying it on Raspberry Pi with Jukebox Device.
#Existing 4 categories of 4 songs for each.
#Selecting the songs is done with push buttons.
#Utilizes PySide library for GUI development.
#Uses pygame library for playing music files.

import pygame
from PySide.QtGui import *
from PySide.QtCore import * 
import sys
import time
import RPi.GPIO as GPIO
from subprocess import call

#Setting up working push buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_UP)                
GPIO.setup(20,GPIO.IN,pull_up_down=GPIO.PUD_UP)                
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP)                
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP)                

GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_UP)                
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_UP)                
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP)                
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)                 

#Shutting down push button
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)                 

status = 0
category = 0
song = 0
bspace = 0

#Main window class
class Jukebox(QMainWindow):
    
    def __init__(self, parent = None):
        super(Jukebox, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        #self.resize(600, 320)
        self.setWindowTitle('Jukebox')
        
        self.setStyleSheet(
        "QMainWindow{background-image: url(/home/pi/Desktop/Jukebox/back.jpg);}"
        
        "QLabel{background-color: white;\n"
        "    background-repeat:none;\n"
        "    border-style: solid;\n"
        "    border-width: 8px;\n"
        "    border-radius: 25px;\n"
        "    border-color: #E64B3C;\n"
        "    font-size:40px;\n"
        "    font-style:bold;\n"
        "    color:#2C3C4C}"     )
        self.setMinimumSize(QSize(1280, 1024))
        self.setMaximumSize(QSize(1280, 1024))
        self.setWindowFlags(Qt.FramelessWindowHint)
    
        self.cat1 = QLabel("Entexno",self)
        self.cat1.setGeometry(112, 310, 225, 70)
        self.cat1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.cat1.hide()
     
        self.cat2 = QLabel("Opera",self)
        self.cat2.setGeometry(112, 482, 225, 70)
        self.cat2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.cat2.hide()
    
        self.cat3 = QLabel("Laika",self)
        self.cat3.setGeometry(112, 654, 225, 70)
        self.cat3.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.cat3.hide()
        
        self.cat4 = QLabel("Rock",self)
        self.cat4.setGeometry(113, 826, 225, 70)
        self.cat4.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.cat4.hide()
        
        
        self.song1 = QLabel(self)
        self.song1.hide()
        self.song1.setGeometry(952, 312, 225, 70)
        self.song1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.song1.setText("1st Track")
        
        self.song2 = QLabel(self)
        self.song2.hide()
        self.song2.setGeometry(952, 484, 225, 70)
        self.song2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.song2.setText("2nd Track")
        
        self.song3 = QLabel(self)
        self.song3.hide()
        self.song3.setGeometry(952, 656, 225, 70)
        self.song3.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.song3.setText("3rd Track")
        
        self.song4 = QLabel(self)
        self.song4.hide()
        self.song4.setGeometry(952, 828, 225, 70)
        self.song4.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.song4.setText("4th Track")
    
        self.bspace = QLabel(self)
        self.bspace.hide()
        self.bspace.setGeometry(524, 828, 225, 70)
        self.bspace.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.bspace.setText("B-Space")
    
        self.songName = QLabel(self)
        self.songName.setGeometry(395,450,500,120)
        self.songName.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.songName.setText("Welcome to Jukebox!")
        self.songName.setStyleSheet("background-color: none;\n"
        "    background-repeat:none;\n"
        "    border-style: none;\n"
        "    font-size:48px;\n")
    
    
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.welcome)
        self.timer.start(3000)
        
        self.workerThread = workerThread()
        self.workerThread.start()
        self.connect(self.workerThread,SIGNAL('send(int,int,int,int)'), self.jukeboxController)
        
        self.show()
        
        
    
    def welcome(self):
        self.songName.setText("")
        self.cat1.show()
        self.cat2.show()
        self.cat3.show()
        self.cat4.show()
        self.timer.stop()
        self.songName.setStyleSheet("background-color: none;\n"
        "    background-repeat:none;\n"
        "    border-style: none;\n"
        "    font-size:36px;\n")
    
    #Rules for selecting and playing the songs
    def jukeboxController(self, status, category, song, bspace):
        pygame.mixer.init()
        print (status,category,song)
        if song and status == 2 and bspace == 2:
            pygame.mixer.music.stop()
    
        if status == 0 and bspace == 0 and category == 0 and song == 0:
            self.cat1.show()
            self.cat2.show()
            self.cat3.show()
            self.cat4.show()
            self.bspace.hide()
            self.song1.hide()
            self.song2.hide()
            self.song3.hide()
            self.song4.hide()
            self.songName.setText("")
        if status == 1: 
            if category == 1:
                pygame.mixer.music.stop()
                self.cat2.hide()
                self.cat3.hide()
                self.cat4.hide()
                self.song1.show()
                self.song2.show()
                self.song3.show()
                self.song4.show()
                self.bspace.show()
                self.songName.setText("")
            elif category == 2:
                pygame.mixer.music.stop()
                self.cat1.hide()
                self.cat3.hide()
                self.cat4.hide()
                self.song1.show()
                self.song2.show()
                self.song3.show()
                self.song4.show()
                self.bspace.show()
                self.songName.setText("")
            elif category == 3:
                pygame.mixer.music.stop()
                self.cat1.hide()
                self.cat2.hide()
                self.cat4.hide()
                self.song1.show()
                self.song2.show()
                self.song3.show()
                self.song4.show()
                self.bspace.show()
                self.songName.setText("")  
            elif category == 4:
                pygame.mixer.music.stop()
                self.cat1.hide()
                self.cat3.hide()
                self.cat2.hide()
                self.song1.show()
                self.song2.show()
                self.song3.show()
                self.song4.show()
                self.bspace.show()
                self.songName.setText("") 
        #Choose the song and play, 4 songs for each category
        if status == 2 and category == 1 and song == 1:
                #if song == 1:
                    self.song2.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Nikos Papazoglou\n Augoustos")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category1 - Entexno/Nikos Papazoglou Augoustos.wav")
                    pygame.mixer.music.play()
                    print("Playing S1")
                    print(status,category,song)
        elif status == 2 and category == 1 and song == 2:
                    self.song1.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Pix Lax\n Anohtes agapes")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category1 - Entexno/Pix Lax Anohtes agapes.wav")
                    pygame.mixer.music.play()
                    print("Playing S2")
        elif status == 2 and category == 1 and song == 3:
                    self.song1.hide()
                    self.song2.hide()
                    self.song4.hide()
                    self.songName.setText("Xrhstos Thyvaios\n Poso poly s'agaphsa")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category1 - Entexno/Poso poly sagaphsa Xrhstos Thyvaios.wav")
                    pygame.mixer.music.play()
                    print("Playing S3")
        elif status == 2 and category == 1 and song == 4:
                    self.song1.hide()
                    self.song2.hide()
                    self.song3.hide()
                    self.songName.setText("Pix Lax\n Poula me")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category1 - Entexno/Pix Lax Poula me.wav")
                    pygame.mixer.music.play()
                    print("Playing S4")
    
        if status == 2 and category == 2 and song == 1:
                #if song == 1:
                    self.song2.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("María Callas\n Un bel dì vedremo")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category2 - Opera/María Callas Un bel dì vedremo.wav")
                    pygame.mixer.music.play()
                    print("Playing S1")
        elif status == 2 and category == 2 and song == 2:
                    self.song1.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Placido Domingo\n E lucevan le stelle")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category2 - Opera/Placido Domingo E lucevan le stelle.wav")
                    pygame.mixer.music.play()
                    print("Playing S2")
        elif status == 2 and category == 2 and song == 3:
                    self.song1.hide()
                    self.song2.hide()
                    self.song4.hide()
                    self.songName.setText("Luciano Pavarotti\n 'O sole mio")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category2 - Opera/Luciano Pavarotti  'O sole mio.wav")
                    pygame.mixer.music.play()
                    print("Playing S3")
        elif status == 2 and category == 2 and song == 4:
                    self.song1.hide()
                    self.song2.hide()
                    self.song3.hide()
                    self.songName.setText("Elina Garanca\n L'amour est un oiseau rebelle")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category2 - Opera/Elina Garanca L'amour est un oiseau rebelle.wav")
                    pygame.mixer.music.play()
                    print("Playing S4")
        
        if status == 2 and category == 3 and song == 1:
                #if song == 1:
                    self.song2.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Dimitris Mitropanos\n Roza")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category3 - Laika/Dimitris Mitropanos Roza.wav")
                    pygame.mixer.music.play()
                    print("Playing S1")
        elif status == 2 and category == 3 and song == 2:
                    self.song1.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Giwrgos Zampetas\n Oi Thalassinoi")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category3 - Laika/Giwrgos Zampetas Oi Thalassinoi.wav")
                    pygame.mixer.music.play()
                    print("Playing S2")
        elif status == 2 and category == 3 and song == 3:
                    self.song1.hide()
                    self.song2.hide()
                    self.song4.hide()
                    self.songName.setText("Stelios Kazantzidis\n Madoubala")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category3 - Laika/Stelios Kazantzidis Madoubala.wav")
                    pygame.mixer.music.play()
                    print("Playing S3")
        elif status == 2 and category == 3 and song == 4:
                    self.song1.hide()
                    self.song2.hide()
                    self.song3.hide()
                    self.songName.setText("Stratos Dionisiou\n Enas Aitos Gremistike")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category3 - Laika/Stratos Dionisiou Enas Aitos Gremistike.wav")
                    pygame.mixer.music.play()
                    print("Playing S4")
    
        if status == 2 and category == 4 and song == 1:
                #if song == 1:
                    self.song2.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Dorothy\n Down to the bottom")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category4 - Rock/Dorothy Down to the bottom.wav")
                    pygame.mixer.music.play()
                    print("Playing S1")
        elif status == 2 and category == 4 and song == 2:
                    self.song1.hide()
                    self.song3.hide()
                    self.song4.hide()
                    self.songName.setText("Red Hot Chili Peppers\n Californication")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category4 - Rock/Red Hot Chili Peppers  Californication.wav")
                    pygame.mixer.music.play()
                    print("Playing S2")
        elif status == 2 and category == 4 and song == 3:
                    self.song1.hide()
                    self.song2.hide()
                    self.song4.hide()
                    self.songName.setText("Vasilis Papakonstantinou\n Ena karavi")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category4 - Rock/Vasilis Papakonstantinou Ena karavi.wav")
                    pygame.mixer.music.play()
                    print("Playing S3")
        elif status == 2 and category == 4 and song == 4:
                    self.song1.hide()
                    self.song2.hide()
                    self.song3.hide()
                    self.songName.setText("Green Day\n Boulevard of broken dreams")
                    pygame.mixer.music.load("/home/pi/Desktop/Jukebox/Category4 - Rock/Green Day Boulevard of Broken Dreams.wav")
                    pygame.mixer.music.play()
                    print("Playing S4")
    
        
        
    
        
    
#Thread class for controlling the Jukebox                
class workerThread(QThread):
    def __init__(self, parent=None):
        super(workerThread, self).__init__(parent)
    
    #Controlling push buttons
    def btnController(self):
        global status
        global category
        global song
        global bspace
        send = Signal(int,int,int,int)
        while True:
            btnBack = GPIO.input(5)
            if btnBack == False and status == 1 and (bspace == 1 or bspace == 0) and category:
                    status = 0
                    category = 0
                    bspace = 0
                    self.send.emit(status,category,song,bspace)
                    print ("BackSpace")
            elif btnBack == False and status == 2 and bspace == 2 and song:
                    status = 1
                    bspace = 1
                    song = 0
                    self.send.emit(status,category,song,bspace)
                    print ("BackSpace")

    
            btnCat1 = GPIO.input(21)
            if btnCat1 == False and not category:
                status = 1
                category = 1
                bspace == 1
                print (str(status)+"  "+str(category))
                self.send.emit(status,category,song,bspace)
            
            btnCat2 = GPIO.input(20)
            if btnCat2 == False and not category:
                status = 1
                category = 2
                bspace == 1
                print (str(status)+"  "+str(category))
                self.send.emit(status,category,song,bspace)
            
            btnCat3 = GPIO.input(16)
            if btnCat3 == False and not category:
                status = 1
                category = 3
                bspace == 1
                print (str(status)+"  "+str(category))
                self.send.emit(status,category,song,bspace)
            
            btnCat4 = GPIO.input(12)
            if btnCat4 == False and not category:
                status = 1
                category = 4
                bspace == 1
                print (str(status)+"  "+str(category))
                self.send.emit(status,category,song,bspace)

            btnSong1 = GPIO.input(26)
            if btnSong1 == False and not song and status == 1:
                status = 2
                song = 1
                bspace = 2
                print (str(status)+"  "+str(song))
                self.send.emit(status,category,song,bspace)
            
            btnSong2 = GPIO.input(19)
            if btnSong2 == False and not song and status == 1:
                status = 2
                song = 2
                bspace = 2
                print (str(status)+"  "+str(song))
                self.send.emit(status,category,song,bspace)
               
            btnSong3 = GPIO.input(13)
            if btnSong3 == False and not song and status == 1:
                status = 2
                song = 3
                bspace = 2
                print (str(status)+"  "+str(song))
                self.send.emit(status,category,song,bspace)
    
            btnSong4 = GPIO.input(6)
            if btnSong4 == False and not song and status == 1:
                status = 2
                song = 4
                bspace = 2
                print (str(status)+"  "+str(song))
                self.send.emit(status,category,song,bspace)
            
            if btnBack == False and btnSong4 == False:
                call("sudo shutdown now",shell=True)
            time.sleep(0.3)
        
        return
    
    def run(self):
        self.btnController()
                

                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = Jukebox()
    sys.exit(app.exec_())

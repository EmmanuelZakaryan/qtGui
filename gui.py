from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QTimer
import firebase_admin
from firebase_admin import credentials, firestore
import sys
from threading import Thread
import cv2
from pyzbar import pyzbar
from time import time, sleep
from ast import literal_eval
import os

app = QtWidgets.QApplication([])
dlg = uic.loadUi("gui/page1.ui")

app2 = QtWidgets.QApplication([])
dlg2 = uic.loadUi("gui/page2.ui")


def updateGui():
    global d

    old = None
    name = ""

    while True:
        
        try:
            c = open("actual.txt", "r").readlines()
        except:
            print("couldnt read")
            continue

        #sprint(c)

        if c == "" or c == " " or c == "\n" or c == []:
            dlg2.hide()
            pass
        else:
            print("showing gui --1")
            dlg2.show()
            d = literal_eval(c[0])
            name = c[1]

            if old == d:
                pass
            else:
                #dlg2.show()
                print("here")
                refresh(d, name)

                old = d


        sleep(0.05)


def refresh(d, name):

    print("in refresh")

    #dlg2.show()

    dlg2.nacier.setText(str(d["acier"]))
    dlg2.nalu.setText(str(d["alu"]))
    dlg2.npet.setText(str(d["pet"]))
    dlg2.nverre.setText(str(d["verre"]))
    dlg2.ntetra.setText(str(d["tetra"]))

    n = d["acier"]+d["alu"]+d["verre"]+d["pet"]+d["tetra"]

    dlg2.points.setText( "points : " + str(n))

    dlg2.name.setText("Bonjour " + name)

    print(d)

    print("out refresh")



def connection():

    global permissionConnection
    global p

    cam2 = cv2.VideoCapture(1)
    count = 0

    start = 0
    start2 = 0

    #page(None)
    print("Starting Qr connection")

    while True:
        
        count +=1

        if count == 10000000:
            print("in while from connection")
            count = 0

        ok, im = cam2.read()
        #cv2.imshow("test", im)
        cv2.waitKey(1)
        
        name = pyzbar.decode(im)

        #print("permission connection {}".format(permissionConnection))
        
        #print(name)

        nameBool = False

        if (name == [] or name == "" or name == " " or name == None):
            nameBool = False
        else:
            nameBool = True

        #print(nameBool)

        if  time() - start2 > 10 and nameBool == True and permissionConnection == True and name[0][1] == "QRCODE":
            
            name = name[0][0].decode("utf-8")
            print(name)
            
            if p.name == None:
                p.name = name

                dlg2.show()
                dlg2.name.setText("Bonjour " + name)

                Thread(target=session, args=(name,)).start()
                
                #dlg2.show()
                print("Connexion de {}".format(name))
                
                #Thread(target=p.talk, args=(name,)).start()

                start = time()

            else:
                if name == p.name:
                    if time() - start > 10:
                        print("Deconnexion de {}".format(name))

                        start2 = time()

                        #dlg.show()

                        dlg2.hide()
                        dlg2.name.setText("Bonjour ")

                        Thread(target=p.deco).start()
                        
                        if "Emmanuel" in name:
                            Thread(target=sms.sendDeconnexion).start()

                        #p.name = None
                        


                        #Thread(target=play, args=("deco",)).start()
                    # else:
                    #     print("Vous venez de vous connecter")

Thread(target=updateGui).start()

dlg.show()


sys.exit(app2.exec_())
sys.exit(app.exec_())

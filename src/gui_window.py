# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from datetime import datetime
from image_processing import Image, np, reconstruct_image, split_parts_list
from scheme import Scheme, spec_chars, spec_chars_key


class Ui_ShamirSecretSharing(object):

    def browse_img(self):
        while True:
            pname, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Odaberi sliku", '.', "(*.tif *.tiff *.jpg *.jpeg *.gif *.png *.bmp *.eps *.raw *.cr2 "
                                                                                               "*.nef *.orf *.sr2)")
            print(pname)
            if pname is not None:
                break
        image_profile = QtGui.QImage(pname)  # QImage objekat
        image_profile = image_profile.scaled(331, 251, aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)  # skaliranje slike na 331x251 i ocuvanje aspect ratio
        self.label_29.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.path_image = pname
        self.dir_name = path.dirname(pname)

    def encrypt_img(self):
        self.listWidget.clear()
        if self.label_29.pixmap() is None:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Молим унесите слику")
            self.error_message.exec_()
        elif self.spinBox.value() == 0 or self.spinBox.value() < self.spinBox_2.value() or self.spinBox_2.value() == 0 or self.spinBox.value() < 2 or self.spinBox_2.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Неки од броја подјела није добар")
            self.error_message.exec_()
        else:
            self.img_name, self.ext = path.splitext(self.path_image)
            t1 = datetime.now()
            pic = Image.open(self.path_image)
            matrix = np.array(pic, np.int32)
            self.sharesRGB = split_parts_list(self.spinBox.value(), self.spinBox_2.value(), 257, matrix, self.path_image)
            print("Vrijeme kreiranja podjela: ")
            print((datetime.now() - t1).seconds)
            self.label_5.setText(self.dir_name)
            i = 0
            for v in range(self.spinBox.value()):
                share_path = self.img_name + "_share" + str(i) + ".png"
                i += 1
                self.listWidget.addItem(share_path)

    def encrypt_text(self):
        self.listWidget_4.clear()
        if self.textEdit.toPlainText() is None or self.textEdit.toPlainText() == "":
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Молим унесите текст за енкрипцију")
            self.error_message.exec_()
        elif self.spinBox_4.value() == 0 or self.spinBox_4.value() < self.spinBox_3.value() or self.spinBox_3.value() == 0 or self.spinBox_3.value() < 2 or self.spinBox_4.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Неки од броја подјела није добар")
            self.error_message.exec_()
        else:
            self.secret_text = self.textEdit.toPlainText()
            text = [ord(c) for c in self.secret_text]
            self.glavna_lista = [[] for i in range(len(self.secret_text))]
            shares, lista = [], []
            for el in text:
                s = Scheme(el, self.spinBox_4.value(), self.spinBox_3.value(), 127)
                shares = s.construct_shares()
                lista.append(shares)

            print(lista)
            self.text_shares = lista
            words_list = [''] * self.spinBox_4.value()
            for dic in lista:
                dict_variable = {}
                counter = 0
                for (key, value) in dic.items():
                    if value < 32:
                        dict_variable[key] = spec_chars[value]
                        words_list[counter] += dict_variable[key]
                    else:
                        dict_variable[key] = chr(value)
                        words_list[counter] += dict_variable[key]
                    counter += 1
                print(dict_variable)
            print(words_list)

            for word in words_list:
                self.listWidget_4.addItem(word)

    def encrypt_number(self):
        self.listWidget_6.clear()
        if self.spinBox_5.value() == 0:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка",
                                                       "Молим унесите број за енкрипцију")
            self.error_message.exec_()
        elif self.spinBox_12.value() == 0 or self.spinBox_12.value() < self.spinBox_11.value() or self.spinBox_11.value() == 0 or self.spinBox_12.value() < 2 or self.spinBox_11.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка",
                                                       "Неки од броја подјела није добар")
            self.error_message.exec_()
        else:
            secret = self.spinBox_5.value()
            self.secret_number = Scheme(secret, self.spinBox_12.value(), self.spinBox_11.value(), 5000003863) # 5000003863 2147483869
            self.shares_number = self.secret_number.construct_shares()
            for sh in self.shares_number:
                self.listWidget_6.addItem(str(self.shares_number[sh]))
            self.inputs = []

    def add_share(self):
        if self.label_29.pixmap() is None:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Слика није енкриптована")
            self.error_message.exec_()
        elif self.spinBox.value() == 0 or self.spinBox.value() < self.spinBox_2.value() or self.spinBox_2.value() == 0 or self.spinBox.value() < 3 or self.spinBox_2.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка",
                                                       "Неки од броја подјела није добар")
            self.error_message.exec_()
        else:
            imgs = []
            for i in range(self.spinBox_2.value()):
                pname, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Odaberi sliku", '', "(*.png)")
                if pname is not None and pname is not "":
                    imgs.append(pname)
                    self.listWidget_2.addItem(pname)
            self.shares_for_reconstruction = imgs

    def add_text_share(self):
        if self.textEdit.toPlainText() is None or self.textEdit.toPlainText() == "":
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Молим унесите текст за енкрипцију")
            self.error_message.exec_()
        elif self.spinBox_4.value() == 0 or self.spinBox_4.value() < self.spinBox_3.value() or self.spinBox_3.value() == 0 or self.spinBox_3.value() < 2 or self.spinBox_4.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Неки од броја подјела није добар")
            self.error_message.exec_()
        else:
            word = self.textEdit_3.toPlainText()
            self.listWidget_5.addItem(word)
            self.textEdit_3.clear()

            counter = 0
            for el in word:
                ord_el = int(ord(el))
                if ord_el > 126:
                    self.glavna_lista[counter].append(spec_chars_key[el])
                else:
                    self.glavna_lista[counter].append(ord_el)
                counter += 1

    def add_number_share(self):
        self.inputs.append(self.spinBox_13.value())
        self.listWidget_7.addItem(str(self.spinBox_13.value()))

    def decrypt_images(self):
        if self.label_29.pixmap() is None:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Слика није енкриптована")
            self.error_message.exec_()
        elif self.spinBox.value() == 0 or self.spinBox.value() < self.spinBox_2.value() or self.spinBox_2.value() == 0 or self.spinBox.value() < 3 or self.spinBox_2.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Неки од броја подјела није добар")
            self.error_message.exec_()
        elif self.listWidget_2.count() < self.spinBox_2.value():
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Није унешено довољно слика")
            self.error_message.exec_()
        else:
            matrix = reconstruct_image(self.shares_for_reconstruction, self.spinBox_2.value(), 257, self.sharesRGB)
            new_img = Image.fromarray(matrix.astype('uint8'), 'RGB')
            new_img.save(self.img_name+"_SECRET" + self.ext)
            image_profile = QtGui.QImage(self.img_name+"_SECRET" + self.ext)  # QImage objekat
            image_profile = image_profile.scaled(331, 251, aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                 transformMode=QtCore.Qt.SmoothTransformation)  # skaliranje slike na 331x251 i ocuvanje aspect ratio
            self.label_30.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.listWidget_2.clear()

    def decrypt_text(self):
        if self.textEdit.toPlainText() is None or self.textEdit.toPlainText() == "":
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Молим унесите текст за енкрипцију")
            self.error_message.exec_()
        elif self.spinBox_4.value() == 0 or self.spinBox_4.value() < self.spinBox_3.value() or self.spinBox_3.value() == 0 or self.spinBox_3.value() < 2 or self.spinBox_4.value() < 2:
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Неки од броја подјела није добар")
            self.error_message.exec_()
        elif self.listWidget_5.count() < self.spinBox_3.value():
            self.error_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Грешка", "Није унешено довољно дијелова")
            self.error_message.exec_()
        else:
            reconstructed_secret = ""
            b = 0
            for dic in self.text_shares:
                reconstructed_secret += chr(int(Scheme.reconstruct_secret_img(dic, self.glavna_lista[b], self.spinBox_3.value(), 127)))
                b += 1
            self.textEdit_2.setText(reconstructed_secret)
            self.listWidget_5.clear()
            self.glavna_lista = [[] for i in range(len(self.secret_text))]

    def decrypt_number(self):
        returned_secret = int(round(self.secret_number.reconstruct_secret(self.shares_number, self.inputs, self.spinBox_11.value(), 5000003863))) # 5000003863 2147483869
        print(returned_secret)
        self.lcdNumber.display(returned_secret)
        self.listWidget_7.clear()
        self.inputs = []

    def setupUi(self, ShamirSecretSharing):
        ShamirSecretSharing.setObjectName("ShamirSecretSharing")
        ShamirSecretSharing.setEnabled(True)
        ShamirSecretSharing.resize(1121, 854)
        self.centralwidget = QtWidgets.QWidget(ShamirSecretSharing)
        self.centralwidget.setObjectName("centralwidget")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(0, 0, 1121, 821))
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox.setMidLineWidth(0)
        self.toolBox.setObjectName("toolBox")
        self.Slika = QtWidgets.QWidget()
        self.Slika.setObjectName("Slika")

        self.pushButton = QtWidgets.QPushButton(self.Slika)
        self.pushButton.setGeometry(QtCore.QRect(10, 260, 331, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.browse_img)
        self.pushButton.setStyleSheet("border:1px solid #e6f5ff;")
        self.progressBar = QtWidgets.QProgressBar(self.Slika)
        self.progressBar.setGeometry(QtCore.QRect(420, 10, 271, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet("border:1px solid #e6f5ff;")
        self.pushButton_2 = QtWidgets.QPushButton(self.Slika)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 220, 241, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.encrypt_img)
        self.pushButton_2.setStyleSheet("border:1px solid #e6f5ff;")
        self.label = QtWidgets.QLabel(self.Slika)
        self.label.setGeometry(QtCore.QRect(420, 50, 231, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Slika)
        self.label_2.setGeometry(QtCore.QRect(420, 120, 231, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.Slika)
        self.spinBox.setGeometry(QtCore.QRect(490, 70, 81, 31))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setStyleSheet("border:1px solid #e6f5ff;")
        self.spinBox_2 = QtWidgets.QSpinBox(self.Slika)
        self.spinBox_2.setGeometry(QtCore.QRect(490, 140, 81, 31))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setStyleSheet("border:1px solid #e6f5ff;")
        self.progressBar_2 = QtWidgets.QProgressBar(self.Slika)
        self.progressBar_2.setGeometry(QtCore.QRect(420, 430, 271, 23))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.progressBar_2.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_3 = QtWidgets.QLabel(self.Slika)
        self.label_3.setGeometry(QtCore.QRect(780, 300, 331, 20))
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.scrollArea = QtWidgets.QScrollArea(self.Slika)
        self.scrollArea.setGeometry(QtCore.QRect(780, 90, 331, 216))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 329, 214))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_4 = QtWidgets.QLabel(self.Slika)
        self.label_4.setGeometry(QtCore.QRect(780, 0, 111, 41))
        self.label_4.setObjectName("label_4")
        self.scrollArea_12 = QtWidgets.QScrollArea(self.Slika)
        self.scrollArea_12.setGeometry(QtCore.QRect(900, 0, 211, 61))
        self.scrollArea_12.setWidgetResizable(True)
        self.scrollArea_12.setObjectName("scrollArea_12")
        self.scrollArea_12.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents_12 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_12.setGeometry(QtCore.QRect(0, 0, 209, 59))
        self.scrollAreaWidgetContents_12.setObjectName("scrollAreaWidgetContents_12")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_12)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.scrollArea_12.setWidget(self.scrollAreaWidgetContents_12)
        self.pushButton_4 = QtWidgets.QPushButton(self.Slika)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 690, 241, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.decrypt_images)
        self.pushButton_4.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.Slika)
        self.scrollArea_2.setGeometry(QtCore.QRect(350, 470, 381, 161))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea_2.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 379, 159))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget_2 = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidget_2.setObjectName("listWidget_2")
        self.horizontalLayout_2.addWidget(self.listWidget_2)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.label_6 = QtWidgets.QLabel(self.Slika)
        self.label_6.setGeometry(QtCore.QRect(370, 630, 341, 20))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.Slika)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 477, 93, 141))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.add_share)
        self.pushButton_3.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_7 = QtWidgets.QLabel(self.Slika)
        self.label_7.setGeometry(QtCore.QRect(780, 440, 331, 21))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_29 = QtWidgets.QLabel(self.Slika)
        self.label_29.setGeometry(QtCore.QRect(10, 0, 331, 251))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.Slika)
        self.label_30.setGeometry(QtCore.QRect(780, 470, 331, 251))
        self.label_30.setObjectName("label_30")
        self.toolBox.addItem(self.Slika, " Слика ")
        self.Tekst = QtWidgets.QWidget()
        self.Tekst.setObjectName("Tekst")
        self.textEdit = QtWidgets.QTextEdit(self.Tekst)
        self.textEdit.setGeometry(QtCore.QRect(20, 50, 331, 301))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_8 = QtWidgets.QLabel(self.Tekst)
        self.label_8.setGeometry(QtCore.QRect(20, 20, 331, 20))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.pushButton_5 = QtWidgets.QPushButton(self.Tekst)
        self.pushButton_5.setGeometry(QtCore.QRect(430, 320, 241, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.encrypt_text)
        self.pushButton_5.setStyleSheet("border:1px solid #e6f5ff;")
        self.spinBox_3 = QtWidgets.QSpinBox(self.Tekst)
        self.spinBox_3.setGeometry(QtCore.QRect(500, 210, 81, 31))
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_3.setStyleSheet("border:1px solid #e6f5ff;")
        self.spinBox_4 = QtWidgets.QSpinBox(self.Tekst)
        self.spinBox_4.setGeometry(QtCore.QRect(500, 130, 81, 31))
        self.spinBox_4.setObjectName("spinBox_4")
        self.spinBox_4.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_9 = QtWidgets.QLabel(self.Tekst)
        self.label_9.setGeometry(QtCore.QRect(430, 110, 231, 16))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.progressBar_3 = QtWidgets.QProgressBar(self.Tekst)
        self.progressBar_3.setGeometry(QtCore.QRect(430, 50, 271, 23))
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setObjectName("progressBar_3")
        self.progressBar_3.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_10 = QtWidgets.QLabel(self.Tekst)
        self.label_10.setGeometry(QtCore.QRect(430, 190, 231, 16))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.Tekst)
        self.label_11.setGeometry(QtCore.QRect(750, 300, 351, 20))
        self.label_11.setScaledContents(False)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.pushButton_6 = QtWidgets.QPushButton(self.Tekst)
        self.pushButton_6.setGeometry(QtCore.QRect(430, 690, 241, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.decrypt_text)
        self.pushButton_6.setStyleSheet("border:1px solid #e6f5ff;")
        self.progressBar_4 = QtWidgets.QProgressBar(self.Tekst)
        self.progressBar_4.setGeometry(QtCore.QRect(430, 420, 271, 23))
        self.progressBar_4.setProperty("value", 0)
        self.progressBar_4.setObjectName("progressBar_4")
        self.progressBar_4.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_12 = QtWidgets.QLabel(self.Tekst)
        self.label_12.setGeometry(QtCore.QRect(750, 390, 351, 20))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.textEdit_2 = QtWidgets.QTextEdit(self.Tekst)
        self.textEdit_2.setGeometry(QtCore.QRect(750, 420, 351, 301))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setStyleSheet("border:1px solid #e6f5ff;")
        self.pushButton_7 = QtWidgets.QPushButton(self.Tekst)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 690, 331, 28))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.add_text_share)
        self.pushButton_7.setStyleSheet("border:1px solid #e6f5ff;")
        self.textEdit_3 = QtWidgets.QTextEdit(self.Tekst)
        self.textEdit_3.setGeometry(QtCore.QRect(20, 450, 331, 231))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.Tekst)
        self.scrollArea_3.setGeometry(QtCore.QRect(740, 40, 361, 261))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollArea_3.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents_13 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_13.setGeometry(QtCore.QRect(0, 0, 359, 259))
        self.scrollAreaWidgetContents_13.setObjectName("scrollAreaWidgetContents_13")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_13)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.listWidget_4 = QtWidgets.QListWidget(self.scrollAreaWidgetContents_13)
        self.listWidget_4.setObjectName("listWidget_4")
        self.horizontalLayout_4.addWidget(self.listWidget_4)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_13)
        self.scrollArea_4 = QtWidgets.QScrollArea(self.Tekst)
        self.scrollArea_4.setGeometry(QtCore.QRect(380, 450, 351, 231))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollArea_4.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 349, 229))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.listWidget_5 = QtWidgets.QListWidget(self.scrollAreaWidgetContents_4)
        self.listWidget_5.setObjectName("listWidget_5")
        self.horizontalLayout_5.addWidget(self.listWidget_5)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.toolBox.addItem(self.Tekst, " Текст ")
        self.Broj = QtWidgets.QWidget()
        self.Broj.setObjectName("Broj")
        self.spinBox_5 = QtWidgets.QSpinBox(self.Broj)
        self.spinBox_5.setGeometry(QtCore.QRect(20, 90, 381, 41))
        self.spinBox_5.setStyleSheet("border:1px solid #e6f5ff;")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_5.setFont(font)
        self.spinBox_5.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_5.setObjectName("spinBox_5")
        self.spinBox_5.setMaximum(2147483647)
        self.label_13 = QtWidgets.QLabel(self.Broj)
        self.label_13.setGeometry(QtCore.QRect(20, 20, 381, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.pushButton_16 = QtWidgets.QPushButton(self.Broj)
        self.pushButton_16.setGeometry(QtCore.QRect(450, 250, 241, 28))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_16.clicked.connect(self.encrypt_number)
        self.pushButton_16.setStyleSheet("border:1px solid #e6f5ff;")
        self.label_27 = QtWidgets.QLabel(self.Broj)
        self.label_27.setGeometry(QtCore.QRect(450, 160, 231, 16))
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.Broj)
        self.label_28.setGeometry(QtCore.QRect(450, 80, 231, 16))
        self.label_28.setAlignment(QtCore.Qt.AlignCenter)
        self.label_28.setObjectName("label_28")
        self.spinBox_11 = QtWidgets.QSpinBox(self.Broj)
        self.spinBox_11.setGeometry(QtCore.QRect(520, 180, 81, 31))
        self.spinBox_11.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_11.setObjectName("spinBox_11")
        self.spinBox_11.setStyleSheet("border:1px solid #e6f5ff;")
        self.progressBar_9 = QtWidgets.QProgressBar(self.Broj)
        self.progressBar_9.setGeometry(QtCore.QRect(450, 20, 271, 23))
        self.progressBar_9.setProperty("value", 0)
        self.progressBar_9.setObjectName("progressBar_9")
        self.progressBar_9.setStyleSheet("border:1px solid #e6f5ff;")
        self.spinBox_12 = QtWidgets.QSpinBox(self.Broj)
        self.spinBox_12.setGeometry(QtCore.QRect(520, 100, 81, 31))
        self.spinBox_12.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_12.setObjectName("spinBox_12")
        self.spinBox_12.setStyleSheet("border:1px solid #e6f5ff;")
        self.spinBox_13 = QtWidgets.QSpinBox(self.Broj)
        self.spinBox_13.setGeometry(QtCore.QRect(20, 480, 351, 31))
        self.spinBox_13.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_13.setObjectName("spinBox_13")
        self.spinBox_13.setStyleSheet("border:1px solid #e6f5ff;")
        self.spinBox_13.setMaximum(2147483647)
        self.pushButton_17 = QtWidgets.QPushButton(self.Broj)
        self.pushButton_17.setGeometry(QtCore.QRect(20, 530, 351, 41))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_17.clicked.connect(self.add_number_share)
        self.pushButton_17.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.Broj)
        self.scrollArea_5.setGeometry(QtCore.QRect(740, 20, 361, 261))
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollArea_5.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 359, 259))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.listWidget_6 = QtWidgets.QListWidget(self.scrollAreaWidgetContents_5)
        self.listWidget_6.setObjectName("listWidget_6")
        self.horizontalLayout_6.addWidget(self.listWidget_6)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.scrollArea_11 = QtWidgets.QScrollArea(self.Broj)
        self.scrollArea_11.setGeometry(QtCore.QRect(390, 470, 351, 251))
        self.scrollArea_11.setWidgetResizable(True)
        self.scrollArea_11.setObjectName("scrollArea_11")
        self.scrollArea_11.setStyleSheet("border:1px solid #e6f5ff;")
        self.scrollAreaWidgetContents_11 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_11.setGeometry(QtCore.QRect(0, 0, 349, 249))
        self.scrollAreaWidgetContents_11.setObjectName("scrollAreaWidgetContents_11")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_11)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.listWidget_7 = QtWidgets.QListWidget(self.scrollAreaWidgetContents_11)
        self.listWidget_7.setObjectName("listWidget_7")
        self.horizontalLayout_7.addWidget(self.listWidget_7)
        self.scrollArea_11.setWidget(self.scrollAreaWidgetContents_11)
        self.pushButton_18 = QtWidgets.QPushButton(self.Broj)
        self.pushButton_18.setGeometry(QtCore.QRect(20, 650, 351, 41))
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_18.clicked.connect(self.decrypt_number)
        self.pushButton_18.setStyleSheet("border:1px solid #e6f5ff;")
        self.lcdNumber = QtWidgets.QLCDNumber(self.Broj)
        self.lcdNumber.setGeometry(QtCore.QRect(760, 550, 341, 121))
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.Panel)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(20)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setProperty("value", -1.0)
        self.lcdNumber.setProperty("intValue", -1)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setStyleSheet("border:1px solid #e6f5ff;")
        self.toolBox.addItem(self.Broj, " Број ")
        ShamirSecretSharing.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ShamirSecretSharing)
        self.statusbar.setObjectName("statusbar")
        ShamirSecretSharing.setStatusBar(self.statusbar)

        self.retranslateUi(ShamirSecretSharing)
        QtCore.QMetaObject.connectSlotsByName(ShamirSecretSharing)

    def retranslateUi(self, ShamirSecretSharing):
        _translate = QtCore.QCoreApplication.translate
        ShamirSecretSharing.setWindowTitle(_translate("ShamirSecretSharing", "Шамир Сикрет Шеринг"))
        self.toolBox.setWhatsThis(_translate("ShamirSecretSharing", "<html><head/><body><p><br/></p></body></html>"))
        self.Slika.setWhatsThis(_translate("ShamirSecretSharing", "<html><head/><body><p>Ekripcija i dekripcija slike</p></body></html>"))
        self.pushButton.setText(_translate("ShamirSecretSharing", "Одабери слику"))
        self.pushButton_2.setText(_translate("ShamirSecretSharing", "Енкриптуј"))
        self.label.setText(_translate("ShamirSecretSharing", "Број подјела:"))
        self.label_2.setText(_translate("ShamirSecretSharing", "Потребно дијелова за реконструкцију:"))
        self.label_3.setText(_translate("ShamirSecretSharing", "Дијелови тајне слике"))
        self.label_4.setText(_translate("ShamirSecretSharing", "Локација подјела:"))
        self.label_5.setText(_translate("ShamirSecretSharing", "линк"))
        self.label_5.setStyleSheet("color: #e6f5ff")
        self.pushButton_4.setText(_translate("ShamirSecretSharing", "Декриптуј"))
        self.label_6.setText(_translate("ShamirSecretSharing", "Одабрани дијелови"))
        self.pushButton_3.setText(_translate("ShamirSecretSharing", "Убаци дио"))
        self.label_7.setText(_translate("ShamirSecretSharing", "Резултат декрипције"))
        self.Tekst.setWhatsThis(_translate("ShamirSecretSharing", "<html><head/><body><p>Ekripcija i dekripcija unesenog broja</p></body></html>"))
        self.label_8.setText(_translate("ShamirSecretSharing", "Текст за енкрипцију"))
        self.pushButton_5.setText(_translate("ShamirSecretSharing", "Енкриптуј"))
        self.label_9.setText(_translate("ShamirSecretSharing", "Број подјела:"))
        self.label_10.setText(_translate("ShamirSecretSharing", "Потребно дијелова за реконструкцију:"))
        self.label_11.setText(_translate("ShamirSecretSharing", "Дијелови тајног текста"))
        self.pushButton_6.setText(_translate("ShamirSecretSharing", "Декриптуј"))
        self.label_12.setText(_translate("ShamirSecretSharing", "Текст добијен декрипцијом"))
        self.pushButton_7.setText(_translate("ShamirSecretSharing", "Додај дио"))
        self.Broj.setWhatsThis(_translate("ShamirSecretSharing", "<html><head/><body><p>Ekripcija i dekripcija unesenog teksta</p></body></html>"))
        self.label_13.setText(_translate("ShamirSecretSharing", "Број за енкрипцију"))
        self.pushButton_16.setText(_translate("ShamirSecretSharing", "Енкриптуј"))
        self.label_27.setText(_translate("ShamirSecretSharing", "Потребно дијелова за реконструкцију:"))
        self.label_28.setText(_translate("ShamirSecretSharing", "Број подјела:"))
        self.pushButton_17.setText(_translate("ShamirSecretSharing", "Додај дио"))
        self.pushButton_18.setText(_translate("ShamirSecretSharing", "Декриптуј"))
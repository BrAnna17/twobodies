# -*- coding: utf-8 -*-

import sys
import math

from Mylt import Mayatnick as Ma # из файла Mylt класс Mayatnick, в котором все методы для расчёта положения маятника.
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication,QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont

class AnimationExample(QtWidgets.QWidget) :
 # конструктор. создаем GUI
    def __init__(self, parent):
        super(AnimationExample, self).__init__(parent)
		
        #QtWidgets.QMainWindow.__init__(self)
        self.resize(700, 400)
        self.setWindowTitle("Two-bodies system")
        #Масса грузика на пружине
        self.paramM1 = QtWidgets.QLineEdit("0.5",self)
        self.paramM1.move(45,30)
        self.labelM1 = QtWidgets.QLabel("M1:",self)
        self.labelM1.move(20,30)
        
        #Масса грузика на стержне
        self.paramM2 = QtWidgets.QLineEdit("1",self)
        self.paramM2.move(45,80)
        self.labelM2 = QtWidgets.QLabel("M2:",self)
        self.labelM2.move(20,80)  

        #Жесткость пружинки
        self.paramk = QtWidgets.QLineEdit("20",self)
        self.paramk.move(45,130)
        self.labelk = QtWidgets.QLabel("k:",self)
        self.labelk.move(20,130) 
        
        #Длина стержня
        self.paraml = QtWidgets.QLineEdit("1",self)
        self.paraml.move(45,180)
        self.labell = QtWidgets.QLabel("l:",self)
        self.labell.move(20,180) 

        
        # кнопка start
        self.buttonStart = QtWidgets.QPushButton("Start",self)
        self.buttonStart.move(20,250)
        self.buttonStart.clicked.connect(self.onStart)
        QToolTip.setFont(QFont('SansSerif', 14))#Шрифт для подсказки
        self.buttonStart.setToolTip('Press here to <b>start!</b>')#подсказка


        # кнопка stop
        self.buttonStop = QtWidgets.QPushButton("Stop",self)
        self.buttonStop.move(100,250)
        self.buttonStop.clicked.connect(self.onStop)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.buttonStop.setToolTip('Press here to <b>stop!</b>')


        #кнопка выхода
        self.btnExit=QPushButton('Quit', self)
        self.btnExit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.btnExit.move(20,280)

        #таймер
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10) #это  влияет на скорость
        self.timer.timeout.connect(self.onTimer)
        #self.show()
        
        self.A=Ma() #создаю маятник
        self.x1=0
        self.x2=0
        self.y2=0
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
             event.ignore()

    def paintEvent(self,ev) :
        # рисуем текущее состояние системы.
        qp=QtGui.QPainter()
        qp.begin(self)
        qpp=QtGui.QPainter()
        qpp.begin(self)
        qpp.setPen(QColor(168, 34, 3))
        
                #рисую точки по координатам маятников
        p0=QtCore.QPointF(self.width()/2 , 30)
        p1=QtCore.QPointF(self.width()/2 - self.x1 , 30 )
        p2=QtCore.QPointF(self.width()/2 - self.x2 , 30 + self.y2)
        
        
        #соединяю точки отрезками
        qp.drawLine(p0,p1)
        qpp.drawLine(p1,p2)
        qpp.drawLine(p1,p2)        

        qp.end()
        qpp.end()
        

    def onTimer(self):
        
        x = self.A.rez_x#иск-координата маятника на пружинке
        fi = self.A.rez_fi#угол отклонения математического маятника
        self.x1=100.0*x#перевожу метры в пиксэли
        self.x2=self.x1-100.0*self.A.l*math.sin(fi)#рассчитываю икс-координату математического маятника
        self.y2=100.0*self.A.l*math.cos(fi)#рассчитываю игрэк-координату математического маятника
        self.A.rezult()#рассчитываю положение маятника через время t (см. Mylt.Mayatnick)
        self.A.up_date()#обновляю начальные условия (см. Mylt.Mayatnick)   
        
        # принуждаем окно к перерисовке
        self.update()

    def onStart(self) :

        m1_str = self.paramM1.text() 
        self.m1=0;
        m1=float(str(m1_str))
        self.A.m1=m1
        
        m2_str = self.paramM2.text() 
        self.m2=0;
        m2=float(str(m2_str))
        self.A.m2=m2
        
        k_str = self.paramk.text() 
        self.k=0;
        k=float(str(k_str))
        self.A.k=k
        
        l_str = self.paraml.text() 
        self.l=0;
        l=float(str(l_str))
        self.A.l=l
        
        x = self.A.rez_x#иск-координата маятника на пружинке
        fi = self.A.rez_fi#угол отклонения математического маятника
        self.x1=100.0*x# метры в пиксэли
        self.x2=self.x1-100.0*math.sin(fi)#рассчитываю икс-координату математического маятника
        self.y2=100.0*math.cos(fi)#y координата математического маятника

        self.timer.start() #стартуем

    def onStop(self) :
        self.timer.stop()
        
#if __name__ == '__main__':
app = QtWidgets.QApplication(sys.argv)#объект приложения (экземпляр QApplication). Параметр sys.argv это список аргументов командной строки.
widget = AnimationExample(None)
widget.show()
sys.exit(app.exec_())
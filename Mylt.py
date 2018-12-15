
from math import *
g=9.8
class Mayatnick:
    
    def __init__(self):
        self.k=20#жесткость пружины, Н/м
        self.m1=1#масса грузика на пружыне, кг
        self.m2=1#масса грузика на стержне, кг
        self.l=1#длина стержня, м
        self.fi0=radians(-50)#начальный угол отклонения стержня от вертикали, отчситывается по часовой стрелке
        self.x0=0#начальная икс-координата пружынного маятника
        self.fi0_sh=radians(0)#sh -- это штрих, производная
        self.x0_sh=0#
        self.dt=0.001#время между итерациями
        self.rez_x=self.x0#текущая икс-координата пружынного маятника
        self.rez_fi=self.fi0#текущий угол отклонения стержня
        self.t=0.01#конечное время
        self.alpha1=self.x0_sh#ускорение бруска
        self.beta1=self.fi0_sh#ускорение груза

    def a_sh(self,x,fi,beta): #ускорение бруска
        ch=self.m2*self.l*sin(fi)*beta**2+self.k*x+self.m2*g*sin(fi)*cos(fi)
        zn=self.m2*(cos(fi))**2-self.m1-self.m2
        return ch/zn
        
    def b_sh(self,x,fi,beta):# ускорение груза
        ch=g*sin(fi)+cos(fi)*(self.m2*self.l*beta**2*sin(fi)+self.k*x)/(self.m1+self.m2)
        zn=-1*self.l+self.m2*self.l*(cos(fi))**2/(self.m1+self.m2)
        return ch/zn
        
    def rezult(self):#rk4
        fi=self.fi0
        x=self.x0
        beta=self.fi0_sh
        alpha=self.x0_sh
        
        for i in range(1,ceil(self.t/self.dt),1):#округление до ближ целого числа - ceil
            k1_a=self.a_sh(x,fi,beta)*self.dt
            k1_b=self.b_sh(x,fi,beta)*self.dt
            k1_x=alpha*self.dt
            k1_fi=beta*self.dt
            k2_a=self.a_sh(x+k1_x/2,fi+k1_fi/2,beta+k1_b/2)*self.dt
            k2_b=self.b_sh(x+k1_x/2,fi+k1_fi/2,beta+k1_b/2)*self.dt
            k2_x=(alpha+k1_a/2)*self.dt
            k2_fi=(beta+k1_b/2)*self.dt
            k3_a=self.a_sh(x+k2_x/2,fi+k2_fi/2,beta+k2_b/2)*self.dt
            k3_b=self.b_sh(x+k2_x/2,fi+k2_fi/2,beta+k2_b/2)*self.dt
            k3_x=(alpha+k2_a/2)*self.dt
            k3_fi=(beta+k2_b/2)*self.dt
            k4_a=self.a_sh(x+k3_x/2,fi+k3_fi/2,beta+k3_b/2)*self.dt
            k4_b=self.b_sh(x+k3_x/2,fi+k3_fi/2,beta+k3_b/2)*self.dt
            k4_x=(alpha+k3_a/2)*self.dt
            k4_fi=(beta+k3_b/2)*self.dt
            alpha+=(k1_a+2*k2_a+2*k3_a+k4_a)/6
            beta+=(k1_b+2*k2_b+2*k3_b+k4_b)/6
            x+=(k1_x+2*k2_x+2*k3_x+k4_x)/6
            fi+=(k1_fi+2*k2_fi+2*k3_fi+k4_fi)/6
            
        self.rez_x=x
        self.rez_fi=fi
        self.alpha1=alpha
        self.beta1=beta

    #Здесь замена начальных условий на только что полученные координаты маятника
    def up_date(self):
        self.x0=self.rez_x
        self.fi0=self.rez_fi
        self.fi0_sh=self.beta1
        self.x0_sh=self.alpha1

    
    
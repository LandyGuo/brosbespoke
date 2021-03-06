#coding=utf8
import types
from exception import LengthError,InputTypeError,SizeTypeError,TransitionError
from util import readCoatTable,searchTable,readTrouseTable
'''
sizeList = [
n1,#领围
n2,#胸围
n3,#腰围
n4,#肩宽
n5,#袖长(右)
n6,#袖长(左)
n7,#后衣长
n8,#臀围
n9,#裤腰围
n10,#裤长
n11,#横档
n12,#膝围
n13,#裤口
n14,#后长
n15,#袖笼
n16,#袖根肥
n17,#袖口
n18,#肚围
n19,#马甲前长
A,#身高
B,#体重
]
userChoice=
{
    'm':0,#m取值  0-修身 1-合身 2-宽松
    'i':0,#i取值 0-打领带 1-不打领带
    'j':0,#j取值 0-手表左 1-手表右 2-无手表
    'q':0,#q取值0-长款 1-短款
}

'''




class SizeConverter(object):
    
    fi = set([86,95,99,100,103,104,105,107,108,109,111,112,113,115,116,117,119
              ,120,121,123,124,125,127,128,129,130,131,132,133,135,136,137,140,
              141,145])
    
    delta = set([87,88,89,91,92,93,96,97,101,134,138,139,142,143,144])
    
    chata = set([90,94,98,102,106,110,114,118,122,126])
    
    
    def __init__(self,sizeList=[],userChoice={}):
        
        self.sizeList= [float(_size) for _size in sizeList]
        self.userChoice = userChoice
        self.__inputCheck()
        self.table2 = readCoatTable(r'/home/ENV/ShiXiongDeYiGui/order/SizeConverter/data/coat.txt')
        self.table3 = readTrouseTable(r'/home/ENV/ShiXiongDeYiGui/order/SizeConverter/data/trou.txt')
#         self.table2 = readCoatTable(r'data/coat.txt')
#         self.table3 = readTrouseTable(r'data/trou.txt')
        self.returnDict = {}
        
    def __inputCheck(self):
        #length and type check
        if len(self.sizeList) == 21 or len(self.userChoice)==4:
            if type(self.userChoice) is types.DictType:
                for _size in self.sizeList:
                    if type(_size) is types.IntType or type(_size) is types.FloatType:
                        continue
                    else:
                        raise SizeTypeError
            else:
                raise InputTypeError
        else:
            raise LengthError
                
    def convert(self):
        #上衣
        A,B = self.sizeList[19:]
        alpha = float(B)/((A-100)*0.9)-1
        if  alpha <=0.15:
            beta1 = 9
        else:
            beta1 = 10
        m = self.userChoice.get('m',1)
        if m==0:
            beta = beta1-1
        elif m==1:
            beta = beta1
        elif m==2:
            beta = beta1+1
        C = self.sizeList[6] if self.userChoice['q']==0 else self.sizeList[6]-2
        D = self.sizeList[1]+beta+1.5
        E = self.sizeList[2]+beta+2.5
        F = self.sizeList[3]-0.5
        G1 = self.sizeList[5]
        G2 = self.sizeList[4]
        H = self.sizeList[17]+beta+2 if self.sizeList[17]!=0 else 0 
        K,k1,k2,k4,k5,k6 = self.__calApartial(A,C,D,E,F,G1,G2) if self.sizeList[17]==0 else self.__calApartial(A,C,D,H,F,G1,G2)
        #下衣
        if self.sizeList[8]<=80:
            I = self.sizeList[8]+2
        elif  self.sizeList[8]>80 and self.sizeList[8]<=105:
            I = self.sizeList[8]
        else:
            I = self.sizeList[8]-2
        J = self.sizeList[7]+ beta-3
        L = (self.sizeList[10]+beta+2)/2
        M = (self.sizeList[11]+beta-1)/2
        N = (self.sizeList[12]+beta+8)/2
        O = self.sizeList[9]
        #马甲成衣
        Yita_a = self.sizeList[18]
        Yita_b = self.sizeList[13]
        Yita_c = self.sizeList[1]+beta
        Yita_d = self.sizeList[2]+beta-0.5
        #衬衫
        P1,P2,P4,P,P5,P6= self.__calTrouserAbias(I,J,L,M,N)
        Q = self.sizeList[0]+0.5 if self.userChoice['i']==0 else self.sizeList[0]-1
        R = self.sizeList[6]+3
        S = self.sizeList[1]+beta+2+2
        T = self.sizeList[17]+beta+3 if self.sizeList[17]!=0 else (self.sizeList[2]+beta+3) 
        U = self.sizeList[3]
        V = self.sizeList[4]
        W = self.sizeList[16]+7 if self.userChoice['j']==1 else self.sizeList[16]+6
        X = self.sizeList[16]+7 if self.userChoice['j']==0 else self.sizeList[16]+6
        Y = self.sizeList[15]+beta
        Z = self.sizeList[14]+beta+1
        theta = self.sizeList[7]+beta
        
        print "coat Size:\n"
        print "A:%s B:%s C:%s D:%s E:%s F:%s G1:%s G2:%s H:%s\n" % (A,B,C,D,E,F,G1,G2,H)
        print "coat fixed size:\n"
        print "K:%s K1:%s K2:%s K4:%s K5:%s K6:%s\n"%(K,k1,k2,k4,k5,k6)
        print "trousers Size :\n"
        print "I:%s J:%s L:%s M:%s N:%s O:%s\n"%(I,J,L,M,N,O)
        print "vest Size:\n"
        print "Yita_a:%s Yita_b:%s Yita_c:%s Yita_d:%s"%(Yita_a,Yita_b,Yita_c,Yita_d)
        print "trousers fixed size:\n"
        print "P:%s P1:%s P2:%s P4:%s P5:%s P6:%s\n" %(P,P1,P2,P4,P5,P6)
        print "shit Size:\n"
        print "Q:%s R:%s S:%s T:%s U:%s V:%s W:%s X:%s Y:%s Z:%s theta:%s\n"%(Q,R,S,T,U,V,W,X,Y,Z,theta)
        
        collection = dict([('A',A),('B',B),('C',C),('D',D),('E',E),('F',F),('G1',G1),('G2',G2),('H',H),
         ('I',I),('J',J),('L',L),('M',M),('N',N),('O',O),
         ('Yita_a',Yita_a), ('Yita_b',Yita_b), ('Yita_c',Yita_c), ('Yita_d',Yita_d),
         ('K',K),('K1',k1),('K2',k2),('K4',k4),('k5',k5),('k6',k6),
         ('P',P),('P1',P1),('P2',P2),('P4',P4),('P5',P5),('P6',P6),
         ('Q',Q),('R',R),('S',S),('T',T),('U',U),('V',V),('W',W),('X',X),('Y',Y),('Z',Z,),('theta',theta)
         ])
        #do data re-check before return
#         self.__resultCheck([k1,k2,k4,k5,k6,P1,P2,P4])
        roundresult = {}
        for key,value in collection.iteritems():
                roundresult[key] = round(float(value),1) if type(value) is types.FloatType or \
                 type(value) is types.IntType else value
        return roundresult
    
    def __resultCheck(self,_tocheckList=[]):
        for _checkData in _tocheckList:
            if abs(_checkData)>5:
                raise TransitionError("K1,K2,K4,K5,K6,P1,P2,P4 seems not Normal,\
                please convert it mannuly")  
        
    def __calTrouserAbias(self,I,J,L,M,N):
        print "Int(J)"+str(int(J))
        rows = searchTable(self.table3,2,int(J))
        print "len(rows):"+str(len(rows))
        if len(rows)==1:
            locatedRow = rows[0]
        else:
            row1 = searchTable(self.table3,2,int(J)+1)[0]
            row2 = searchTable(self.table3,2,int(J)-1)[0]
            locatedRow = row1 if abs(row1[1]-I)<abs(row2[1]-I) else row2
        P_,I_,J_,L_ ,M_,N_= locatedRow[:6]
        P1 = I-I_
        P2 = J-J_
        P4 = L-L_
        P = P_
        P5 = M-M_
        P6 = N -N_
        return (P1,P2,P4,P,P5,P6)
        
        
        
    def __calApartial(self,A,C,D,E,F,G1,G2):
        delta = 100000
        rowNumber =  -1
        for num,row in enumerate(self.table2):
            A_ = row[0]
            C_ = row[3]
            G_,D_,E_,F_ = row[4:]
            deltaTmp = abs(D-D_)*0.4+abs(E-E_)*0.3+abs(C-C_)*0.3+abs(F-F_)*0.2+abs((G1+G2)/2 - G_)*0.1+abs(A-A_-5)*0.075
            if deltaTmp<delta:
                delta = deltaTmp
                rowNumber = num
        k_1,k_2,k_3,C_,G_,D_,E_,F_ = self.table2[rowNumber]
        k1 = D-D_
        k2 = E-E_
        k4 = F-F_
        k5 = C-C_
        k6 = (G1+G2)/2 - G_
        K = "-".join([str(k_1)+'-'+k_2,k_3])
        return K,k1,k2,k4,k5,k6
            
if __name__=="__main__":
    sizeList = [
                47.5,#领围
                125,#胸围
                119,#腰围
                48,#肩宽
                63,#袖长(右)
                63,#袖长(左)
                72,#后衣长
                110,#臀围
                122,#裤腰围
                106,#裤长
                76,#横档
                46.5,#膝围
                27,#裤口
                50,#后长
                55,#袖笼
                42,#袖根肥
                21,#袖口
                119,#肚围
                50,#马甲前长
                175,#身高
                115,#体重
                ]
    
    userChoice={
                    'm':1,#m取值  0-修身 1-合身 2-宽松
                    'i':0,#i取值 0-打领带 1-不打领带
                    'j':1,#j取值 0-手表左 1-手表右 2-无手表
                    'q':1,#q取值0-长款 1-短款
                }      
    result = SizeConverter(sizeList,userChoice).convert()    
        

#coding=utf8

def readCoatTable(tableFilePath):
    lst = []
    with open(tableFilePath,'r') as dataSource:
        for row  in dataSource:
            if row.strip()!="":
                type1,type2,type3,C1,G1,D1,E1,F1 = row.split() 
                lst.append((int(type1),type2,type3,float(C1),\
                            float(G1),float(D1),float(E1),float(F1)))
    return lst

def readTrouseTable(tableFilePath):
    lst = []
    with open(tableFilePath,'r') as dataSource:
        for row  in dataSource:
            if row.strip()!="":
                P,I,J,L,M,N,a,b,c,d = row.split() 
                lst.append((int(P),int(I),int(J),float(L),float(M),float(N),\
                            float(a),float(b),float(c),int(d)))
    return lst

def searchTable(table,columnNum,value):
    querrySet = []
    for row in table:
        if row[columnNum]==value:
            querrySet.append(row)
    return querrySet



if __name__=="__main__":
    table = readTrouseTable(r'../trousers.txt')
    result = searchTable(table,2,100)
    print result
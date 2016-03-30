# coding:utf-8
import xlrd
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

def xizhuang(userinfo,users,cycc,oederlist,order_xx):

    rb = xlwt.Workbook()
    rs = rb.add_sheet(u'西装下单表')
    style = xlwt.XFStyle()
    style1 = xlwt.XFStyle()
    style2 = xlwt.XFStyle()
    style3 = xlwt.XFStyle()
    style4 = xlwt.XFStyle()
    style5 = xlwt.XFStyle()
    style6 = xlwt.XFStyle()
    style7 = xlwt.XFStyle()
    style8 = xlwt.XFStyle()
    style9 = xlwt.XFStyle()
    style10 = xlwt.XFStyle()
    style11 = xlwt.XFStyle()
    style12 = xlwt.XFStyle()
    style13 = xlwt.XFStyle()
    style14 = xlwt.XFStyle()
    font = xlwt.Font()
    font1 = xlwt.Font()
    font2 = xlwt.Font() 
    font6 = xlwt.Font() 
    font7 = xlwt.Font()
    font8 = xlwt.Font() 

    font2.height = 500
    font1.height = 440
    font6.height = 240
    font7.height = 240
    font8.height = 180
    font.name = u'微软雅黑'
    font1.name = u'微软雅黑'
    font8.name = u'微软雅黑'
    font1.bold = True
    font2.bold = True
    font7.bold = True
    style.font = font #为样式设置字体
    style1.font = font1 #为样式设置字体
    style2.font = font2  
    style3.font = font
    style4.font = font #为样式设置字体
    style13.font = font
    style8.font = font7
    style5.font = font
    style6.font = font6
    style7.font = font7
    style9.font = font8
    style14.font = font8
    style10.font = font
    style11.font = font
    style12.font = font
    borders=xlwt.Borders()
    borders.left=1
    borders.right=1
    borders.top=1
    borders.bottom=1
    style.borders=borders
    style4.borders=borders
    style13.borders=borders
    style5.borders=borders
    style1.borders=borders
    style2.borders=borders
    style3.borders=borders
    style6.borders=borders
    style7.borders=borders
    style8.borders=borders
    style9.borders=borders
    style14.borders=borders
    style10.borders=borders
    style11.borders=borders
    style12.borders=borders
    #颜色
    pattern = xlwt.Pattern()
    pattern2 = xlwt.Pattern()
    pattern3 = xlwt.Pattern()
    pattern4 = xlwt.Pattern()
    pattern5 = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern3.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern4.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern5.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x29
    pattern2.pattern_fore_colour = 0x0D
    pattern3.pattern_fore_colour = 0x34
    pattern4.pattern_fore_colour = 0x0A
    pattern5.pattern_fore_colour = 0X1E
    style4.pattern = pattern
    style13.pattern = pattern
    style7.pattern = pattern
    style5.pattern = pattern2
    style14.pattern = pattern2
    style9.pattern = pattern3
    style10.pattern = pattern3
    style11.pattern = pattern4
    style12.pattern = pattern5
    alignment = xlwt.Alignment()
    alignment2 = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment2.horz = xlwt.Alignment.HORZ_LEFT
    alignment2.vert = xlwt.Alignment.VERT_JUSTIFIED
    style.alignment=alignment
    style2.alignment=alignment
    style1.alignment=alignment
    style3.alignment=alignment2
    style13.alignment=alignment2
    style4.alignment=alignment
    style5.alignment=alignment
    style6.alignment=alignment
    style7.alignment=alignment
    style8.alignment=alignment
    style9.alignment=alignment2
    style14.alignment=alignment2
    style10.alignment=alignment2
    style11.alignment=alignment
    style12.alignment=alignment

    #rs.row(3).set_style(style2) 
    rs.write_merge(0,1,0,6, u'北大下单表（西装）',style1)
    rs.write(0,7, u'接单时间',style5)
    rs.write_merge(0,0,8,10, order_xx['tmime'],style5)
    rs.write(1,7, u'预计交期',style5)
    rs.write_merge(1,1,8,10, '',style5)
    rs.write(2,7, u'下单人员',style5)
    rs.write_merge(2,2,8,10,oederlist.xdy,style5)
    rs.write(2,0, u'客户',style6)
    rs.write_merge(2,2,1,2,order_xx['user'],style)
    rs.write(2,3,u'电话:',style6)
    rs.write_merge(2,2,4,6, order_xx['phone'],style)
    rs.write(3,0, u'上衣',style8)
    rs.write(3,1,u'成衣',style6)
    rs.write_merge(3,3,2,4,u'设计要求',style6)
    rs.write(3,7, '',style)
    rs.write_merge(3,3,8,9,u'试穿号衣：',style)
    rs.write(3,10,cycc['K'],style)

    rs.write(4,0,u'身高',style)
    rs.write(4,1,cycc['A'],style4)
    rs.write(4,2,u'单排扣' ,style)
    if len(oederlist.kouxing_sy) == 1:
        rs.write(4,3,oederlist.kouxing_sy,style)
        rs.write(9,3,u'圆下摆',style)
    else:
        rs.write(5,3,oederlist.kouxing_sy,style)
        rs.write(9,3,u'直下摆',style)
    rs.write(4,4,'',style)
    rs.write(4,5,'',style)
    rs.write(4,6,'',style)
    rs.write(4,7,u'部位' ,style4)
    rs.write(4,8,u'+/-',style4)
    rs.write(4,9,'',style)
    rs.write(4,10,'',style)
    rs.write(5,0,u'体重',style)
    rs.write(5,1,cycc['B'],style4)
    rs.write(5,2,u'双排扣',style)
    rs.write(5,4,u'',style)
    rs.write(5,5,u'',style)
    rs.write(5,6,u'',style)
    rs.write(5,7,u'胸围',style4)
    if cycc['K1'] > 0:
        rs.write(5,8,'+' + str(cycc['K1']),style4)
    else:
        rs.write(5,8,cycc['K1'],style4)
    rs.write_merge(5,5,9,10,u'工艺：',style10)
    rs.write(6,0,u'后衣长',style)
    rs.write(6,1,cycc['C'],style4)
    rs.write(6,2,u'领型' ,style)
    rs.write(6,3,oederlist.lingxing_sy ,style)
    rs.write(6,4,u'',style)
    rs.write(6,5,u'',style)
    rs.write(6,6,u'',style)
    rs.write(6,7,u'腰围' ,style4)
    if cycc['K2'] > 0:
        rs.write(6,8,'+' + str(cycc['K2']),style4)
    else:
        rs.write(6,8,cycc['K2'],style4)
    rs.write(7,0,u'胸围',style)
    rs.write(7,1,cycc['D'],style4)
    rs.write(7,2,u'领宽',style)
    rs.write(7,3,u'普通',style)
    rs.write(7,4,u'',style)
    rs.write(7,5,u'',style)
    rs.write(7,6,u'',style)
    rs.write(7,7,u'臀围',style4)
    rs.write(7,8,u'',style4)
    rs.write(8,0,u'腰围',style)
    rs.write(8,1,cycc['E'],style4)
    rs.write(8,2,u'开气',style)
    rs.write(8,3,oederlist.kaiqi_sy,style)
    rs.write(8,4,u'',style)
    rs.write(8,5,u'',style)
    rs.write(8,6,u'',style)
    rs.write(8,7,u'肩宽',style4)
    if cycc['K4'] > 0:
        rs.write(8,8,'+' + str(cycc['K4']),style4)
    else:
        rs.write(8,8,cycc['K4'],style4)
    rs.write(9,0,u'肩宽',style)
    rs.write(9,1,cycc['F'],style4)
    rs.write(9,2,u'前下摆',style)
    
    rs.write(9,4,u'',style)
    rs.write(9,5,u'',style)
    rs.write(9,6,u'',style)
    rs.write(9,7,u'总衣长',style4)
    if cycc['k5'] > 0:
        rs.write(9,8,'+' + str(cycc['k5']),style4)
    else:
        rs.write(9,8,cycc['k5'],style4)
    rs.write(10,0,u'袖长 左',style)
    rs.write(10,1,cycc['G1'],style4)
    rs.write(10,2,u'腰兜',style)
    rs.write(10,3,oederlist.yaodou_sy,style)
    rs.write(10,4,u'',style)
    rs.write(10,5,u'',style)
    rs.write(10,6,u'',style)
    rs.write(10,7,u'袖长',style4)
    if cycc['k6'] > 0:
        rs.write(10,8,'+' + str(cycc['k6']),style4)
    else:
        rs.write(10,8,cycc['k6'],style4)
    rs.write(11,0,u'袖长 右',style)
    rs.write(11,1,cycc['G2'],style4)
    rs.write(11,2,u'胸兜',style)
    rs.write(11,3,u'舟型',style)
    rs.write(11,4,u'',style)
    rs.write(11,5,u'',style)
    rs.write(11,6,u'',style)
    rs.write(11,7,u'前衣长',style4)
    rs.write(11,8,u'',style4)
    rs.write(12,0,u'肚围',style)
    if int(cycc['H']) == 0:
        rs.write(12,1,'',style4)
    else:
        rs.write(12,1,cycc['H'],style4)
    rs.write(12,2,u'过面',style)
    rs.write(12,3,u'连耳皮',style)
    rs.write(12,4,u'',style)
    rs.write(12,5,u'',style)
    rs.write(12,6,u'',style)
    rs.write(12,7,u'后衣长',style4)
    rs.write(12,8,u'',style4)
    rs.write_merge(6,11,9,10,','.join(oederlist.product.craft.split('|')),style9)
    rs.write_merge(12,12,9,10,u'备注：',style3)
    rs.write(13,0,u'垫肩 左',style6)
    rs.write(13,1,u'0.4',style7)
    rs.write(13,2,u'内部兜',style)
    rs.write(13,3,oederlist.neibudou_sy,style3)
    rs.write(13,4,u'',style)
    rs.write(13,5,u'',style2)
    rs.write(13,6,u'',style)
    rs.write(13,7,u'溜肩',style4)
    rs.write(13,8,u'',style4)
    rs.write_merge(13,18,9,10,oederlist.beizhu_sy,style3)
    rs.write(14,0,u'垫肩 右',style6)
    rs.write(14,1, u'0.4',style7)
    rs.write(14,2,u'袖扣',style)
    rs.write(14,3,oederlist.xiukou_sy,style3)
    rs.write(14,4,u'',style)
    rs.write(14,5,u'',style2)
    rs.write(14,6,u'',style2)
    rs.write(14,7,u'后溜肩',style4)
    rs.write(14,8,u'',style4)
    rs.write(15,0,'')
    rs.write(15,1,'')
    rs.write(15,2,u'装饰线',style)
    rs.write(15,3,u'AMF',style6)
    rs.write(15,4,u'',style)
    rs.write(15,5,u'',style)
    rs.write(15,6,u'',style)
    rs.write(15,7,u'袖口',style4)
    rs.write(15,8,u'',style4)
    rs.write(16,0,u'',style)
    rs.write(16,1,u'',style)
    rs.write(16,2,u'驳头眼',style)
    rs.write(16,3,u'有',style)
    rs.write(16,4,u'',style)
    rs.write(16,5,u'',style)
    rs.write(16,6,u'',style)
    rs.write(16,7,u'挺胸',style4)
    rs.write(16,8,u'',style4)
    rs.write_merge(17,19,0,0,u'体型修正',style13)
    rs.write(17,1,u'袖山高',style4)
    rs.write(17,2,u'',style4)
    rs.write(17,3,u'',style4)
    rs.write(17,4,u'前胸围',style4)
    rs.write(17,5,u'',style4)
    rs.write(17,6,u'后胸围',style4)
    rs.write(17,7,u'驼背',style4)
    rs.write(17,8,u'',style4)
    rs.write(18,1,u'叠袖',style4)
    rs.write(18,2,u'',style4)
    rs.write(18,3,u'',style4)
    rs.write(18,4,u'前腰围',style4)
    rs.write(18,5,u'',style4)
    rs.write(18,6,u'后腰围',style4)
    rs.write(18,7,u'袖笼深',style4)
    rs.write(18,8,u'',style4)
    rs.write(19,1,u'袖根肥',style4)
    rs.write(19,2,'',style4)
    rs.write(19,3,u'',style4)
    rs.write(19,4,u'肚省',style4)
    rs.write(19,5,u'',style4)
    rs.write(19,6,u'F',style4)
    rs.write(19,7,u'N高',style4)
    rs.write(19,8,u'',style4)
    rs.write_merge(19,19,9,10,u'肩部手针绷白线',style5)
    rs.write(21,0,u'下衣',style8)
    rs.write(21,1,u'成衣',style6)
    rs.write(21,2,u'',style)
    rs.write_merge(21,21,3,6,u'设计要求',style6)
    rs.write(21,7,u'',style)
    rs.write_merge(21,21,8,9,u'试穿号衣:',style6)
    rs.write(21,10,cycc['P'],style)
    rs.write(22,0,u'腰围',style)
    rs.write(22,1,cycc['I'],style4)
    rs.write(22,2,u'裤褶',style)
    rs.write(22,3,oederlist.kuzhe_xk,style)
    rs.write(22,4,u'',style)
    rs.write(22,5,u'',style)
    rs.write(22,6,u'',style)
    rs.write(22,7,u'部位',style4)
    rs.write(22,8,u'+/-',style4)
    rs.write(22,9,u'',style)
    rs.write(22,10,u'',style)
    rs.write(23,0,u'臀围',style)
    rs.write(23,1,cycc['J'],style4)
    rs.write(23,2,u'前兜设计',style)
    rs.write(23,3,u'斜兜',style)
    rs.write(23,4,u'',style)
    rs.write(23,5,u'',style)
    rs.write(23,6,u'',style)
    rs.write(23,7,u'腰围',style4)
    if cycc['P1'] > 0:
        rs.write(23,8,'+' + str(cycc['P1']),style4)
    else:
        rs.write(23,8,cycc['P1'],style4)
    
    rs.write(23,9,u'工艺',style10)
    if oederlist.kujiao_xk == '内折边':
        rs.write(23,10,u'斜切裤脚',style9)
    else:
        rs.write(23,10,u'',style9)
    rs.write(24,0,u'立裆',style)
    rs.write(24,1,'',style4)
    rs.write(24,2,u'后兜',style)
    rs.write(24,3,oederlist.houdou_xk,style)
    rs.write(24,4,u'',style)
    rs.write(24,5,u'',style)
    rs.write(24,6,u'',style)
    rs.write(24,7,u'臀围',style4)
    if cycc['P2'] > 0:
        rs.write(24,8,'+' + str(cycc['P2']),style4)
    elif cycc['P2'] == 0:
        rs.write(24,8, '',style4)
    else:
        rs.write(24,8,cycc['P2'],style4)
    rs.write(25,2,u'串带',style)
    rs.write(25,3,u'6',style)
    rs.write(25,4,u'',style)
    rs.write(25,5,u'',style)
    rs.write(25,6,u'',style)
    rs.write(25,7,u'裤长',style4)
    rs.write(25,8,u'',style4)
    rs.write_merge(24,24,9,10,u'',style3)
    rs.write_merge(25,25,9,10,u'备注：',style3)
    rs.write(26,2,u'裤脚',style)
    rs.write(26,3,oederlist.kujiao_xk,style)
    rs.write(26,4,u'',style)
    rs.write(26,5,u'',style)
    rs.write(26,6,u'',style)
    rs.write(26,7,u'横档',style4)
    if cycc['P4'] > 0:
        rs.write(26,8,'+' + str(cycc['P4']),style4)
    else:
        rs.write(26,8,cycc['P4'],style4)
    
    rs.write(25,0,u'横档',style)
    rs.write(25,1,cycc['L'],style4)
    rs.write(27,2,u'裤钩',style)
    rs.write(27,3,u'普通',style)
    rs.write(27,4,u'',style)
    rs.write(27,5,u'',style)
    rs.write(27,6,u'',style)
    rs.write(27,7,u'中档',style4)
    if cycc['P5'] > 0:
        rs.write(27,8,'+' + str(cycc['P5']),style4)
    else:
        rs.write(27,8,cycc['P5'],style4)
    rs.write(26,0,u'膝围',style)
    rs.write(26,1,cycc['M'],style4)
    rs.write_merge(28,28,2,4,u'',style)
    rs.write_merge(29,29,2,4,u'',style)
    rs.write_merge(30,30,2,4,u'',style)
    rs.write_merge(28,30,5,5,u'体型修正',style13)
    rs.write(28,6,u'',style)
    rs.write(28,7,u'裤口',style4)
    if cycc['P6'] > 0:
        rs.write(28,8,'+' + str(cycc['P6']),style4)
    else:
        rs.write(28,8,cycc['P6'],style4)
    rs.write_merge(26,30,9,10,oederlist.beizhu_xk,style3)
    rs.write(27,0,u'裤口',style)
    rs.write(27,1,cycc['N'],style4)
    rs.write(29,6,u'',style)
    rs.write(29,7,u'立裆',style4)
    rs.write(29,8,u'',style4)
    rs.write(28,0,u'裤长',style)
    rs.write(28,1,cycc['O'],style4)
    rs.write(30,6,u'',style)
    rs.write(30,7,u'前立裆',style4)
    rs.write(30,8,u'',style4)
    rs.write(32,0,u'马甲',style)
    rs.write(32,1,u'成衣',style)

    rs.write_merge(32,36,2,2,u'',style)
    rs.write_merge(32,32,3,6,u'设计要求',style)
    rs.write_merge(32,32,8,9,u'工艺',style5)
    rs.write_merge(33,36,8,9,u'马甲成衣后背面料用西服面料，不用里布。',style14)
    rs.write(33,0,u'前长',style)
    rs.write(33,3,u'领型',style)
    rs.write(33,5,u'',style)
    rs.write(33,6,u'',style)
    #rs.write_merge(32,36,9,9,u'备注',style)
    rs.write(32,10,u'备注',style)
    rs.write_merge(33,36,10,10,oederlist.beizhu,style3)
    #rs.write_merge(32,36,10,10,oederlist.beizhu,style3)
    rs.write(34,0,u'后长',style)
    
    rs.write(34,3,u'前扣',style)
    rs.write(34,7,u'',style)
    rs.write(35,0,u'胸围',style)
    
    rs.write(35,3,u'面兜',style)
    rs.write_merge(35,35,4,5,u'3',style)
    rs.write(35,6,u'',style)
    rs.write(36,0,u'中胴',style)
    
    rs.write(36,3,u'装饰线',style)
    rs.write_merge(36,36,4,5,u'无',style)
    rs.write(36,7,u'',style)
    rs.write(38,0,u'制作要求',style11)
    if oederlist.add_kuzi:
        rs.write_merge(38,38,5,6,u'单加裤子',style12)
    else:
        rs.write_merge(38,38,5,6,u'',style12)
    if oederlist.add_majia:
        rs.write_merge(38,38,3,4,u'单加马甲',style12)
        rs.write(33,4,oederlist.majia_lingxing,style)
        if len(oederlist.majia_kouxing) == 1:
            rs.write_merge(34,34,4,5,u'单排扣：'+oederlist.majia_kouxing,style)
        else:
            rs.write_merge(34,34,4,5,u'双排扣：'+oederlist.majia_kouxing,style)
        if int(cycc['Yita_a']):
            rs.write(33,1,cycc['Yita_a'],style4)
        else:
            rs.write(33,1,'',style4)
        rs.write(34,1,cycc['Yita_b'],style4)
        rs.write(35,1,cycc['Yita_c'],style4)
        rs.write(36,1,cycc['Yita_d'],style4)
    else:
        rs.write_merge(38,38,3,4,u'',style12)
        rs.write(34,5,'',style)
    if oederlist.add_bespoke:
        rs.write_merge(38,38,1,2,u'Bespoke',style12)
    else:
        rs.write_merge(38,38,1,2,u'',style12)
    if oederlist.add_xiuzi:
        rs.write_merge(39,39,1,6,oederlist.xiuzi,style)
    else:
        rs.write_merge(39,39,1,6,'',style)
    rs.write(38,7,u'里布',style5)
    rs.write_merge(38,39,8,8,u'面料',style)
    rs.write_merge(38,39,9,10,oederlist.fabric.name,style)
    rs.write(39,0,u'上衣绣字内容',style3)
    rs.write(39,7,oederlist.libu_sy,style5)
    #rs.write(39,7,u'',style2)
    #rs.write(39,9,u'量体师',style)
    #rs.write(39,10,userinfo.liangtishi,style)
    rs.col(10).width = 4000
    rs.col(9).width = 2800
    rs.col(1).width = 2800
    rs.col(6).width = 1600
    rs.col(0).width = 256 * 8
    rs.col(1).width = 256 * 8
    rs.col(2).width = 256 * 8
    rs.col(3).width = 256 * 8
    rs.col(4).width = 256 * 6
    rs.col(5).width = 256 * 5
    rs.col(6).width = 256 * 7
    rs.col(7).width = 256 * 10
    rs.col(8).width = 256 * 8
    rs.col(9).width = 256 * 6
    rs.col(10).width = 256 * 17
    name = u'西装下单表'
    #name = name.encode('gb2312')
    rb.save('/home/Download/'+ str(oederlist.id) + str(users.nickname) +'-'+ str(users.phonenumber) + '.xls')
    return 'ok'

    
def chenshan(userinfo,users,cycc,oederlist,order_xx):
    rb = xlwt.Workbook()
    style = xlwt.XFStyle()
    style1 = xlwt.XFStyle()
    style2 = xlwt.XFStyle()
    style3 = xlwt.XFStyle()
    style4 = xlwt.XFStyle()

    font = xlwt.Font()
    font1 = xlwt.Font()
    font2 = xlwt.Font() 
    font2.height = 400
    font1.height = 260
    borders=xlwt.Borders()
    borders.left=1
    borders.right=1
    borders.top=1
    borders.bottom=1
    style.borders=borders
    style1.borders=borders
    style3.borders=borders
    style4.borders=borders

    #颜色
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x0D
    style3.pattern = pattern
    alignment = xlwt.Alignment()
    alignment2 = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment2.horz = xlwt.Alignment.HORZ_LEFT
    alignment2.vert = xlwt.Alignment.VERT_JUSTIFIED
    style.alignment=alignment
    style1.alignment=alignment
    style3.alignment=alignment2
    style4.alignment=alignment2

    font.name = u'微软雅黑'
    font1.name = u'微软雅黑'
    font1.bold = True
    font2.bold = True
    style.font = font #为样式设置字体
    style1.font = font1 #为样式设置字体
    style2.font = font2  
    style3.font = font
    style4.font = font
    cs = rb.add_sheet(u'衬衫下单表')
    cs.write_merge(0,1,0,10, u'                            北大下单表 (衬衫)',style2)
    cs.write_merge(2,2,0,1, u'客户名称',style1)
    cs.write_merge(2,2,2,3, u'联系电话',style1)
    cs.write_merge(2,2,4,5, u'电子邮件',style1)
    cs.write_merge(2,2,6,7, u'下单时间',style3)
    cs.write_merge(3,3,6,7, u'预计交期',style3)
    cs.write_merge(3,3,0,1, order_xx['user'],style)
    cs.write_merge(3,3,2,3, order_xx['phone'],style)
    cs.write_merge(3,3,4,5, u'',style)
    cs.write_merge(2,2,8,10, order_xx['tmime'],style3)
    cs.write_merge(3,3,8,10, order_xx['d2'],style3)
    cs.write_merge(4,4,0,1, u'身高：'+str(cycc['A']),style1)
    cs.write_merge(4,4,2,4, u'体重：'+str(cycc['B']),style1)
    cs.write(4,5, u'',style)
    cs.write_merge(4,4,6,7, u'下单人员',style3)
    cs.write_merge(4,4,8,10, oederlist.xdy,style3)
    cs.write_merge(5,5,0,10, u'                                     衬衫成衣尺寸                    单位：CM                                     ',style1)
    cs.write(6,0,u'领围',style1)
    cs.write(6,1,u'衣长',style1)
    cs.write(6,2,u'胸围',style1)
    cs.write(6,3,u'腰围',style1)
    cs.write(6,4,u'肩宽',style1)
    cs.write(6,5,u'袖长',style1)
    cs.write(6,6,u'右袖口',style1)
    cs.write(6,7,u'左袖口',style1)
    cs.write(6,8,u'袖根肥',style1)
    cs.write(6,9,u'袖笼',style1)
    cs.write(6,10,u'臀围',style1)
    cs.write(7,0,cycc['Q'],style)
    cs.write(7,1,cycc['R'],style)
    cs.write(7,2,cycc['S'],style)
    cs.write(7,3,cycc['T'],style)
    cs.write(7,4,cycc['U'],style)
    cs.write(7,5,cycc['V'],style)
    cs.write(7,6,cycc['W'],style)
    cs.write(7,7,cycc['X'],style)
    cs.write(7,8,cycc['Y'],style)
    cs.write(7,9,cycc['Z'],style)
    cs.write(7,10,cycc['theta'],style)
    cs.write_merge(8,9,0,10,u'                                     款式',style2)
    cs.write(10,0,u'领型',style)
    cs.write(10,1,oederlist.lingxing_cs,style)
    cs.write(10,2,u'袖口',style)
    cs.write(10,3,oederlist.xiukou_cs,style)
    cs.write(10,4,u'下摆',style)
    cs.write(10,5,oederlist.xiabai_cs,style)
    cs.write(10,6,u'门襟',style)
    cs.write(10,7,oederlist.menjin_cs,style)
    cs.write(10,8,u'',style)
    cs.write(10,9,u'',style)
    cs.write(10,10,u'',style)
    cs.write(11,0,u'后背',style)
    cs.write(11,1,oederlist.houbei_cs,style)
    cs.write(11,2,u'口袋',style)
    cs.write(11,3,oederlist.koudai_cs,style)
    cs.write(11,4,u'',style)
    cs.write(11,5,u'',style)
    cs.write(11,6,u'',style)
    cs.write(11,7,u'',style)
    cs.write(11,8,u'',style)
    cs.write(11,9,u'',style)
    cs.write(11,10,u'',style)
    cs.write(12,0,u'绣字内容',style)
    cs.write(12,2,u'绣字颜色',style)
    cs.write(12,4,u'绣字字体',style)
    cs.write(12,6,u'部位',style)
    if oederlist.add_xiuzi:
        cs.write(12,1,oederlist.xiuzi,style4)
        cs.write(12,3,u'顺色',style)
        cs.write(12,5,u'',style)  
        cs.write(12,7,u'袖口',style)
    else:
        cs.write(12,1,u'',style)
        cs.write(12,3,u'',style)
        cs.write(12,5,u'',style)  
        cs.write(12,7,u'',style)    
    
    cs.write(12,8,u'',style)
    cs.write(12,9,u'',style)
    cs.write(12,10,u'',style)
    cs.write_merge(13,13,0,3,u'面料信息',style)
    cs.write_merge(13,14,4,5,u'工艺：',style)
    cs.write_merge(13,14,6,9,','.join(oederlist.product.craft.split('|')),style4)
    cs.write(13,10,u'',style)
    cs.write(14,0,oederlist.product.title,style)
    #cs.write(14,1,oederlist.fabric.name,style)
    cs.write_merge(14,14,1,3,oederlist.fabric.name,style)
    cs.write_merge(15,16,4,5,u'备注：',style)
    cs.write_merge(15,16,6,9,u'',style)
    cs.write(15,0,u'',style)
    cs.write(15,1,u'',style)
    cs.write_merge(15,15,2,3,u'',style)
    cs.write(16,0,u'',style)
    cs.write(16,1,u'',style)
    cs.write_merge(16,16,2,3,u'',style)
    cs.write_merge(14,16,10,10,u'不要绣面料信息的标签',style3)
    cs.col(0).width = 256 * 9
    cs.col(1).width = 256 * 12
    cs.col(2).width = 256 * 7
    cs.col(4).width = 256 * 7
    cs.col(6).width = 256 * 8
    cs.col(7).width = 256 * 8
    cs.col(8).width = 256 * 8 
    cs.col(9).width = 256 * 8 
    name = u'衬衫下单表'
    #name = name.encode('gb2312')
    rb.save('/home/Download/'+str(oederlist.id) + str(users.nickname) +'-'+ str(users.phonenumber)+ '.xls')
    
if __name__=="__main__":
    
    bzcc={}
    cycc ={}
    xzks ={}
    cycc = {'A': 175.0, 'K2': -0.5, 'K1': -2.0, 'B': 60.0, 'K4': 0.8, 'G2': 54.5, 'G1': 54.5, 'k6': -1.5, 'k5': -1.5, 'P2': 1.0, 'C': 66.5, 'P1': -4.0, 'E': 82.5, 'D': 92.0, 'P4': -1.4, 'F': 42.0, 'I': 79.0, 'K': '155-80B-6R/40', 'J': 101.0, 'M': 22.0, 'L': 30.5, 'N': 16.5, 'Q': 37.5, 'P': 82.0, 'S': 92.0, 'R': 66.5, 'U': 43.5, 'T': 82.5, 'W': 15.5, 'Y': 29.5, 'X': 15.5, 'Z': 42.0, 'n': 51.0, 'v': 56.0}
    xizhuang(cycc,xzks)
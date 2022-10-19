import threading
import webLogin as WB
import pandas as pd
import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import time
import auto_update_chrome_driver as au

webList = [

{
    'WEB_NAME' : '嘉華',
    'LOGIN' : "//a[@title='會員登入']",
    'USERNAME' : 'username',
    'PASSWORD' : 'password',
    'SUBMIT' : "//a[@id='urlogin_a']",
    'SEARCH_BTN' : "//a[@title='產品查詢']",
    'SEARCH_TEXT_NAME' : "//input[@name='drug']",
    'SEARCH_TEXT_HID' : "//input[@name='hid']",
    'SEARCH_TEXT_INGRE' : "//input[@name='emt_drug']",
    'SEARCH_TEXT_IID' : "//input[@name='itemiid2']",
    'SEARCH_OK' : "//a[@title='查詢']",
    'RESULT_PRODs' : ("class","item"),
    'RESULT_PROD' : ("class","grpt"),
    'RESULT_PRICE' : ("class","sell_price"),
    'RESULT_ID' : ("class","code"),
    'RESULT_INGRE' : ("class","copul"),
    'RESULT_UNIT' : ("class","sell_price"),#只取中文部分即單位
    'RESULT_STATUS' : ("class","status.black")
},

{
    'WEB_NAME' : '法碼希',
    'USERNAME' : 'name',
    'PASSWORD' : 'pw',
    'SUBMIT' : "//input[@id='BTNLOGIN']",
    'VERIFY' : 'RND',
    'VERIFYTAG' : 'div',
    'VERIFYID' : 'F4',
    'SEARCH_BTN' : "//img[@src='images/BTN_04.png']",
    'SEARCH_TEXT' : "//input[@name='search']",
    'SEARCH_OK' : "//input[@type='submit']",
    'RESULT_PRODs' : ("class","news_title","normal_text"),
    'RESULT_PROD' : ("div",3),
    'RESULT_PRICE' : ("div",4),
    'RESULT_ID' : ("div",2),
    'RESULT_INGRE' : ("div",3),
    'RESULT_UNIT' : ("div",4),#只取中文部分即單位
    'RESULT_STATUS' : ("div",4)
},

{
    'WEB_NAME' : '茂源',
    'LOGIN' : "//a[@class='sun-line sign-first']",
    'USERNAME' : 'username',
    'PASSWORD' : 'password',
    'SUBMIT' : "//button[@id='ulogin_submit']",
    'SEARCH_TEXT' : "//input[@name='keyword']",
    'SEARCH_OK' : "//a[@class='search-btn']",
    'RESULT_PRODs' : ("class","mj.items","item"),
    'RESULT_PROD' : ("tag","h3"),
    'RESULT_PRICE' : ("class","price"),
    'RESULT_ID' : ("class","nhi-code.under"),
    'RESULT_INGRE' : ("tag","li"),
    'RESULT_UNIT' : ("class","price"),#只取中文部分即單位
    'RESULT_STATUS' : ("class","stock")
    
},

{
    'WEB_NAME' : '坤億',
    'USERNAME':'ctl00$cphContent$txtAccount',
    'PASSWORD':'ctl00$cphContent$txtPassword',
    'SUBMIT':'//input[@id="cphContent_btnLogin"]',
    'SEARCH_BTN' : "//a[@id='lkbAllCatalog']",
    'SEARCH_TEXT' : "//input[@id='cphContent_ucCT_txtKeyword']",
    'SEARCH_OK' : "//input[@id='cphContent_ucCT_btnSearch']",
    'RESULT_PRODs' : ("id", "cphContent_ucCT_gv"),
    'RESULT_PROD' : ("td", 3),
    'RESULT_PRICE' : ("td", 5),
    'RESULT_ID' : ("td",2),
    'RESULT_INGRE' : "原網站未提供",
    'RESULT_UNIT' : ("td",4),#只取中文部分即單位
    'RESULT_STATUS' : ("td",1)
},

{
    'WEB_NAME' : '采曜',
    'USERNAME':'email',
    'PASSWORD':'password',
    'SUBMIT':'//button[@type="submit"]',
    'SEARCH_TEXT' : "//input[@type='text']",
    'SEARCH_OK' : "//button[@type='submit']",
    'RESULT_PRODs' : ("class", "card.card-bordered.card-stretched-vertical.shadow-none"),
    'RESULT_PROD' : ("class", "text-secondary"),
    'RESULT_PRICE' : ("class","card-text.text-dark"),
    'RESULT_ID' : ("class","card-text.text-dark.mb-0"),
    'RESULT_INGRE' : "原網站未提供",
    'RESULT_UNIT' : ("class","card-text.text-dark"),#只取中文部分即單位
    'RESULT_STATUS' : ("class","badge.bg-warning.rounded-pill")
},

{
    'WEB_NAME' : '兆鴻',  
    'USERNAME':'username',
    'PASSWORD':'password',
    'SUBMIT':'//button[@id="ulogin_submit"]',
    'SEARCH_BTN' : "//a[@href='order.php?act=order']",
    'SEARCH_TEXT' : "//input[@name='keyword']",
    'SEARCH_OK' : "//button[@type='button']",
    'RESULT_PRODs' : ("class","item"),
    'RESULT_PROD' : ("class", "name-ingredient"),
    'RESULT_PRICE' : ("class","orange"),
    'RESULT_ID' : ("class","nhi-code"),
    'RESULT_INGRE' : ("class","ingredient"),
    'RESULT_UNIT' : ("class","price-unit"),#只取中文部分即單位
    'RESULT_STATUS' : ("class","stock")
},

{
    'WEB_NAME' : '彬利',
    'USERNAME':'username',
    'PASSWORD':'password',
    'SUBMIT':'//button[@type="button"]',
    'SEARCH_BTN' : "//a[@data-id='order.php']",
    'SEARCH_TEXT_NAME' : "//input[@name='drug']",
    'SEARCH_TEXT_HID' : "//input[@name='hid']",
    'SEARCH_TEXT_INGRE' : "//input[@name='emt_drug']",
    'SEARCH_TEXT_IID' : "//input[@name='iid']",
    'SEARCH_OK' : "//button[@type='button']",
    'RESULT_PRODs' : ("class","item"),
    'RESULT_PROD' : ("tag","h3"),
    'RESULT_PRICE' : ("class","price.red"),
    'RESULT_ID' : ("class","nhi-code"),
    'RESULT_INGRE' : ("class","name-ingredient"),
    'RESULT_UNIT' : ("class","unit"),#只取中文部分即單位
    'RESULT_STATUS' : ("class","stock")
},

{
    'WEB_NAME' : '藥典',
    'LOGIN' : "//a[@title='會員登入']",
    'USERNAME':'account',
    'PASSWORD':'password',
    'SUBMIT':'//input[@type="SUBMIT"]',
    "VERIFY" : "security_code",
    'SEARCH_BTN' : "//a[@title='商品查詢']",
    'SEARCH_TEXT_NAME' : "//input[@name='get_prod_name']",
    'SEARCH_TEXT_HID' : "//input[@name='get_prod_medicine']",
    'SEARCH_TEXT_INGRE' : "//input[@name='get_prod_content']",
    'SEARCH_TEXT_IID' : "//input[@name='get_prod_barcode']",
    'SEARCH_OK' : "//input[@type='SUBMIT']",
    'RESULT_PRODs' : ("id","FORM1"),
    'RESULT_PROD' : ("td", 2),
    'RESULT_PRICE' : ("td", 3),
    'RESULT_ID' : ("td",1),
    'RESULT_INGRE' : ("td",2),
    'RESULT_UNIT' : ("td",3),#只取中文部分即單位
    'RESULT_STATUS' : ("td",3)
    
},

{
    'WEB_NAME' : '裕利',
    'LOGIN' : "//button[@class='sign-in-button-style']",
    'USERNAME':'username',
    'PASSWORD':'password',
    'SUBMIT':'//input[@id="okta-signin-submit"]',
    'SEARCH_BTN' : "成立訂單",
    'SEARCH_TEXT' : "//input[@class='searchbox']",
    'RESULT_PRODs' : ("class","ant-table-fixed"),
    'RESULT_PROD' : ("td",3),
    'RESULT_PRICE' : ("td",7),
    'RESULT_ID' : ("td",2),
    'RESULT_INGRE' : "原網站未提供",
    'RESULT_UNIT' : ("td",5),#只取中文部分即單位
    'RESULT_STATUS' : "原網站未提供"
}

]

def treeview_sort_column(tv, col, reverse):
    if col == "價格": 
        l = [(float(tv.set(k, col)), k) for k in tv.get_children('')]
        l = sorted(l, key=lambda x:x[0],reverse=reverse)
    else:
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        
    for index, (val, k) in enumerate(l): 
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
    
def treeviewClick(event):
    for item in treeview.selection():
        index=0
        item_text = treeview.item(item, "values")
        web = item_text[0]
        name = item_text[1]
        for i in range(len(webList)):
            if webList[i]['WEB_NAME']==web:
                index=i
        webList[index]["UI"] = True
        webList[index]["DEBUG"] = 1
        show = WB.WEB(webList[index])
        show.web_start(name, "SEARCH_TEXT_HID")
        if webList[index]["WEB_NAME"]!="茂源":
            webList[index]["UI"] = False
        webList[index]["DEBUG"] = 0
  
def enter(event):
    button_event()

def button_event():
    global trHead
    global Mode
    if combobox.get()=="中英品名":
         Mode = "SEARCH_TEXT_NAME"
    elif combobox.get()=="成分":
         Mode = "SEARCH_TEXT_INGRE"
    elif combobox.get()=="健保碼":
         Mode = "SEARCH_TEXT_HID"
    elif combobox.get()=="國際條碼":
         Mode = "SEARCH_TEXT_IID"
    global L
    All = []
    threads = []
    webs = []
    count = 0
    if Input.get() != '':
        iList = treeview.get_children()
        for item in iList:
            treeview.delete(item)
        medID = Input.get()

        for i in range(L):
            if webList[i]["ENABLE"] == 1:
                webs.append(WB.WEB(webList[i]))
                threads.append(threading.Thread(target = webs[count].web_start, args=(medID,Mode,)))
                threads[count].start()
                count += 1
        count = 0
        for i in range(L):
            if webList[i]["ENABLE"] == 1:
                threads[count].join()            
                All += webs[count].get_result()
                count += 1
        try:
            if webList[8]["ENABLE"] == 1:
                enrx = WB.WEB(webList[8])
                enrx.web_start(medID,Mode)
                All += enrx.get_result()
        except:
            pass
        All = sorted(All, key=lambda x:x[2])
        for i in range(len(All)):
            try:
                price = float(All[i][4])
            except:
                price = All[i][4]
            treeview.insert('',i,values=(All[i][0],All[i][1],All[i][2],All[i][3],price,All[i][5],All[i][6]))
        indexs = [i.pop(0) for i in All]
        data = All
        colunms = ("健保碼","品名","成分","價格","單位","庫存","連結")
        Ex = pd.DataFrame(data, columns=colunms, index=indexs)
        Time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        fileName = Time + "_" + medID + "_" + "price.xlsx"
        path = "C:\\Pn300\\price\\temp\\"+fileName
        with pd.ExcelWriter(path) as writer:
            Ex.to_excel(writer, index=True) 

def goUpdate():
    global window
    window.destroy()
    urL='https://chromedriver.storage.googleapis.com/index.html'
    webbrowser.get('windows-default').open_new(urL)
        
    
window = tk.Tk()
Update = au.check_update_chromedriver()
if type(Update) == str:
    window.title('Error')
    window.geometry('340x80')
    Label = tk.Label(window, text = Update)
    Label.grid(rowspan=2,columnspan=2)
    exit_button = tk.Button(window, text="前往下載", command=goUpdate)
    exit_button.grid(rowspan=2,columnspan=2)
else:
    AP_data = pd.read_excel("APU_data.xlsx", sheet_name=0, usecols="A, B, C, D, E, F,G")
    for i in range(len(webList)):
        webList[i]["WEB_NAME"]=AP_data.iat[i, 0]
        webList[i]["URL"]=AP_data.iat[i, 1]
        webList[i]["ID"]=AP_data.iat[i, 2]
        webList[i]["PS"]=str(AP_data.iat[i, 3])
        webList[i]["ENABLE"]=int(AP_data.iat[i, 4])
        webList[i]["DEBUG"]=int(AP_data.iat[i, 5])
        webList[i]["UI"]=bool(AP_data.iat[i, 6])
        
    L = len(webList)-1
    Mode="SEARCH_TEXT_NAME"
    # 要檢查的目錄路徑
    folderpath = "C:\\Pn300"
    
    
    if os.path.isdir(folderpath):
        window.title('藥品比價APP  Beta v1.3.0')
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        window.geometry('{}x{}'.format(w, h-100))
        
        Label = tk.Label(window, text = "           選擇產品類別:")
        Label.grid(row=3, sticky="e")
    
        search_key = ["中英品名","成分","健保碼","國際條碼"]
        combobox = ttk.Combobox(window,values=search_key)
        combobox.grid(row=3, column=1, sticky="w")
        combobox.current(0)
        
        Label = tk.Label(window, text = "           請輸入關鍵字:")
        Label.grid(row=4, sticky="e")
        
        Input = tk.Entry(window, width=23)
        Input.grid(row=4, column=1, sticky="w")
        
        
        
        
        Submit = tk.Button(window, text='開始搜尋', command=button_event)
        Submit.grid(row=4, column=2, sticky="w")
        
        trHead = ("廠商","健保碼","品名","成分","價格","單位","庫存")
        treeview = ttk.Treeview(window,height=25, show="headings",columns=trHead)
        treeview.column("廠商", width=50, anchor='center')
        treeview.column("品名", width=400, anchor='w')
        treeview.column("價格", width=50, anchor='center')
        treeview.heading("廠商", text="廠商")
        treeview.heading("品名", text="品名")
        treeview.heading("價格", text="價格")
        treeview.grid(row=5,columnspan = 3)
    
        
        yscrollbar = ttk.Scrollbar(window, orient=VERTICAL)            # y軸scrollbar物件
        yscrollbar.grid(row=5, column=3,rowspan = 5) 
        yscrollbar.config(command=treeview.yview)   # y軸scrollbar設定
        treeview.configure(yscrollcommand=yscrollbar.set)
        treeview.bind('<Double-1>', treeviewClick)
        window.bind('<Return>', enter)
        for col in trHead:  # 绑定函数，使表头可排序
            treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
    else:
        window.title('Error')
        window.geometry('90x60')
        Label = tk.Label(window, text = "     目錄遺失...")
        Label.grid(rowspan=2,columnspan=2)
        exit_button = tk.Button(window, text="確認", command=window.destroy)
        exit_button.grid(rowspan=2,columnspan=2)
window.mainloop()

import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import ddddocr
class WEB:
    def __init__(self, tags):
        self.medID = None
        self.Mode = None
        self.tags = tags
        self.option = webdriver.ChromeOptions()
        self.args = ["hide_console", ]
        if not(self.tags['UI']):
            self.option.add_argument("headless")
        self.option.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.chrome = webdriver.Chrome('./chromedriver', chrome_options=self.option, service_args=self.args)
        self.chrome.implicitly_wait(30)
        self.resultList = []

    def web_start(self,medID,Mode):
        self.medID = medID
        self.Mode = Mode
        self.chrome.get(self.tags['URL'])
        self.web_login()
        sleep(1)
        try:
            self.web_login()
        except:
            pass
        sleep(3)
        try:
            self.chrome.switch_to.alert.accept()
        except:
            pass
        self.chrome.refresh()
        
        # sleep(5)
        self.resultList = self.web_search()
        
    
    def get_result(self):
        if self.tags["DEBUG"]==0:
            self.chrome.quit()
        return self.resultList

    
    def web_login(self):
        try:
            self.chrome.switch_to.alert.dismiss()    
        except:
            try:
                self.chrome.switch_to.alert.accept()
            except:
                pass
        if ('LOGIN' in self.tags.keys()):
            login = self.chrome.find_element(By.XPATH, self.tags['LOGIN'])
            login.click()
        
        USERNAME = self.chrome.find_element(By.NAME, self.tags['USERNAME'])
        PASSWORD = self.chrome.find_element(By.NAME, self.tags['PASSWORD'])
        SUBMIT = self.chrome.find_element(By.XPATH, self.tags['SUBMIT'])
        #sleep(1)
        
        if ('VERIFY' in self.tags.keys()):
            TEXT =  ""
            VERIFY = self.chrome.find_element(By.ID, self.tags['VERIFY'])
            if self.tags['WEB_NAME'] ==  '藥典':
                TEXT = self.find_verify_code()
            else:
                TEXT = self.chrome.find_element(By.ID, self.tags['VERIFYID']).text
            VERIFY.send_keys(TEXT)
            
        USERNAME.send_keys(str(self.tags['ID']))
        if self.tags['WEB_NAME'] ==  '裕利':
            sleep(1)
        PASSWORD.send_keys(self.tags['PS'])
        if self.tags['WEB_NAME'] ==  '裕利':
            sleep(1)
        SUBMIT.click()
        
    def web_search(self):
        SEARCH_TEXT = None
        if 'SEARCH_BTN' in self.tags:
            if self.tags["WEB_NAME"] == "裕利":
                sleep(1)
                self.chrome.get("https://ezrx.com/shoppingBag")
            else:
                SEARCH_BTN = self.chrome.find_element(By.XPATH, self.tags["SEARCH_BTN"])
                SEARCH_BTN.click()
        sleep(2)
        if 'SEARCH_TEXT' in self.tags:
            if self.tags["WEB_NAME"] == "裕利":
                SEARCH_TEXT = self.chrome.find_element(By.CLASS_NAME, "searchbox")
            else:
                SEARCH_TEXT = self.chrome.find_element(By.XPATH, self.tags["SEARCH_TEXT"])
        else:
            SEARCH_TEXT = self.chrome.find_element(By.XPATH, self.tags[self.Mode])
        SEARCH_TEXT.send_keys(Keys.CONTROL + 'a')
        sleep(0.5)
        SEARCH_TEXT.send_keys(Keys.BACKSPACE)
        sleep(0.5)
        SEARCH_TEXT.send_keys(self.medID)
        if 'SEARCH_OK' in self.tags:
            SEARCH_OK = self.chrome.find_element(By.XPATH, self.tags["SEARCH_OK"])
            SEARCH_OK.click()
        sleep(5)
        medInfo = self.get_prodData()
        if self.tags["DEBUG"]==0:
            self.chrome.close()
        return medInfo
    def find_verify_code(self):
        self.chrome.maximize_window()
        self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        verifyElement = self.chrome.find_element(By.ID, 'CSI')
        verifyElement.screenshot('verifyPic.png')
        
        ocr = ddddocr.DdddOcr()
        with open('verifyPic.png', 'rb') as f:
            img_bytes = f.read()
        code = ocr.classification(img_bytes)
        return code
        
    def get_prodData(self):
        medInfo = []
        itemPrice = 0
        itemID = ""
        itemIngre = ""
        itemStatus = ""
        current_url = self.chrome.current_url
        if self.tags["RESULT_PRODs"][0]=="class" and self.tags["WEB_NAME"]!="裕利":
            itemList = self.chrome.find_elements(By.CLASS_NAME, self.tags["RESULT_PRODs"][1])
            if len(self.tags["RESULT_PRODs"])>2:
                itemList = self.chrome.find_element(By.CLASS_NAME, self.tags["RESULT_PRODs"][1])
                itemList = itemList.find_elements(By.CLASS_NAME, self.tags["RESULT_PRODs"][2])
                if self.tags["WEB_NAME"]=="法碼希":
                    itemList = self.chrome.find_elements(By.CLASS_NAME, self.tags["RESULT_PRODs"][1])[1]
                    itemList = itemList.find_elements(By.CLASS_NAME, self.tags["RESULT_PRODs"][2])
                    del itemList[0]
                    del itemList[0]
                    del itemList[0]
            for item in itemList:
                if type(self.tags["RESULT_PROD"][1])==str:
                    if self.tags["RESULT_PROD"][0]=="class":
                        itemName = item.find_element(By.CLASS_NAME, self.tags["RESULT_PROD"][1])
                    elif self.tags["RESULT_PROD"][0]=="tag":
                        itemName = item.find_element(By.TAG_NAME, self.tags["RESULT_PROD"][1])
                    itemPrice = item.find_element(By.CLASS_NAME, self.tags["RESULT_PRICE"][1])
                    if self.tags["RESULT_ID"][0]=="class":
                        itemID = item.find_element(By.CLASS_NAME, self.tags["RESULT_ID"][1]).text
                    if self.tags["RESULT_INGRE"][0]=="class":
                        try:
                            itemIngre = item.find_element(By.CLASS_NAME, self.tags["RESULT_INGRE"][1]).text
                        except:
                            itemIngre = "原網站未提供"
                        if self.tags["WEB_NAME"]=="彬利":
                            itemIngre = itemIngre.split("\n")[1]
                    elif self.tags["RESULT_INGRE"][0]=="tag":
                        itemIngre = item.find_element(By.TAG_NAME, self.tags["RESULT_INGRE"][1]).text
                    elif self.tags["RESULT_INGRE"]=="原網站未提供":
                        itemIngre = "原網站未提供"
                    if self.tags["RESULT_UNIT"][0]=="class":
                        itemUnit = item.find_element(By.CLASS_NAME, self.tags["RESULT_UNIT"][1]).text
                        itemUnit = re.findall('[\u4e00-\u9fa5]+',itemUnit)#取中文部分
                    if self.tags["RESULT_STATUS"][0]=="class":
                        try:
                            itemStatus = item.find_element(By.CLASS_NAME, self.tags["RESULT_STATUS"][1]).text
                        except:
                            if self.tags["WEB_NAME"]=="采曜":
                                itemStatus = "供貨中"
                            else:
                                itemStatus = "缺貨"
                    
                    try:
                        if self.tags["WEB_NAME"]!="采曜":
                            itemPrice = itemPrice.find_element_by_tag_name("span")
                    except:
                        pass
                else:
                    itemName = item.find_elements(By.TAG_NAME, self.tags["RESULT_PROD"][0])[self.tags["RESULT_PROD"][1]]
                    if type(self.tags["RESULT_PRICE"][1])==int:
                        itemPrice = item.find_elements(By.TAG_NAME, self.tags["RESULT_PRICE"][0])[self.tags["RESULT_PRICE"][1]]
                    else:
                        itemPrice = item.find_element(By.CLASS_NAME, self.tags["RESULT_PRICE"][1])
                    
                    if type(self.tags["RESULT_ID"][1])==int:
                        itemID = item.find_elements(By.TAG_NAME, self.tags["RESULT_ID"][0])[self.tags["RESULT_ID"][1]].text[0:10]
                    elif self.tags["RESULT_ID"][0]=="class":
                        itemID = item.find_element(By.CLASS_NAME, self.tags["RESULT_ID"][1]).text
                        
                    if type(self.tags["RESULT_INGRE"][1])==int:
                        itemIngre = item.find_elements(By.TAG_NAME, self.tags["RESULT_INGRE"][0])[self.tags["RESULT_INGRE"][1]]
                        itemIngre = itemIngre.text.split("\n")[1]
                    elif self.tags["RESULT_INGRE"][0]=="class":
                        itemIngre = item.find_element(By.CLASS_NAME, self.tags["RESULT_INGRE"][1]).text
                    if type(self.tags["RESULT_UNIT"][1])==int:
                        itemUnit = item.find_elements(By.TAG_NAME, self.tags["RESULT_UNIT"][0])[self.tags["RESULT_UNIT"][1]].text
                        itemUnit = re.findall('[\u4e00-\u9fa5]+',itemUnit)#取中文部分
                    elif self.tags["RESULT_UNIT"][0]=="class":
                        itemUnit = item.find_element(By.CLASS_NAME, self.tags["RESULT_UNIT"][1]).text
                        itemUnit = re.findall('[\u4e00-\u9fa5]+',itemUnit)#取中文部分
                    if type(self.tags["RESULT_STATUS"][1])==int:
                        itemStatus = item.find_elements(By.TAG_NAME, self.tags["RESULT_STATUS"][0])[self.tags["RESULT_STATUS"][1]].text
                        if "補貨中" in itemStatus:
                            itemStatus = "缺貨"
                        else:
                            itemStatus = "供貨中"
                    elif self.tags["RESULT_STATUS"][0]=="class":
                        try:
                            itemStatus = item.find_element(By.CLASS_NAME, self.tags["RESULT_STATUS"][1]).text
                        except:
                            itemStatus = "缺貨"
                itemPrice = re.sub(",","",itemPrice.text)
                itemPrice = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemPrice)]
                itemName = itemName.text.split("\n")[0]
                medInfo.append([self.tags["WEB_NAME"],itemID,itemName,itemIngre,float(itemPrice[0]),itemUnit[0],itemStatus,self.tags["URL"]])
            
        elif self.tags["RESULT_PRODs"][0]=="id" or self.tags["WEB_NAME"] == "裕利":
            if self.tags["WEB_NAME"] != "裕利":
                table = self.chrome.find_element(By.ID, self.tags["RESULT_PRODs"][1])
            else:
                table = self.chrome.find_element(By.CLASS_NAME, self.tags["RESULT_PRODs"][1])
            trList = table.find_elements(By.TAG_NAME, "tr")
            del trList[0]
            if trList[len(trList)-2].get_attribute("align")=="center" and self.tags["WEB_NAME"] == "坤億":
                trList.pop()
                trList.pop()
            for item in trList:
                tdList = item.find_elements(By.TAG_NAME, "td")
                if self.tags["RESULT_PROD"][0]=="td":
                    itemName = tdList[self.tags["RESULT_PROD"][1]].text
                    itemName = itemName.split("\n")[0]
                if self.tags["RESULT_PRICE"][0]=="td":    
                    itemPrice = re.sub(",","",tdList[self.tags["RESULT_PRICE"][1]].text)
                    itemPrice = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemPrice)]
                    if len(itemPrice) == 0:
                        itemPrice = []
                        itemPrice.append(-1)
                    else:
                        itemPrice = float(itemPrice[0])
                if self.tags["RESULT_ID"][0]=="td":
                    itemID = tdList[self.tags["RESULT_ID"][1]].text.split("\n")
                    if self.tags["WEB_NAME"] != "裕利":
                        itemID = itemID[1]
                    if self.tags["WEB_NAME"] == "藥典":
                        itemID = tdList[self.tags["RESULT_ID"][1]].text.split("\n")[0]
                if self.tags["RESULT_INGRE"]=="原網站未提供":
                    itemIngre = "原網站未提供"
                else:
                    itemIngre = tdList[self.tags["RESULT_INGRE"][1]].text.split("\n")[1].split(":")[1]
                if self.tags["RESULT_UNIT"][0]=="td":
                    itemUnit = tdList[self.tags["RESULT_UNIT"][1]].text
                    if itemUnit != "EA":
                        if self.tags["WEB_NAME"] == "藥典":
                            itemUnit = tdList[self.tags["RESULT_UNIT"][1]].text.split("\n")[0]
                            itemUnit = itemUnit[len(itemUnit)-1]
                    else:
                        itemUnit = []
                        itemUnit.append(tdList[self.tags["RESULT_UNIT"][1]].text)
                if self.tags["RESULT_STATUS"][0]=="td":
                    if self.tags["WEB_NAME"] == "藥典":
                        itemStatus = tdList[self.tags["RESULT_UNIT"][1]].text.split("\n")[1].split(":")[1]
                    else:
                        itemStatus = tdList[self.tags["RESULT_STATUS"][1]].text
                        if itemStatus=="有":
                            itemStatus = "供貨中"
                        else:
                            itemStatus = "缺貨"
                else:
                    itemStatus = self.tags["RESULT_STATUS"]
                medInfo.append([self.tags["WEB_NAME"],itemID,itemName,itemIngre,itemPrice,itemUnit[0],itemStatus,self.tags["URL"]])
            
        elif self.tags["RESULT_PRODs"][0]=="table":
            table = self.chrome.find_elements(By.TAG_NAME, self.tags["RESULT_PRODs"][0])[self.tags["RESULT_PRODs"][1]]
            trList = table.find_elements(By.TAG_NAME, "tr")
            del trList[0]
            for i in range(0,len(trList),2):
                itemName = trList[i].find_element(By.TAG_NAME, "td")
                itemPrice = trList[i].find_element(By.TAG_NAME, "strong")
                itemPrice = re.sub(",","",itemPrice.text)
                itemPrice = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemPrice)]
                itemName = itemName.text.split("\n")[0]
                medInfo.append([self.tags["WEB_NAME"],itemName,float(itemPrice[0]),current_url,self.tags["URL"]])
                
        elif self.tags["RESULT_PRODs"][0]=="tag":
            itemList = self.chrome.find_elements(By.TAG_NAME, self.tags["RESULT_PRODs"][0])[self.tags["RESULT_PRODs"][1]]
            trList = table.find_elements(By.TAG_NAME, "tr")
            del trList[0]
            for item in itemList:
                itemName = item.find_element(By.CLASS_NAME, "td")
                itemPrice = trList[i].find_element(By.TAG_NAME, "strong")
                itemPrice = re.sub(",","",itemPrice.text)
                itemPrice = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemPrice)]
                itemName = itemName.text.split("\n")[0]
                medInfo.append([self.tags["WEB_NAME"],itemName,float(itemPrice[0]),current_url,self.tags["URL"]])
                
        return medInfo
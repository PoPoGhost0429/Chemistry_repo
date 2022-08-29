import requests,winreg,zipfile,re,os,sysconfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
url='https://chromedriver.storage.googleapis.com/index.html' # chromedriver download link
def get_Chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    return version

def get_latest_version(url):
    '''查询最新的Chromedriver版本'''
    rep = requests.get(url).text
    time_list = []                                          # 用来存放版本时间
    time_version_dict = {}                                  # 用来存放版本与时间对应关系
    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)     # 匹配文件夹（版本号）和时间
    for i in result:
        time = i[-24:-1]                                    # 提取时间
        version = re.compile(r'.*?/').findall(i)[0]         # 提取版本号
        time_version_dict[time] = version                   # 构建时间和版本号的对应关系，形成字典
        time_list.append(time)                              # 形成时间列表
    latest_version = time_version_dict[max(time_list)][:-1] # 用最大（新）时间去字典中获取最新的版本号
    return latest_version
def get_server_chrome_versions():
    '''return all versions list'''
    versionList=[]
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    rep = requests.get(url, headers=headers).text
    print(rep)
    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)
    print(result)
    for i in result:                                 # 提取时间
        version = re.compile(r'.*?/').findall(i)[0]         # 提取版本号
        print(version)
        versionList.append(version[:-1])                  # 将所有版本存入列表
    return versionList



def get_version():
    '''查询系统内的Chromedriver版本'''
    outstd2 = os.popen('chromedriver --version').read()
    return outstd2.split(' ')[1]


def check_update_chromedriver():
    chromeVersion=get_Chrome_version()
    chrome_main_version=int(chromeVersion.split(".")[0]) # chrome主版本号
    driverVersion=get_version()
    driver_main_version=int(driverVersion.split(".")[0]) # chromedriver主版本号
    if driver_main_version!=chrome_main_version:
        return "chromedriver版本与chrome浏览器不兼容，请前往\nhttps://chromedriver.storage.googleapis.com/index.html\n下載{}版號或與之相近的版本".format(chromeVersion)


if __name__=="__main__":
    check_update_chromedriver()
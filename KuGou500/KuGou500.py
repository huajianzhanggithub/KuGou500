import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook

headers={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'+
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'+
    ' Mobile Safari/537.36'
    }

def get_info(url):
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,'lxml')
    ranks=soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num')
    titles=soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')#get('title')
    times=soup.select('span.pc_temp_tips_r > span')
    integration=[]
    for rank,title,time in zip(ranks,titles,times): 
        integration.append([rank.get_text().strip()
                            ,title.get('title').split('-')[0].strip()
                            ,title.get('title').split('-')[1].strip()
                            ,time.get_text().strip()])
    return integration
if __name__=='__main__':
    urls=['https://www.kugou.com/yy/rank/home/{}-8888.html'
          .format(str(i)) for i in range(1,24)]
    wb=Workbook()
    ws=wb.active
    ws.append(['rank','singer','title','time'])
    n=1
    for url in urls:
        integration = get_info(url)
        for integr in integration:
            ws.append(integr)
        print('第{}页已经写完！！！'.format(n))
        n+=1
        time.sleep(2)
    wb.save('KuGou500.xlsx')
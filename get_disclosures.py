from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def fn_test(url):
      
      
      a,b,c,d,e,f  = [],[],[],[],[],[] 
      df = pd.DataFrame() 

      
      html = urlopen(url)
      bsObj = BeautifulSoup(html, "html.parser")    
      tbl3 = bsObj.findAll("table")[3]
      trs = tbl3.findAll("tr")

      for tr in trs:
            lst=[]
            tds = tr.findAll('td') 
            for td in tds:
                  
                  if td.get("class")[1] =="kjTime":a += [td.text ] 
                  if td.get("class")[1] =="kjCode":b += [td.text ] 
                  if td.get("class")[1] =="kjName":c += [td.text ] 
                  if td.get("class")[1] =="kjTitle":d += [td.text ]
                  if td.get("class")[1] =="kjTitle": 
                      e += [td.a.get("href") ] if td.a is not None else [td.a ] 
                  if td.get("class")[1] =="kjXbrl" : 
                      f += [td.a.get("href") ] if td.a  is not None else [td.a ] 

      
      df = pd.DataFrame(
            data={
                'Time': a,
                'Code': b,
                'Company': c,
                'Title': d,
                'PDF_Link': e,
                'XBRL_Link': f
            })        
      return df 


# date = '20250408' 
date =  datetime.today().strftime("%Y%m%d")



url0 = 'https://www.release.tdnet.info/inbs/'
url1 = url0  +  'I_list_{}_{}.html'.format('001',date)


html = urlopen(url1)
bsObj = BeautifulSoup(html, "html.parser")
tbl1 = bsObj.findAll("table")[1]

dv1 = tbl1.findAll("div",{"class":"kaijiSum"})
dv2 = tbl1.findAll("div",{"class":"pager-O"})
dv3 = tbl1.findAll("div",{"class":"pager-M"})

if dv1 ==[]:
   print('No Disclosures')
else:
    print(str(dv1).split('全')[1].split('</')[0])
    lst =[ int(i.string) for i in dv3]
    if lst ==[]:
        df  = fn_test(url1)    
        print(df)
    else:
        
        mxpg= max(lst) 
        print( mxpg ) 

        
        df_all = pd.DataFrame()  # master container

        for i in range(mxpg):
            s = str(i + 1)
            url1 = url0 + 'I_list_{}_{}.html'.format(s.zfill(3), date)
            print(s, url1)

            df_page = fn_test(url1)
            df_all = pd.concat([df_all, df_page], ignore_index=True)  # append each page

        # Final result
        print(df_all)


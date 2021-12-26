import json
from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict
import os
import Classes




def store_dict(dict):
    with open('/content/drive/MyDrive/2140-IR/project/data/'+'dic_course.txt','w') as f:
        jsObj = json.dumps(dict)
        f.write(jsObj)

def one_c_info(url):
  one_course = requests.get(url) # Demo网址
  one_course = one_course.text  # 抓取的数据
  soup_1course = BeautifulSoup(one_course, 'html.parser')
  info=(soup_1course.find_all("div", attrs = {"id": "main"}))
  for i in info:

    txt = i.get_text()
    txt = txt.strip()

    l = txt.split('\n')#[0:-1]
    #print((l))
    for i, j in enumerate(l):
      d = 'Past SectionsPlease click the headings below to view the hidden section'
      if d in j:
        l.pop(i)

    txt = '\n'.join(l)
    
    with open('/content/drive/MyDrive/2140-IR/project/data/'+'course.txt','a+') as f:
      f.write(txt) 
      f.write('\n') 
      f.write(url)
      f.write('\n-------------------\n')  




r_course = requests.get('https://courses.sci.pitt.edu/courses#') # SCI course website
demo_course = r_course.text  # get text

soup_course = BeautifulSoup(demo_course, 'html.parser')  # parse text

def not_lacie(href):
        return href and re.compile("courses/view").search(href)

# return list containing all of course in website
l_course = soup_course.find_all('a',href=not_lacie)

# form a dictionary contain course field, name, link
# dict{field:{name: link}}
d = defaultdict(dict)
for i in l_course:
  field  = i.get_text().split()[0]
  course_id = i.get_text().split()[1]
  d[field][course_id] ='https://courses.sci.pitt.edu/'+i.get('href')

store_dict(d)



os.remove(r'/content/drive/MyDrive/2140-IR/project/data/course.txt')
for i in d:
  print(i)
  for j in d[i].values():
    print(j)
    one_c_info(j)




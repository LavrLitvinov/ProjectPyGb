from os import write
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import os

from requests.models import to_native_string
ext_link = set() # Множество внешних ссылок
int_link = set() # Множество внутренних ссылок
java_link = set() # Множество кривых ссылок на javascript
break_link = set() # Множестов битых ссылок

DOMAIN_NAME = ""



def valid_url(url):
    # проверяем валидность адреса по схеме и домену
   # print("url =  ", url)
    urlss = urlparse(url)
    if(urlss.scheme == 'javascript'): return True
    # Проверили кривую ссылку, но ссылку! на javascript
    if (not(bool(urlss.scheme)) or not(bool(urlss.netloc))): 
        #print(url, " - неправильная или отсутствует схема")
        return False
# Проверили наличие схемы и домена
    try:
        urls = requests.get(url)
    except:
        #print(url, " - Ошибка при вызове")
        return False
# Вроде это даже ссылка, иначе не открылось и выпало исключение
    if urls.status_code != requests.codes.ok : 
        #print(url, " - Плохой ответ сервера")
        return False   
# Оно даже ответило
    return True

# *********************************************************************************************
def website_links(url, ext_link, int_link, java_link, break_link, DOMAIN_NAME ):
    print("Изучаааююю url: ", url)
    urls = set()
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_teg in soup.find_all("a", href = True):  
        href_row = a_teg.attrs.get("href")
        #print("a: ", a_teg)
        
        if href_row in (None, "", "#", "/", " ", "\\", "'"):
            break_link.add("Отсутствует адрес ссылки. визуально на странице: " + a_teg.text)
            continue

        href = urljoin(url, href_row)
        if(not(valid_url(href))):
            break_link.add(href_row + " визуально на странице: " + a_teg.text)
            continue

        #print("href= ", href)
        if(urlparse(href).scheme == 'javascript' ): 
            java_link.add(href+ "  визуально на странице: " + a_teg.text)
            continue 

        if(urlparse(href).netloc != DOMAIN_NAME ): 
            ext_link.add(href+ "  визуально на странице: " + a_teg.text)  
            continue

        urls.add(href)
       
    for j in urls:
        if j in int_link:
            continue

        int_link.add(j)
        website_links(j, ext_link, int_link, java_link, break_link, DOMAIN_NAME )
    return




def print_set(ext_link, int_link, java_link, break_link):
    # Отладочная печать
    l = list(java_link)
    l.sort()
    print("Ссылки на JS: ")
    for j in l:
        print(j)
   
    print("Всего ", len(l), "ед.")
    print()
    print()
    l1 = list(ext_link)
    l1.sort()
    print("Внешние работающие ссылки:")
    for j in l1:
        print(j)
    
    print("Всего ", len(l1), "ед.")
    print()
    print()
    l2 = list(int_link)
    l2.sort()
    print("Рабочие внутренние ссылки:")
    for j in l2:
        print(j)
    
    print("Всего ", len(l2), "ед.")
    print()
    print()
    l3 = list(break_link)
    l3.sort()
    print("Битые ссылки:")
    for j in l3:
        print(j)
  
    print("Всего ", len(l3), "ед.")
    print()
    print()
    print("Итого: уникальных ссылок: ",len(l1)+len(l2)+len(l3)+len(l), " шт." )
    print()
    print()


    
def write_set (ext_link, int_link, java_link, break_link):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_dir, 'link_200.txt')
    file_path1 = os.path.join(current_dir, 'link_300.txt')

    l = list(java_link)
    l.sort()
    l1 = list(ext_link)
    l1.sort()
    l2 = list(int_link)
    l2.sort()
    l3 = list(break_link)
    l3.sort()

    with open(file_path, "w") as out:
        out.write("Рабочие внешние ссылки:" + "\n")
        for j in l1:
            out.write(j + '\n')
        out.write("Рабочие внутренние ссылки:" + "\n")
        for j in l2:
            out.write(j + '\n')
        out.write("Рабочие ссылки JS:" + "\n")
        for j in l:
            out.write(j + '\n')
    with open(file_path1, "w") as gr:
        gr.write("Битые ссылки:" + "\n")
        for j in l3:
            gr.write(j + '\n')
    print()
    print("Путь к файлам с результатами: ", file_path, " и ",file_path1  )
        


 
# *************************************************************************

tr = True

while tr:
    #print("Для демонстрации намертво зашита ссылка http://links.testingcourse.ru/")
    print()
    start_url = input("Введите начальный адрес ( обязательно с HTTP, HTTPS или в том роде):   ") # "http://links.testingcourse.ru/"  
    #"javascript:alert('Hello');" 
    if(urlparse(start_url).scheme == 'javascript'):
        print("Ссылка на javascript!") 
        continue 
    if (valid_url(start_url)):
        print()   
        print("Ok, поехали.")
        #print()
        #print("Работа началась... *****************************************************")
        #print("Продолжается... ********************************************************")
        #print("Ну пчтииии ... *********************************************************")
        tr = False 
    else:
        print("Ссылка ", start_url, " -  сломана и нуждается в замене или ремонте")

DOMAIN_NAME = urlparse(start_url).netloc # Получили доменное имя проверяемого сайта

website_links(start_url, ext_link, int_link, java_link, break_link, DOMAIN_NAME )# спарсили все ссылки начальной страницы в множество urls      
print()
print("Вывод в консоль: ")
print()
print_set(ext_link, int_link, java_link, break_link) # Отладочная печать
write_set (ext_link, int_link, java_link, break_link)
print()
print(" Все!")
print()


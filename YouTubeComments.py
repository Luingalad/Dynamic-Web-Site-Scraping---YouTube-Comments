# -*- coding: utf-8 -*-

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

start_url = "https://www.youtube.com/watch?v=TUo2nPWlV74&list=UUv6jcPwFujuTIwFQ11jt1Yw"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("start-maximized")
iRange = 500

driver = webdriver.Chrome("D:\Python Things\chromedriver.exe", chrome_options = chrome_options)

while True:
    
    driver.get(start_url)
    
    for i in range(5):
        driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
    
    res = driver.execute_script("return document.documentElement.outerHTML")            
    soup = bs(res, 'lxml')
    
    try:
        comment_header = soup.find("yt-formatted-string", {"class": "count-text style-scope ytd-comments-header-renderer"}).text
        comment_count = re.sub("[^0-9]", "", comment_header)
        comment_count_int = float(comment_count)
        iRange = int(comment_count_int/2.5)
    except:
        print("An error")
        continue
    
    driver.find_element_by_css_selector('body').send_keys(Keys.END)
    
    for i in range(iRange):
        driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
    
    
    res = driver.execute_script("return document.documentElement.outerHTML")            
    soup = bs(res, 'lxml')
        
    list_index = soup.find("span", {"class":"index-message style-scope ytd-playlist-panel-renderer"})
    list_index_things = str.split(list_index.text, " ")
    print(list_index.text)

    list_index_things = ["0","0","0"]
        
    next_url = soup.find("a", {"class": "ytp-next-button ytp-button"})
    start_url = next_url["href"]
    
    box = soup.find("ytd-comments", {"id":"comments","class":"style-scope ytd-watch-flexy"})    
    
    comments = box.find_all("yt-formatted-string", {"class":"style-scope ytd-comment-renderer"})
    
    with open("comments.txt", "a+",  encoding = 'utf-8') as f:
        for comment in comments:
             
            if(any(c.isalpha() for c in comment.text)):                
                f.write(comment.text)
                f.write("\n#CommentSep#\n")
                print(comment.text)
            
    
        f.write("\n#VideoSep#\n")
    
    if list_index_things[0] == list_index_things[-1] or list_index_things[0] == "NaN":
        break;
            
print(50*"*" + "\n" + "Comment scraping has finished.\n" + 50*"*" + "\n")
driver.quit()
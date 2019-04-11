import time
import pickle
from selenium import webdriver
import os
import glob
from datetime import datetime
def crawl_page(driver, page):
    driver.get(page)
    SCROLL_PAUSE_TIME = 1.0
    get_height = "return document.body.scrollHeight"
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    last_height = driver.execute_script(get_height)
    while True:
        driver.execute_script(scroll_down)
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script(get_height)
        if new_height == last_height:
            break
        last_height = new_height
    return driver.page_source

def crawl():
    driver = webdriver.Firefox()
    for f in glob.glob('crawl_list/*'):
        f = f.rstrip('/')
        url = open('{}/url.txt'.format(f),'r').read().strip().strip('/')
        subs = open('{}/subs.txt'.format(f), 'r').read().strip().split()
        driver.get(url)
        cookies = pickle.load(open("{}/cookies.pkl".format(f), "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        t = int(datetime.utcnow().timestamp())
        for page in ['{}/{}'.format(url, sub) for sub in subs]:
            folder = page.replace('https://', '')
            html = crawl_page(driver, page)
            os.makedirs('archive/{}'.format(folder), exist_ok=True)
            with open('archive/{}/{}.html'.format(folder, t), 'w') as f:
                f.write(html)
    driver.close()

if __name__ == '__main__':
    crawl()


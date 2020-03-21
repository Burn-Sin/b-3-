import requests,json,queue,os
from bs4 import BeautifulSoup as bs
from multiprocessing import Process

class hb3_spider(object):

    def __init__(self):
        self.page_flag = 1
        self.Q = queue.Queue()

    def get_all_url(self, name, page=1):
        url = 'https://search.bilibili.com/all'
        r = requests.get(url,params={
            'keyword': name,
            'from_source': 'nav_search',
            'spm_id_from': '333.851.b_696e7465726e6174696f6e616c486561646572.10',
            'page': page
        })
        print(page)
        content = r.content.decode(r.encoding)
        soup = bs(content,'lxml')
        v_list = soup.find_all("li",{'class':'video-item matrix'})
        last_page = int(soup.find_all('button',{'class':'pagination-btn'})[-1].string)
        for url_list in v_list:
            for url_link in url_list.find_all('a',{'class':'img-anchor'}):
                av = url_link['href'].replace('?from=search','').replace('//www.bilibili.com/video/av','')
                self.get_cid(av)


        if self.page_flag != last_page:
            self.page_flag+=1
            self.get_all_url(name,self.page_flag)

    def get_cid(self,av):
        url = 'https://api.bilibili.com/x/player/pagelist?aid={}'.format(av)
        r = requests.get(url)
        content = json.loads(r.content.decode(r.encoding))
        for d in content.get('data'):
            self.Q.put(d.get('cid'))

    def get_list(self):
        while True:
            if self.Q.empty() == True:
                break
            Q = self.Q.get()
            url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(Q)
            ##print(Q)
            self.Q.task_done()
            r = requests.get(url)
            r.encoding = 'UTF-8'
            content = r.content.decode(r.encoding)
            b = bs(content, 'xml')
            path = './data'
            for L in b.findChildren('d'):
                if not os.path.exists(path): os.mkdir(path)
                with open(path + '/data.txt', 'a', encoding='utf-8') as f:
                    for i in L:
                        print(i)
                        f.write(str(i) + "\n")

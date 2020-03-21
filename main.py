import spider
from multiprocessing import Process

def run_spider():
    b = spider.hb3_spider()
    p1 = Process(target=b.get_all_url('崩坏3'))
    p1.start()
    p1.join()
    for _ in range(3):
        P2 = Process(target=b.get_list())
        P2.start()

def wold_cloud():pass


if __name__ == '__main__':
    #run_spider()
    pass
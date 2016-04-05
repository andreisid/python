import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'devopsjournal'
HOMEPAGE = 'http://devopsjournal.org/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
Spider.boot()
Spider.crawl_page('First spider', Spider.base_url)

# uncomment to run sequentially:
# while len(file_to_set(QUEUE_FILE)) > 0:
#    queue = file_to_set(QUEUE_FILE)
#    Spider.crawl_page(threading.current_thread().name,queue.pop())

NUMBER_OF_THREADS = 8
queue = Queue()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


#Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()

from link_finder import LinkFinder
from general import *
import requests
from domain import *

class Spider:
    # Class vars
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = project_name + '/queue.txt'
        Spider.crawled_file = project_name + '/crawled.txt'

    # Method to create directory structure and files
    # Also load existing urls
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Crawls a page, adds new links to the queue and removes current url from the queue
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Method returns all links found on the current page
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = requests.get(page_url)
            if 'text/html' in response.headers['Content-Type']:
                html_string = str(response.content)
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(e)
            print('Error: can not crawl page')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        # Add only those urls that are not already in the queue, or have been crawled already or anchor links
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in get_domain_name(url):
                continue
            if '#' in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue,Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

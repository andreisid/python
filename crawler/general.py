import os

# Each website crawled is a separate folder


def create_project_dir(folder):
    if not os.path.exists(folder):
        print("Creating folder " + folder)
        os.makedirs(folder)

# Crate queue and crawled files


def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        print('Creating queue file '+queue)
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        print('Creating crawled file '+crawled)
        write_file(crawled,'')

# Create a new file


def write_file(path, data):
    f=open(path,'w')
    f.write(data)
    f.close()

# Add data to file
def appent_to_file(path,data):
    with open(path,'a') as file:
        file.write(data + '\n')

# Deletes content of a file
def delete_file_contens(path):
    with open(path,'w'):
        pass

# Read a file and convert lines to set elements
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as file:
        for line in file:
            results.add(line.replace('\n',''))
    return results

# Iterate through the set, each item in the set will be a line in a file


def set_to_file(links, file):
    delete_file_contens(file)
    for link in sorted(links):
        appent_to_file(file,link)

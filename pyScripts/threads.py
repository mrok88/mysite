import timeit
from concurrent.futures import ThreadPoolExecutor

urls = ['http://b.ssut.me', 'https://google.com', 'https://apple.com', 'https://ubit.info', 'https://github.com/ssut']

def fetch(url):
    print('Start', url)
    print(url)
    print('Done', url)

#if __name__ == "__main__":    
start = timeit.default_timer()
with ThreadPoolExecutor(max_workers=5) as executor:
    for url in urls:
        executor.submit(fetch, url)

duration = timeit.default_timer() - start
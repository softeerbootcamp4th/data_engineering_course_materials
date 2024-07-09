'''
multiprocessing을 사용하기 위한 프로그래밍 지침
https://docs.python.org/ko/3/library/multiprocessing.html#multiprocessing-programming
'''

from multiprocessing import Process

def print_continent(name='Asia'):
    print("The name of continent is:", name)

if __name__ == '__main__':
    agrs_list = [(), ('America',), ('Europe',), ('Africa',)]
    processes = [Process(target=print_continent, args=args) for args in agrs_list]

    # processes = [
    #     Process(target=print_continent),
    #     Process(target=print_continent, args=('America',)),
    #     Process(target=print_continent, args=('Europe',)),
    #     Process(target=print_continent, args=('Africa',))
    # ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()
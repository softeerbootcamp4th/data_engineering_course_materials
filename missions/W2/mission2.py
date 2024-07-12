from multiprocessing import Process
import time


CONTINENTS = ['Asia', 'America', 'Europe', 'Africa']

def print_continent(arg='Asia'):
    print(f'The name of continent is : {arg}')
    return None

if __name__ == '__main__':
    created_procs = []
    for continent in CONTINENTS:
        p = Process(target=print_continent, args=(continent,))
        p.start()
        created_procs.append(p)
        
    for p in created_procs:
        p.join()  # wait until all child process be done.
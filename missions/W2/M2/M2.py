from multiprocessing import Process

continents = ["America", "Europe",  "Africa"]
def print_continent(continent="Asia"):
    print("The name of continent is : {}".format(continent))

if __name__ == '__main__':
    procs = []
    proc = Process(target=print_continent)
    proc.start()
    for i,continent  in enumerate(continents):
        proc = Process(target=print_continent, args=(continent,))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()


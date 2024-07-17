from multiprocessing import Process


def print_continent(continent: str = "Asia"):
    print(f'The name of continent is {continent}')


if __name__ == '__main__':
    names = ["America", "Europe", "Africa"]
    processes = []
    process = Process(target=print_continent)
    processes.append(process)

    for name in names:
        process = Process(target=print_continent, args=(name,))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

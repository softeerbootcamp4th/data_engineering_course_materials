from multiprocessing import Process

def print_continent(continent: str = "Asia"):
    print(f"The name of continent is : {continent}")

if __name__ == "__main__":
    continent_list = ["Africa", "America", "Europe"]
    processes = [Process(target=print_continent, args=(continent, )) for continent in continent_list]
    # For default argument
    processes.append(Process(target=print_continent))

    for process in processes:
        process.start()

    # ensure processes are finished before the main process ends
    for process in processes:
        process.join()
import multiprocessing

def print_continent(name="Asia"):
    print(f"The name of continent is : {name}")

if __name__ == "__main__":
    p_default = multiprocessing.Process(target=print_continent)
    
    continents = ["America", "Europe", "Africa"]
    processes = [multiprocessing.Process(target=print_continent, args=(continent,)) 
                 for continent in continents]

    p_default.start()
    for p in processes:
        p.start()

    p_default.join()
    for p in processes:
        p.join()
import multiprocessing

# Print Function
def print_continent(name):
    print(f"The name of continent is : {name}")

# Continent dict example
continents = ["Asia", "North America", "Europe", "Africa", "Oceania", "South America"]

if __name__ == "__main__":
    processes = []
    # Process for each continent
    for continent in continents:
        # print(continent)
        process = multiprocessing.Process(target=print_continent, args=(continent,))
        processes.append(process)
        process.start()
    
    # print(processes)

    # Process 끝나는 거 wait
    for process in processes:
        process.join()

from multiprocessing import Process

def print_continent_name(continent="Asia"):
    print(f"The name of continent is : {continent}")

if __name__ == '__main__':
    continents = ["America", "Europe", "Africa"]
    
    processes = []

    # 기본값(Asia)을 사용하는 프로세스 추가
    process_default = Process(target=print_continent_name)
    processes.append(process_default)
    process_default.start()

    for continent in continents:
        process = Process(target=print_continent_name, args=(continent,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()


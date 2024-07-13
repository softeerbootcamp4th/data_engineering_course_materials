# process

import multiprocessing

# 대륙 이름 출력 함수
def print_continent(continent = "Asia"):
    print(f'The name of continent is: {continent}')

if __name__ == "__main__":
    processes = []
    
    processes.append(multiprocessing.Process(target=print_continent))
    processes.append(multiprocessing.Process(target=print_continent, args = ('America',)))
    processes.append(multiprocessing.Process(target=print_continent, args = ('Europe',)))
    processes.append(multiprocessing.Process(target=print_continent, args = ('Africa',)))

    # 프로세스 실행
    for process in processes:
        process.start()

    # processes에 저장된 모든 프로세스가 완료될 때까지 대기
    for process in processes:
        process.join()


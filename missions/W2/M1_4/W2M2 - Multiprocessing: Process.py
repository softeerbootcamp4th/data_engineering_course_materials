import multiprocessing
import time


def print_continent_name(continent="Asia"):
    """
    대륙 이름을 출력하는 함수
    """
    
    print(f"The name of continent is : {continent}")
    time.sleep(1)  # 시뮬레이션을 위해 1초 대기

if __name__ == '__main__':
    '''
    Process 클래스를 통해 프로세스를 생성하여 병럴 작업을 수행할 수 있음
    이 연습에서는 총 4개의 프로세스를 생성함
    4개의 프로세스는 병렬적으로 수행됨
    
    join 메소드를 통해 부모 프로세스에서 자식 프로세스가 종료된 이후 다음 명령을 수행합니다.
    '''
    
    # 다른 대륙 이름들
    continents = ["America", "Europe", "Africa"]
    
    # 기본값을 사용하는 프로세스 생성
    default_process = multiprocessing.Process(target=print_continent_name)
    
    # 다른 대륙 이름을 사용하는 프로세스들 생성
    continent_processes = [multiprocessing.Process(target=print_continent_name, args=(continent,)) for continent in continents]
    
    # 모든 프로세스 시작
    default_process.start()
    for process in continent_processes:
        process.start()
    
    # 모든 프로세스가 종료될 때까지 대기
    default_process.join()
    for process in continent_processes:
        process.join()

    print("All processes have finished execution.")

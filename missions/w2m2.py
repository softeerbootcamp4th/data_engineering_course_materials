from multiprocessing import Process

# 대륙 이름을 출력하는 함수를 정의합니다. 기본값은 "아시아"입니다.
def print_region_name(continent="Asia"):
    print(f"The name of continent is : {continent}")

if __name__ == '__main__':
    # 기본 대륙으로 함수를 실행하는 프로세스를 생성하고 시작합니다.
    p_default = Process(target=print_region_name)
    p_default.start()

    # 다른 대륙 이름으로 함수를 실행하는 프로세스를 생성합니다.
    region = ["America", "Europe", "Africa"]
    processes = [Process(target=print_region_name, args=(continent,)) for continent in region]

    # 모든 프로세스를 시작합니다.
    for p in processes:
        p.start()

    # 기본 프로세스가 종료될 때까지 기다립니다.
    p_default.join()

    # 다른 모든 프로세스가 종료될 때까지 기다립니다.
    for p in processes:
        p.join()

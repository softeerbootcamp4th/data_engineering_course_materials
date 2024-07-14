from multiprocessing import Process


def print_continent(continent: str = "Asia"):
    print(f'The name of continent is : {continent}')


if __name__ == '__main__':
    p_list = [
        Process(target=print_continent, args=("America", )),
        Process(target=print_continent, args=("Europe", )),
        Process(target=print_continent),
        Process(target=print_continent, args=("Africa", )),
    ]

    for p in p_list:
        p.run()
        p.join
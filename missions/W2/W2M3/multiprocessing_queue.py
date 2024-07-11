from multiprocessing import Queue


def main():
    colors = ["red", "green", "blue", "black"]
    cnt = 1
    q = Queue()
    print("pushing items to queue:")
    for color in colors:
        print("item no: ", cnt, color)
        q.put(color)
        cnt += 1

    print("\npopping items from queue:")
    cnt = 0
    while not q.empty():
        print("item no: ", cnt, " ", q.get())
        cnt += 1


if __name__ == "__main__":
    main()

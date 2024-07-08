from multiprocessing import Queue

colors = [
    "red",
    "green",
    "blue",
    "black",
]
if __name__ == '__main__':
    q = Queue()
    qsize=0
    print("pushing items to queue:")
    for i, color in enumerate(colors):
        # print("item no: {} {}".format(q.qsize(), color))
        qsize+=1
        q.put((i,color))
        print("item no: {} {}".format(i+1, color))

    print("popping items from queue:")
    while qsize > 0:
        # print("item no: {} {}".format(q.qsize(), q.get()))
        qsize -= 1
        index, color = q.get()
        print("item no: {} {}".format(index,color))

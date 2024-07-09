from multiprocessing import Process, Queue
 
ITEMS = ['red', 'green', 'blue', 'black']

if __name__=="__main__":
    q = Queue()
    # push
    print('pushing items to queue:')
    for idx, item in enumerate(ITEMS):
        q.put(item)
        print(f'item no: {idx} {item}')

    # pop
    print('popping items from queue:')
    for idx, item in enumerate(ITEMS):
        item = q.get()
        print(f'item no: {idx} {item}')
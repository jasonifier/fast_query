import multiprocessing
import time
import threading

def worker(f, in_q, out_q):
    current_time = time.time()
    while True:
        time.sleep(0.1)
        if time.time() - current_time > 1.2:
            print('In Queue Size:', in_q.qsize())
            print('Out Queue Size:', out_q.qsize())
            current_time = time.time()
        text= in_q.get()
        if text == 'lkjhgfdsa':
            in_q.task_done()
            break
        result = f(text)
        in_q.task_done()
        out_q.put(result)

def write_to_disk(out_q, filename):
    current_time = time.time()
    while True:
        if time.time() - current_time > 0.2:
            if out_q.empty():
                break
            with open(filename, 'a+') as f:
                f.write(out_q.get() + '\n')
            current_time = time.time()

def make_uppercase(input_string):
    return input_string.upper()

in_queue = multiprocessing.JoinableQueue()
out_queue = multiprocessing.Queue()

p = multiprocessing.Process(target=worker, args=(make_uppercase, in_queue, out_queue))
p.start()
t = threading.Thread(target=write_to_disk, args=(out_queue, 'data.txt'))
t.start()

for i in range(100):
    in_queue.put("hello earth")
in_queue.put('lkjhgfdsa')
in_queue.join()

p.join()

outputs = []
while not out_queue.empty():
    result = out_queue.get()
    outputs.append(result)

print('-----------------------')
print('Out Queue Size:', out_queue.qsize())
print(len(outputs))
print(outputs[0])
t.join() 

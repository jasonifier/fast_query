#!/usr/bin/env python3
import multiprocessing
import os
import queue
import threading
import time
import sys

class FastQuery:
    num_procs = multiprocessing.cpu_count()
    thread_pool_size = 10

    def __init__(self, target=None, args=None, num_procs=num_procs, thread_pool_size=thread_pool_size):
        self.target = target
        self.args = args
        self.num_procs = num_procs
        self.thread_pool_size = thread_pool_size

    def create_queues(self, args):
        #  currently args[0] must be a list
        data = args[0]
        self.in_queue = multiprocessing.Queue()
        self.out_queue = multiprocessing.Queue()
        inputs = [self.in_queue.put(rec) for rec in data]
        #  place poison pills into the main multiprocessing FIFO queue
        for _ in range(self.num_procs):
            self.in_queue.put(None)
        
    def create_processes(self):
        self.create_queues(self.args)
        pool = []
        for _ in range(num_procs):
            p = multiprocessing.Process(target=self.worker,
                                        args=(self.in_queue,
                                              self.out_queue),
                                        daemon=False)
            pool.append(p)
            pool[-1].start()

    def worker(self, in_q, out_q):
        print(multiprocessing.current_process().name, "working")
        func = self.target
                
    def thread_worker(self, func, in_q, out_q):
        while True:
            item = in_q.get()
            if item is None:
                in_q.task_done()
                break
            result = func(item)
            out_q.put(result)
            in_q.task_done()

    def execute_threads(self, func):
        q = queue.Queue()
        results_queue = queue.Queue()
        self.populate_thread_queue(q)
        self.poison_thread_queue(q)
        threads = []

        for _ in range(self.thread_pool_size):
            t = threading.Thread(target=self.thread_worker,
                                 args=(func, q, results_queue),
                                 daemon=False)
            threads.append(t)
            t.start()

        q.join()
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        for t in threads:
            t.join()

        return results
 
    def populate_thread_queue(self, q):
        for _ in range(self.thread_pool_size):
            q.put(self.in_queue.get())
   
    def poison_thread_queue(self, q):
        for _ in range(self.thread_pool_size):
            q.put(None)
 
    def show_target(self):
        return self.target

    def show_args(self):
        return self.args

    def get_num_procs(self):
        return self.num_procs

    def get_thread_pool_size(self):
        return self.thread_pool_size
    
    def get_info_dict(self):
       data = {'Target Function': self.show_target(),
               'Arguments': self.show_args(),
               'Number of processes': self.get_num_procs(),
               'Thread Pool Size': self.get_thread_pool_size()}
       return data

    @property
    def info(self):
       data = {k: str(v) for k, v in self.get_info_dict().items()}
       #  Order in which to show the info statement
       fields = ['Target Function', 'Arguments', 'Number of processes', 'Thread Pool Size']
       statement = ''
       for i, f in enumerate(fields, start=1):
           statement += '{0}: {1}'.format(f, data[f])
           if i != len(fields):
               statement += '\n'
       return statement

#  Test the class

if __name__ == '__main__':
    test_obj = FastQuery(target=lambda x: x + 10, args=(1,2,3))
    print(test_obj.info)

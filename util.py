import time
def separator(func):
    def wrapper(*args,**kargs):
        line = ['-']*20
        print('-'.join(line))
        func(*args,**kargs)
        print('-'.join(line))
    return wrapper

def timer(func):
    def wrapper(*args,**kargs):
        start_time = time.time()
        func(*args,**kargs)
        print("----%s----"%(time.time()-start_time))
    return wrapper
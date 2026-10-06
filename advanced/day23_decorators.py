def timer(f):
    def w(*a,**k):
        import time; t=time.time(); r=f(*a,**k); print(time.time()-t); return r
    return w

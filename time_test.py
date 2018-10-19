import timeit

from lazy import APIResponse as LazyResp
from eager import APIResponse as EagerResp


def testLazyIteration():
    resps = [LazyResp.fromKeys('Chinook', 'Album', i) for i in range(1, 10)]
    albsWith10Tracks = []
    for resp in resps:
        if len(resp['Track']) >= 10:
            albsWith10Tracks.append(resp)


def testEagerIteration():
    resps = [EagerResp.fromKeys('Chinook', 'Album', i) for i in range(1, 10)]
    albsWith10Tracks = []
    for resp in resps:
        if len(resp['Track']) >= 10:
            albsWith10Tracks.append(resp)


def createLazy():
    r = LazyResp.fromKeys('Chinook', 'Album', 1)
    r['Track']


def createEager():
    r = EagerResp.fromKeys('Chinook', 'Album', 1)
    r['Track']

if __name__ == '__main__':
    NUM_TRYS = 10

    t = timeit.Timer(testLazyIteration)
    lazyTime = t.timeit(NUM_TRYS)
    print('Time for lazy:  ', lazyTime)
    t = timeit.Timer(testEagerIteration)
    eagerTime = t.timeit(NUM_TRYS)
    print('Time for eager: ', eagerTime)
    print('Lazy was about', round(eagerTime/lazyTime), 'times faster!')

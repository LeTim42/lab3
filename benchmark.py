from time import time


def go(settings, query, conn=None, cur=None, table=None):
    tests = int(settings['tests'])
    queries = settings['queries']
    times = [[0.0] * tests for _ in range(len(queries))]
    for j in range(tests):
        for i in range(len(queries)):
            start = time()
            query(conn, cur, table, settings['dataset'], int(queries[j]))
            finish = time()
            times[i][j] = finish - start
    results = ''
    for i in range(len(queries)):
        list.sort(times[i])
        t = f"{(times[i][tests//2+tests%2-1]+times[i][tests//2])/2:.3f}"
        print(f"Query {queries[i]}: {t} sec")
        results += t + '\t'
    with open('results.txt', 'a') as file:
        file.write(results.replace('.', ',') + '\n')

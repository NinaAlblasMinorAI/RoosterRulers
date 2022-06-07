import numpy as np
from sklearn.cluster import dbscan
from loader import init_students


students = init_students("../data/students.csv")

data = [student._courses for student in students]

def lev_dist(source, target):
    if source == target:
        return 0

    # Prepare matrix
    slen, tlen = len(source), len(target)
    dist = [[0 for i in range(tlen+1)] for x in range(slen+1)]
    for i in range(slen+1):
        dist[i][0] = i
    for j in range(tlen+1):
        dist[0][j] = j

    # Counting distance
    for i in range(slen):
        for j in range(tlen):
            cost = 0 if source[i] == target[j] else 1
            dist[i+1][j+1] = min(
                            dist[i][j+1] + 1,   # deletion
                            dist[i+1][j] + 1,   # insertion
                            dist[i][j] + cost   # substitution
                        )
    return dist[-1][-1]

def lev_metric(x, y):
    i, j = int(x[0]), int(y[0])   
    return lev_dist(data[i], data[j])

X = np.arange(len(data)).reshape(-1, 1)
print(dbscan(X, metric=lev_metric, eps=1, min_samples=2))
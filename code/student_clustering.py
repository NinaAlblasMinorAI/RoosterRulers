import numpy as np
from sklearn.cluster import DBSCAN, dbscan
from loader import init_students


def main():

    # obtain list of all student objects
    students = init_students("../data/students.csv")

    # restructure data to a list of all course lists of students
    data = [student._courses for student in students]

    def lev_metric(x, y):
        """Parses the right data to the lev_dist() function."""

        i, j = int(x[0]), int(y[0])   
        return lev_dist(data[i], data[j])

    # reshape data and perform clustering based on Levenshein method
    X = np.arange(len(data)).reshape(-1, 1)
    clustering = DBSCAN(eps=0.5, min_samples=7, metric=lev_metric).fit(X)

    core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
    core_samples_mask[clustering.core_sample_indices_] = True
    labels = clustering.labels_
    print(labels)

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)


def lev_dist(source, target):
    """Computes the Levenshein distance between two lists of strings"""

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

main()

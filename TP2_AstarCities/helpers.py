def extractPositions(path):
    stream = open(path, "r")
    dictionary = {a[0]: (int(a[1]), int(a[2])) for a in [s.split() for s in stream]}
    return dictionary


def extractConnections(path):
    stream = open(path, "r")
    dictionary = {(a[0], a[1]): int(a[2]) for a in [s.split() for s in stream]}
    return dictionary

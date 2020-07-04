from hashlib import sha256


def G(X):
    X = sha256(X).digest()
    X_L = sha256(X[:16]).digest()
    X_M = sha256(X[8:24]).digest()
    X_R = sha256(X[16:]).digest()
    return X_L+X_M+X_R


def G_L(X):
    prn = G(X=X)
    return prn[:16]


def G_M(X):
    prn = G(X=X)
    return prn[8:24]


def G_R(X):
    prn = G(X=X)
    return prn[16:]

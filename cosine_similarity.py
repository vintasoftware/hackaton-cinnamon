from math import sqrt

def intersect(a, b):
    """Intersection of a and b."""
    return (k for k in a if k in b)

def dot(a, b):
    """Dot product of values in a and b."""
    return sum((a[k] * b[k]) for k in intersect(a, b))

def l2norm(a):
    """L2 norm, aka Euclidean length, of a regarded as a vector."""
    return sqrt(sum(v ** 2 for v in a.values()))

def similarity(a, b):
    """Cosine similarity of a and b."""
    return dot(a, b) / (l2norm(a) * l2norm(b))


def to_dict(issue):
    d = {}
    for tag in issue.tags.all():
        d[tag.name.lower()] = tag.relevance
    return d

def get_key_f(current_issue):
    current_issue_d = to_dict(current_issue)
    def key(issue):
        return similarity(current_issue_d, to_dict(issue))
    return key

# sorted(Issue.objects.all(), key=get_key_f(Issue.objects.first()), reverse=True)

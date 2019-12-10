from magma.passes.tsort import tsort


def test_basic():
    graph = [(2, []),
             (5, [11]),
             (11, [2, 9, 10]),
             (7, [11, 8]),
             (9, []),
             (10, []),
             (8, [9]),
             (3, [10, 8])]
    sorted_ = tsort(graph)

    # Check topo. sorted property of sorted_.
    indices = {k: i for i, (k, _) in enumerate(sorted_)}
    for k, neighbors in sorted_:
        index = indices[k]
        for neighbor in neighbors:
            assert indices[neighbor] < index

    # Explicitly check expectation of sorted list.
    assert sorted_ == [(2, []),
                       (9, []),
                       (10, []),
                       (8, [9]),
                       (3, [10, 8]),
                       (11, [2, 9, 10]),
                       (7, [11, 8]),
                       (5, [11]),]

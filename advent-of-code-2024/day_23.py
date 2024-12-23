from aoc_general import *


def get_input_edges_dict() -> dict[str, list[str]]:
    connections = [ tuple(ln.split("-")) for ln in read_input_day(23).split("\n") ]
    edges_per_node = {}
    for a, b in connections:
        edges_per_node.setdefault(a, []).append(b)
        edges_per_node.setdefault(b, []).append(a)
    return edges_per_node

def solve_part_1():
    edges_per_node = get_input_edges_dict()

    # Get a list of all nodes, sorted by the number of connections
    edges_per_node_list = list((k, v) for k, v in edges_per_node.items())
    edges_per_node_list.sort(key=lambda x: len(x[1]), reverse=True)

    # Iterate nodes, find nodes with a triangle that we didnt see yet
    found_cliques = []
    had_vertices = set()
    for vertex, edges in edges_per_node_list:
        for other_i, other_1 in enumerate(edges[:-1]):
            if other_1 in had_vertices:
                continue
            for other_2 in edges[other_i+1:]:
                if other_2 in had_vertices:
                    continue
                if other_1 in edges_per_node[other_2]:
                    found_cliques.append((vertex, other_1, other_2))
        had_vertices.add(vertex)
    
    # Then only get the ones with a t
    cliques_with_t = [ clique for clique in found_cliques if any(x[0] == "t" for x in clique) ]
    return len(cliques_with_t)

def solve_part_2():

    def bron_kerbosch(R: set[str], P: dict[str, list[str]], X: set) -> list[set[str]]:
        if len(P) == 0 and len(X) == 0:
            return [ R ]
        cliques = []
        for vert in list(P.keys()):
            p_interscet_nv = { k: P[k] for k in list(P.keys()) if k in P[vert] }
            r = bron_kerbosch(R.union(set([vert])), p_interscet_nv, X.intersection(set(P[vert])))
            cliques.extend(r)
            del P[vert]
            X.add(vert)
        return cliques
    
    edges_per_node = get_input_edges_dict()
    cliques = bron_kerbosch(set(), edges_per_node, set())
    biggest_clique = max(cliques, key=lambda x: len(x))
    elems = sorted(list(biggest_clique))
    return ",".join(elems)

    
submit_result_day(23, 1, solve_part_1())

submit_result_day(23, 2, solve_part_2(), allow_non_numeric=True)

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from graph import Graph
from search import bfs, dfs


def make_test_graph():
    """
    A --(100m)-- B --(100m)-- C
    |                         |
  (150m)                   (80m)
    |                         |
    D --(100m)-- E --(100m)-- F
    Speed = 20 m/min on all edges.
    """
    g = Graph()
    g.add_node("A", 0, 1); g.add_node("B", 1, 1); g.add_node("C", 2, 1)
    g.add_node("D", 0, 0); g.add_node("E", 1, 0); g.add_node("F", 2, 0)
    g.add_edge("A", "B", 100, 20)
    g.add_edge("B", "C", 100, 20)
    g.add_edge("A", "D", 150, 20)
    g.add_edge("C", "F", 80, 20)
    g.add_edge("D", "E", 100, 20)
    g.add_edge("E", "F", 100, 20)
    return g


def test_simple_path():
    g = make_test_graph()
    for name, fn in [("BFS", bfs), ("DFS", dfs)]:
        r = fn(g, "A", "C", required_stops=set(), start_time=20.0)
        assert r is not None
        assert r["path"][0] == "A" and r["path"][-1] == "C"
        print(f"  {name} A->C  path={r['path']}  time={r['total_time']:.2f}  expanded={r['nodes_expanded']}")


def test_required_stop():
    g = make_test_graph()
    for name, fn in [("BFS", bfs), ("DFS", dfs)]:
        r = fn(g, "A", "C", required_stops={"D"}, start_time=20.0)
        assert r is not None and "D" in r["path"]
        assert r["path"][0] == "A" and r["path"][-1] == "C"
        print(f"  {name} A->C via D  path={r['path']}  time={r['total_time']:.2f}")


def test_bfs_fewest_hops():
    g = make_test_graph()
    r = bfs(g, "A", "C", required_stops=set(), start_time=20.0)
    assert r is not None and len(r["path"]) == 3
    print(f"  BFS fewest-hops  path={r['path']}")


def test_no_path():
    g = make_test_graph()
    g.add_node("Z", 5, 5)
    for name, fn in [("BFS", bfs), ("DFS", dfs)]:
        assert fn(g, "A", "Z") is None
    print("  No-path test passed")


def test_multiple_required_stops():
    g = make_test_graph()
    for name, fn in [("BFS", bfs), ("DFS", dfs)]:
        r = fn(g, "A", "F", required_stops={"B", "E"}, start_time=20.0)
        assert r is not None
        assert "B" in r["path"] and "E" in r["path"]
        print(f"  {name} A->F via B,E  path={r['path']}  time={r['total_time']:.2f}")


if __name__ == "__main__":
    tests = [
        ("Simple path", test_simple_path),
        ("Required stop", test_required_stop),
        ("BFS fewest hops", test_bfs_fewest_hops),
        ("No path exists", test_no_path),
        ("Multiple required stops", test_multiple_required_stops),
    ]
    passed = 0
    for label, fn in tests:
        print(f"\n[TEST] {label}")
        try:
            fn()
            passed += 1
            print("  PASSED")
        except AssertionError as e:
            print(f"  FAILED: {e}")
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\nResults: {passed}/{len(tests)} tests passed")

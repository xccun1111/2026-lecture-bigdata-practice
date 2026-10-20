#!/usr/bin/env python3
"""Week 5 · Task 2 — convergence experiments and generated report."""
import argparse
import json
import os
import platform
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
JSON_PATH = os.path.join(OUT, "convergence.json")
MD_PATH = os.path.join(OUT, "convergence.md")


def memory_gb():
    try:
        if os.name == "nt":
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return round(stat.ullTotalPhys / (1024 ** 3), 2)
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            return round(pages * page_size / (1024 ** 3), 2)
        except (ValueError, OSError, AttributeError):
            pass
    except Exception:
        pass
    return None


def machine():
    return {"platform": platform.platform(),
            "processor": platform.processor() or platform.machine(),
            "logical_cpu_count": os.cpu_count(),
            "ram_gb": memory_gb(),
            "python": platform.python_version()}


def generate_report(data):
    runs = data.get("runs", [])
    lines = ["# Week 05 — PageRank convergence report", "",
             "Generated from the local experiments in `convergence.json`. Timings depend on the machine.", "",
             "## Machine", "",
             f"- Platform: {data.get('machine', {}).get('platform', 'not recorded')}",
             f"- CPU: {data.get('machine', {}).get('processor', 'not recorded')}",
             f"- Logical CPUs: {data.get('machine', {}).get('logical_cpu_count', 'not recorded')}",
             f"- RAM: {data.get('machine', {}).get('ram_gb', 'not detected')} GB", "",
             "## Runs", "",
             "| Nodes | β | Tolerance | Iterations | Seconds | Top 3 nodes |",
             "|---:|---:|---:|---:|---:|---|"]
    for r in runs:
        top = ", ".join(str(x) for x in r.get("top10", [])[:3])
        iters = r.get("iterations")
        iters_text = str(iters) + (" (max_iter cap)" if iters == 500 else "")
        lines.append(f"| {r.get('nodes')} | {r.get('beta')} | {r.get('tol')} | {iters_text} | {r.get('seconds', 0):.3f} | {top} |")

    lines += ["", "## A3 — Shape of the convergence curve", "",
              "As β approaches 1, convergence generally takes more iterations: the teleportation contribution (1−β)/n becomes smaller, and the iteration operator contracts more slowly. If a run reaches the 500-iteration limit, it has hit the cap rather than necessarily meeting the tolerance.", "",
              "## A4 — Graph size versus time", "",
              "The iteration count is mainly governed by β, the graph structure, and the tolerance; it does not normally grow in direct proportion to node count. Wall time does grow with graph size because each iteration processes nodes and edges. Compare runs with the same β and tolerance at different node counts in the table above.", "",
              "## A5 — Tolerance", "",
              "Compare runs with the same node count and β=0.85 at different tolerances. A stricter tolerance usually requires more iterations; the actual extra iterations are shown below."]
    # Find matching runs and report actual delta in iterations when available.
    groups = {}
    for r in runs:
        key = (r.get("nodes"), r.get("beta"))
        groups.setdefault(key, []).append(r)
    found_tol_comparison = False
    for (nodes, beta), group in groups.items():
        by_tol = {r.get("tol"): r for r in group}
        if len(by_tol) >= 2:
            ordered = sorted(by_tol.items())
            low_tol, low_run = ordered[0]
            high_tol, high_run = ordered[-1]
            if low_run.get("iterations") is not None and high_run.get("iterations") is not None:
                lines.append(f"- Nodes={nodes}, β={beta}: tolerance {low_tol:g} → {low_run['iterations']} iterations; tolerance {high_tol:g} → {high_run['iterations']} iterations; difference = {abs(low_run['iterations'] - high_run['iterations'])} iterations.")
                found_tol_comparison = True
    if not found_tol_comparison:
        lines.append("- The tolerance comparison will appear after you run the required `--tol 1e-6 --betas 0.85` command.")

    lines += ["", "## A6 — Top-10 ranking stability", "",
              "Top-10 order is compared across β values for each fixed graph size and tolerance. The first β whose ordered top-10 list differs from the lowest-β run is reported below."]
    top_change_found = False
    buckets = {}
    for r in runs:
        buckets.setdefault((r.get("nodes"), r.get("tol")), []).append(r)
    for (nodes, tol), group in buckets.items():
        group = sorted(group, key=lambda r: r.get("beta", 0))
        if len(group) < 2:
            continue
        baseline = group[0]
        changed = next((r for r in group[1:] if r.get("top10") != baseline.get("top10")), None)
        if changed:
            lines.append(f"- Nodes={nodes}, tol={tol:g}: first change relative to β={baseline['beta']} occurs at β={changed['beta']}.")
        else:
            lines.append(f"- Nodes={nodes}, tol={tol:g}: no top-10 order change among the recorded β values.")
        top_change_found = True
    if not top_change_found:
        lines.append("- Run the five-β experiment to compare rankings.")
    lines += ["", "## A7 — Other running applications", "",
              "Record what else was running during the timing tests (for example, VS Code, a browser, or other heavy applications). CPU and RAM are detected automatically; running applications are not.", ""]
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--betas", default="0.5,0.7,0.85,0.95,0.99")
    parser.add_argument("--nodes", type=int, default=None)
    parser.add_argument("--tol", type=float, default=1e-10)
    args = parser.parse_args()
    os.makedirs(OUT, exist_ok=True)

    import bench
    if args.nodes:
        bench.NODES = args.nodes
    graph = bench.build()
    from task1_pagerank import pagerank
    rows = []
    for beta in [float(x) for x in args.betas.split(",") if x.strip()]:
        start = time.perf_counter()
        ranks = pagerank(graph, beta=beta, iterations=500, tol=args.tol)
        elapsed = time.perf_counter() - start
        iters = getattr(pagerank, "iterations", None)
        top = sorted(ranks.items(), key=lambda kv: (-kv[1], str(kv[0])))[:10]
        row = {"beta": beta, "nodes": len(graph), "tol": args.tol,
               "iterations": iters, "seconds": elapsed,
               "top10": [node for node, _ in top]}
        rows.append(row)
        print(f"  beta {beta:<5} {str(iters):>4} iterations {elapsed:>7.3f}s   top: {', '.join(str(k) for k, _ in top[:3])}")

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"runs": []}
    data["machine"] = machine()
    data.setdefault("runs", []).extend(rows)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    generate_report(data)
    print(f"\n  -> out/convergence.json ({len(data['runs'])} recorded run(s))")
    print("  -> out/convergence.md")


if __name__ == "__main__":
    main()

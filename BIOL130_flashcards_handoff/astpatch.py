"""Edit card-constructor arguments in the card source files via the Python AST.

op = (func, key_prefix, arg_index, new_value)
  func: combo | match | tf | mc | S
  key: combo/match -> title (arg 1); tf -> claim (arg 2); mc -> stem (arg 1); S -> text (arg 0)
Each key must identify exactly one call. Values: str, bool, list[str], list[tuple[str,str]].
"""
import ast, json

KEY_ARG = {"combo": 1, "match": 1, "tf": 2, "mc": 1, "S": 0}


def lit(v):
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list) and v and isinstance(v[0], tuple):
        return "[" + ",\n   ".join("(" + ", ".join(json.dumps(x, ensure_ascii=False) for x in t) + ")" for t in v) + "]"
    if isinstance(v, list):
        return "[" + ",\n   ".join(json.dumps(x, ensure_ascii=False) for x in v) + "]"
    raise TypeError(type(v))


def patch(fn, ops):
    src = open(fn, encoding="utf-8").read()
    b = src.encode("utf-8")
    line_off = [0]
    for line in b.split(b"\n")[:-1]:
        line_off.append(line_off[-1] + len(line) + 1)
    tree = ast.parse(src)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in KEY_ARG]
    reps = []
    for func, key, idx, val in ops:
        hits = []
        for n in calls:
            if n.func.id != func:
                continue
            k = n.args[KEY_ARG[func]]
            if isinstance(k, ast.Constant) and isinstance(k.value, str) and k.value.startswith(key):
                hits.append(n)
        assert len(hits) == 1, f"{fn}: {func} {key!r} matched {len(hits)}"
        a = hits[0].args[idx]
        start = line_off[a.lineno - 1] + a.col_offset
        end = line_off[a.end_lineno - 1] + a.end_col_offset
        reps.append((start, end, lit(val).encode("utf-8")))
    reps.sort(reverse=True)
    for i in range(len(reps) - 1):
        assert reps[i + 1][1] <= reps[i][0], f"{fn}: overlapping edits"
    for s, e, r in reps:
        b = b[:s] + r + b[e:]
    out = b.decode("utf-8")
    ast.parse(out)
    open(fn, "w", encoding="utf-8").write(out)
    return len(reps)

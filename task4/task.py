import json
import numpy as np

def m(x, pts):
    # значение функции принадлежности в точке x
    pts = sorted(pts, key=lambda p: p[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    if len(pts) < 2:
        return 0.0

    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]

    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            dx = xs[i + 1] - xs[i]
            if dx == 0:
                return (ys[i] + ys[i + 1]) / 2
            return ys[i] + (ys[i + 1] - ys[i]) * (x - xs[i]) / dx

    return 0.0

def fuzzify(x, terms):
    # считаем принадлежность x ко всем terms
    res = {}
    for t in terms:
        res[t["id"]] = m(x, t["points"])
    return res

def ctrl_limits(terms):
    # минимальное и максимальное значение управления
    xs = []
    for t in terms:
        xs.extend(p[0] for p in t["points"])

    if not xs:
        return 0, 26

    return min(xs), max(xs)

def apply_rules(in_mu, rules, out_terms, grid):
    # применяем правила и объединяем результат
    res = np.zeros(len(grid))

    for rule in rules:
        if len(rule) < 2:
            continue

        in_id, out_id = rule
        act = in_mu.get(in_id, 0.0)

        if act == 0:
            continue

        term = None
        for t in out_terms:
            if t["id"] == out_id:
                term = t
                break

        if term is None:
            continue

        mu_vals = np.array([m(x, term["points"]) for x in grid])
        clipped = np.minimum(act, mu_vals)
        res = np.maximum(res, clipped)

    return res

def defuzz_first_max(x_vals, mu_vals):
    # первый максимум (берем середину первого плато)
    if len(mu_vals) == 0:
        return 0.0

    max_mu = np.max(mu_vals)
    if max_mu == 0:
        return x_vals[len(x_vals) // 2]

    for i in range(len(mu_vals)):
        if mu_vals[i] == max_mu:
            start = i
            end = start
            while end + 1 < len(mu_vals) and mu_vals[end + 1] == max_mu:
                end += 1
            return (x_vals[start] + x_vals[end]) / 2

    return x_vals[len(x_vals) // 2]

def calc_control(temp, temp_terms, ctrl_terms, rules, steps=1001):
    # полный цикл нечеткого вывода
    x_min, x_max = ctrl_limits(ctrl_terms)
    grid = np.linspace(x_min, x_max, steps)

    in_mu = fuzzify(temp, temp_terms)
    out_mu = apply_rules(in_mu, rules, ctrl_terms, grid)

    if np.max(out_mu) == 0:
        return 0.0

    return defuzz_first_max(grid, out_mu)

def main(temp_json, control_json, rules_json, current_temp):
    temp_data = json.loads(temp_json)
    ctrl_data = json.loads(control_json)
    rules = json.loads(rules_json)

    temp_terms = temp_data.get("температура", [])
    ctrl_terms = ctrl_data.get("температура", [])

    return calc_control(current_temp, temp_terms, ctrl_terms, rules)

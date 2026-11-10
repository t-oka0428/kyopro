# https://github.com/t-oka0428/kyopro/blob/main/all_ACL_codon.py
# AtCoder Library (ACL) - Complete All-in-One Combined & Converted for Codon

import math
from heapq import heappush, heappop

# ==========================================
# 1. DSU (Disjoint Set Union / Union-Find)
# ==========================================
class DSU:
  def __init__(self, n: int = 0) -> None:
    self._n = n
    self.parent_or_size = [-1] * n

  def merge(self, a: int, b: int) -> int:
    assert 0 <= a < self._n
    assert 0 <= b < self._n
    x = self.leader(a)
    y = self.leader(b)
    if x == y:
      return x
    if -self.parent_or_size[x] < -self.parent_or_size[y]:
      x, y = y, x
    self.parent_or_size[x] += self.parent_or_size[y]
    self.parent_or_size[y] = x
    return x

  def same(self, a: int, b: int) -> bool:
    assert 0 <= a < self._n
    assert 0 <= b < self._n
    return self.leader(a) == self.leader(b)

  def leader(self, a: int) -> int:
    assert 0 <= a < self._n
    parent = self.parent_or_size[a]
    while parent >= 0:
      if self.parent_or_size[parent] < 0:
        return parent
      self.parent_or_size[a], a, parent = (
        self.parent_or_size[parent],
        self.parent_or_size[parent],
        self.parent_or_size[self.parent_or_size[parent]]
      )
    return a

  def size(self, a: int) -> int:
    assert 0 <= a < self._n
    return -self.parent_or_size[self.leader(a)]

  def groups(self):
    leader_buf = [self.leader(i) for i in range(self._n)]
    result = [[] for _ in range(self._n)]
    for i in range(self._n):
      result[leader_buf[i]].append(i)
    return list(filter(lambda r: r, result))


# ==========================================
# 2. FenwickTree (Binary Indexed Tree)
# ==========================================
class FenwickTree:
  def __init__(self, n: int = 0):
    self._n = n
    self.data = [0] * n

  def add(self, p: int, x: int) -> None:
    p += 1
    while p <= self._n:
      self.data[p - 1] += x
      p += p & -p

  def sum(self, left: int, right: int) -> int:
    return self._sum(right) - self._sum(left)

  def _sum(self, r: int) -> int:
    s = 0
    while r > 0:
      s += self.data[r - 1]
      r -= r & -r
    return s


# ==========================================
# 3. SegTree (Segment Tree)
# ==========================================
class SegTree:
  def __init__(self, op, e, v):
    self._op = op
    self._e = e
    if isinstance(v, int):
      self._n = v
      self._size = 1
      while self._size < self._n:
        self._size *= 2
      self._log = (self._size).bit_length() - 1
      self.d = [self._e()] * (2 * self._size)
      for i in range(self._size):
        self.d[self._size + i] = self._e()
    else:
      self._n = len(v)
      self._size = 1
      while self._size < self._n:
        self._size *= 2
      self._log = (self._size).bit_length() - 1
      self.d = [self._e()] * (2 * self._size)
      for i in range(self._n):
        self.d[self._size + i] = v[i]
      for i in range(self._size - 1, 0, -1):
        self._update(i)

  def set(self, p: int, x) -> None:
    p += self._size
    self.d[p] = x
    for i in range(1, self._log + 1):
      self._update(p >> i)

  def get(self, p: int):
    return self.d[p + self._size]

  def prod(self, l: int, r: int):
    if l == r:
      return self._e()
    l += self._size
    r += self._size
    sml = self._e()
    smr = self._e()
    while l < r:
      if l & 1:
        sml = self._op(sml, self.d[l])
        l += 1
      if r & 1:
        r -= 1
        smr = self._op(self.d[r], smr)
      l >>= 1
      r >>= 1
    return self._op(sml, smr)

  def all_prod(self):
    return self.d[1]

  def _update(self, k: int) -> None:
    self.d[k] = self._op(self.d[2 * k], self.d[2 * k + 1])


# ==========================================
# 4. LazySegTree (Lazy Segment Tree)
# ==========================================
class LazySegTree:
  def __init__(self, op, e, mapping, composition, id_, v):
    self._op = op
    self._e = e
    self._mapping = mapping
    self._composition = composition
    self._id = id_

    if isinstance(v, int):
      self._n = v
      self._size = 1
      while self._size < self._n:
        self._size *= 2
      self._log = (self._size).bit_length() - 1
      self.d = [self._e()] * (2 * self._size)
      for i in range(self._size):
        self.d[self._size + i] = self._e()
    else:
      self._n = len(v)
      self._size = 1
      while self._size < self._n:
        self._size *= 2
      self._log = (self._size).bit_length() - 1
      self.d = [self._e()] * (2 * self._size)
      for i in range(self._n):
        self.d[self._size + i] = v[i]
      for i in range(self._size - 1, 0, -1):
        self._update(i)

    self.lz = [self._id] * self._size

  def set(self, p: int, x) -> None:
    p += self._size
    for i in range(self._log, 0, -1):
      self._push(p >> i)
    self.d[p] = x
    for i in range(1, self._log + 1):
      self._update(p >> i)

  def get(self, p: int):
    p += self._size
    for i in range(self._log, 0, -1):
      self._push(p >> i)
    return self.d[p]

  def prod(self, l: int, r: int):
    if l == r:
      return self._e()

    l += self._size
    r += self._size

    for i in range(self._log, 0, -1):
      if ((l >> i) << i) != l:
        self._push(l >> i)
      if ((r >> i) << i) != r:
        self._push((r - 1) >> i)

    sml = self._e()
    smr = self._e()

    while l < r:
      if l & 1:
        sml = self._op(sml, self.d[l])
        l += 1
      if r & 1:
        r -= 1
        smr = self._op(self.d[r], smr)
      l >>= 1
      r >>= 1

    return self._op(sml, smr)

  def all_prod(self):
    return self.d[1]

  def apply(self, l: int, r, f=None):
    if f is None:
      p = l
      p += self._size
      for i in range(self._log, 0, -1):
        self._push(p >> i)
      self.d[p] = self._mapping(f, self.d[p])
      for i in range(1, self._log + 1):
        self._update(p >> i)
      return

    if l == r:
      return

    l += self._size
    r += self._size

    for i in range(self._log, 0, -1):
      if ((l >> i) << i) != l:
        self._push(l >> i)
      if ((r >> i) << i) != r:
        self._push((r - 1) >> i)

    l2 = l
    r2 = r
    while l < r:
      if l & 1:
        self._all_apply(l, f)
        l += 1
      if r & 1:
        r -= 1
        self._all_apply(r, f)
      l >>= 1
      r >>= 1

    l = l2
    r = r2
    for i in range(1, self._log + 1):
      if ((l >> i) << i) != l:
        self._update(l >> i)
      if ((r >> i) << i) != r:
        self._update((r - 1) >> i)

  def _update(self, k: int) -> None:
    self.d[k] = self._op(self.d[2 * k], self.d[2 * k + 1])

  def _all_apply(self, k: int, f) -> None:
    self.d[k] = self._mapping(f, self.d[k])
    if k < self._size:
      self.lz[k] = self._composition(f, self.lz[k])

  def _push(self, k: int) -> None:
    self._all_apply(2 * k, self.lz[k])
    self._all_apply(2 * k + 1, self.lz[k])


# ==========================================
# 5. SCC (Strongly Connected Components)
# ==========================================
class SCCGraph:
  def __init__(self, n: int) -> None:
    self._n = n
    self._edges = []

  def add_edge(self, from_el: int, to_el: int) -> None:
    assert 0 <= from_el < self._n
    assert 0 <= to_el < self._n
    self._edges.append((from_el, to_el))

  def scc(self):
    g_from = [0] * (self._n + 1)
    for u, v in self._edges:
      g_from[u + 1] += 1
    for i in range(self._n):
      g_from[i + 1] += g_from[i]
    g_buf = [0] * len(self._edges)
    cursor = g_from[:]
    for u, v in self._edges:
      g_buf[cursor[u]] = v
      cursor[u] += 1

    qid = [0] * self._n
    inc = [True] * self._n
    st = []
    path = []
    order = 0
    n = self._n

    low = [0] * n
    ord_ = [-1] * n

    def dfs(vertex):
      nonlocal order
      ord_[vertex] = order
      low[vertex] = order
      order += 1
      path.append(vertex)
      st.append(vertex)
      for i in range(g_from[vertex], g_from[vertex + 1]):
        to = g_buf[i]
        if ord_[to] == -1:
          dfs(to)
          low[vertex] = min(low[vertex], low[to])
        elif inc[to]:
          low[vertex] = min(low[vertex], ord_[to])
      if low[vertex] == ord_[vertex]:
        while True:
          u = path.pop()
          inc[u] = False
          qid[u] = vertex
          if u == vertex:
            break

    for i in range(n):
      if ord_[i] == -1:
        dfs(i)

    group_num = 0
    qid_map = {}
    for i in range(n):
      if qid[i] not in qid_map:
        qid_map[qid[i]] = group_num
        group_num += 1
      qid[i] = qid_map[qid[i]]

    result = [[] for _ in range(group_num)]
    for i in range(n):
      result[qid[i]].append(i)
    return result


# ==========================================
# 6. MaxFlow (MFGraph)
# ==========================================
class MFGraph:
  class Edge:
    def __init__(self, to: int, rev: int, cap: int) -> None:
      self.to = to
      self.rev = rev
      self.cap = cap

    def __repr__(self) -> str:
      return f"Edge(to={self.to}, rev={self.rev}, cap={self.cap})"

  def __init__(self, n: int) -> None:
    self._n = n
    self._g = [[] for _ in range(n)]
    self._pos = []

  def add_edge(self, from_el: int, to_el: int, cap: int) -> int:
    assert 0 <= from_el < self._n
    assert 0 <= to_el < self._n
    assert 0 <= cap
    m = len(self._pos)
    from_id = len(self._g[from_el])
    to_id = len(self._g[to_el])
    if from_el == to_el:
      to_id += 1
    self._g[from_el].append(MFGraph.Edge(to_el, to_id, cap))
    self._g[to_el].append(MFGraph.Edge(from_el, from_id, 0))
    self._pos.append((from_el, from_id))
    return m

  def get_edge(self, i: int):
    assert 0 <= i < len(self._pos)
    from_el, from_id = self._pos[i]
    e = self._g[from_el][from_id]
    re = self._g[e.to][e.rev]
    return (from_el, e.to, e.cap + re.cap, re.cap)

  def edges(self):
    return [self.get_edge(i) for i in range(len(self._pos))]

  def change_edge(self, i: int, new_cap: int, new_flow: int) -> None:
    assert 0 <= i < len(self._pos)
    assert 0 <= new_flow <= new_cap
    from_el, from_id = self._pos[i]
    e = self._g[from_el][from_id]
    re = self._g[e.to][e.rev]
    e.cap = new_cap - new_flow
    re.cap = new_flow

  def flow(self, s: int, t: int, flow_limit: int = 10**18) -> int:
    assert 0 <= s < self._n
    assert 0 <= t < self._n
    assert s != t

    flow = 0
    while flow < flow_limit:
      level = [-1] * self._n
      level[s] = 0
      que = [s]
      head = 0
      while head < len(que):
        v = que[head]
        head += 1
        lv = level[v]
        for e in self._g[v]:
          if e.cap == 0 or level[e.to] >= 0:
            continue
          level[e.to] = lv + 1
          if e.to == t:
            break
          que.append(e.to)
        if level[t] >= 0:
          break

      if level[t] < 0:
        break

      iter_ = [0] * self._n
      def augment(v, t, up):
        if v == t:
          return up
        res = 0
        lv = level[v]
        for i in range(iter_[v], len(self._g[v])):
          iter_[v] = i
          e = self._g[v][i]
          if level[e.to] <= lv or e.cap == 0:
            continue
          d = augment(e.to, t, min(up - res, e.cap))
          if d <= 0:
            continue
          e.cap -= d
          self._g[e.to][e.rev].cap += d
          res += d
          if res == up:
            return res
        level[v] = self._n + 1
        return res

      while flow < flow_limit:
        f = augment(s, t, flow_limit - flow)
        if f == 0:
          break
        flow += f
    return flow

  def min_cut(self, s: int):
    visited = [False] * self._n
    que = [s]
    visited[s] = True
    head = 0
    while head < len(que):
      v = que[head]
      head += 1
      for e in self._g[v]:
        if e.cap > 0 and not visited[e.to]:
          visited[e.to] = True
          que.append(e.to)
    return visited


# ==========================================
# 7. MinCostFlow (MCFGraph)
# ==========================================
class MCFGraph:
  class Edge:
    def __init__(self, dst: int, cap: int, cost: int, rev) -> None:
      self.dst = dst
      self.cap = cap
      self.cost = cost
      self.rev = rev

  def __init__(self, n: int) -> None:
    self._n = n
    self._g = [[] for _ in range(n)]
    self._edges = []

  def add_edge(self, src: int, dst: int, cap: int, cost: int) -> int:
    assert 0 <= src < self._n
    assert 0 <= dst < self._n
    assert 0 <= cap
    m = len(self._edges)
    e = MCFGraph.Edge(dst, cap, cost, None)
    re = MCFGraph.Edge(src, 0, -cost, None)
    e.rev = re
    re.rev = e
    self._g[src].append(e)
    self._g[dst].append(re)
    self._edges.append(e)
    return m

  def flow(self, s: int, t: int, flow_limit: int = 10**18):
    return self.slope(s, t, flow_limit)[-1]

  def slope(self, s: int, t: int, flow_limit: int = 10**18):
    assert 0 <= s < self._n
    assert 0 <= t < self._n
    assert s != t

    dual = [0] * self._n
    prev = [None] * self._n

    def refine_dual():
      pq = [(0, s)]
      visited = [False] * self._n
      dist = [None] * self._n
      dist[s] = 0
      while pq:
        d, v = heappop(pq)
        if visited[v]:
          continue
        visited[v] = True
        if v == t:
          break
        for i, e in enumerate(self._g[v]):
          to = e.dst
          if visited[to] or e.cap == 0:
            continue
          cost = e.cost - dual[to] + dual[v]
          if dist[to] is None or dist[to] > dist[v] + cost:
            dist[to] = dist[v] + cost
            prev[to] = (v, i)
            heappush(pq, (dist[to], to))
      if not visited[t]:
        return False
      for v in range(self._n):
        if dist[v] is None:
          continue
        dual[v] -= dist[t] - dist[v]
      return True

    flow = 0
    cost = 0
    prev_cost_per_flow = -1
    result = [(0, 0)]

    while flow < flow_limit:
      if not refine_dual():
        break
      f = flow_limit - flow
      cur = t
      while cur != s:
        p_v, p_i = prev[cur]
        f = min(f, self._g[p_v][p_i].cap)
        cur = p_v
      flow += f
      cost += f * (-dual[s])
      cur = t
      while cur != s:
        p_v, p_i = prev[cur]
        e = self._g[p_v][p_i]
        e.cap -= f
        e.rev.cap += f
        cur = p_v
      if prev_cost_per_flow == -dual[s]:
        result.pop()
      result.append((flow, cost))
      prev_cost_per_flow = -dual[s]

    return result


# ==========================================
# 8. TwoSAT
# ==========================================
class TwoSAT:
  def __init__(self, n: int = 0) -> None:
    self._n = n
    self._scc = SCCGraph(2 * n)
    self._answer = [False] * n

  def add_clause(self, i: int, f: bool, j: int, g: bool) -> None:
    assert 0 <= i < self._n
    assert 0 <= j < self._n
    self._scc.add_edge(2 * i + (0 if f else 1), 2 * j + (1 if g else 0))
    self._scc.add_edge(2 * j + (0 if g else 1), 2 * i + (1 if f else 0))

  def satisfiable(self) -> bool:
    id_ = self._scc.scc()
    qid = [0] * (2 * self._n)
    for i, group in enumerate(id_):
      for vertex in group:
        qid[vertex] = i
    for i in range(self._n):
      if qid[2 * i] == qid[2 * i + 1]:
        return False
      self._answer[i] = qid[2 * i] < qid[2 * i + 1]
    return True

  def answer(self):
    return self._answer


# ==========================================
# 9. String Algorithms (Suffix Array, Z-Algorithm)
# ==========================================
def suffix_array(s):
  if isinstance(s, str):
    s = [ord(c) for c in s]
  n = len(s)
  if n == 0:
    return []
  if n == 1:
    return [0]
  if n == 2:
    if s[0] < s[1]:
      return [0, 1]
    else:
      return [1, 0]
  
  idx = list(range(n))
  idx.sort(key=lambda i: s[i])
  sa = [0] * n
  s_map = [0] * n
  s_map[idx[0]] = 0
  unique_cnt = 1
  for i in range(1, n):
    if s[idx[i]] != s[idx[i - 1]]:
      unique_cnt += 1
    s_map[idx[i]] = unique_cnt - 1

  h = 1
  while unique_cnt < n:
    idx.sort(key=lambda i: (s_map[i], s_map[i + h] if i + h < n else -1))
    sa[idx[0]] = 0
    unique_cnt = 1
    s_map_new = [0] * n
    s_map_new[idx[0]] = 0
    for i in range(1, n):
      prev = idx[i - 1]
      curr = idx[i]
      prev_key = (s_map[prev], s_map[prev + h] if prev + h < n else -1)
      curr_key = (s_map[curr], s_map[curr + h] if curr + h < n else -1)
      if prev_key != curr_key:
        unique_cnt += 1
      s_map_new[curr] = unique_cnt - 1
    s_map = s_map_new
    h *= 2
    if h >= n:
      break
  return idx


def z_algorithm(s):
  if isinstance(s, str):
    s = [ord(c) for c in s]
  n = len(s)
  if n == 0:
    return []
  z = [0] * n
  z[0] = n
  j = 0
  for i in range(1, n):
    k = max(0, min(z[i - j], j + z[j] - i))
    while i + k < n and s[k] == s[i + k]:
      k += 1
    z[i] = k
    if j + z[j] < i + z[i]:
      j = i
  return z


# ==========================================
# 10. Math Utilities (pow_mod, inv_gcd, floor_sum)
# ==========================================
def pow_mod(x: int, n: int, m: int) -> int:
  assert 0 <= n and 1 <= m
  if m == 1:
    return 0
  r = 1
  y = x % m
  while n > 0:
    if n & 1:
      r = (r * y) % m
    y = (y * y) % m
    n >>= 1
  return r

def inv_gcd(a: int, b: int):
  a %= b
  if a == 0:
    return (b, 0)
  sib = b
  s = a
  tz = 0
  while s > 0 and s % 2 == 0 and sib % 2 == 0:
    s //= 2
    sib //= 2
    tz += 1
  prev_x, x = 1, 0
  prev_y, y = 0, 1
  while s > 0:
    while s % 2 == 0:
      s //= 2
      if prev_x % 2 == 0 and prev_y % 2 == 0:
        prev_x //= 2
        prev_y //= 2
      else:
        prev_x = (prev_x + b) // 2
        prev_y = (prev_y - a) // 2
    while sib % 2 == 0:
      sib //= 2
      if x % 2 == 0 and y % 2 == 0:
        x //= 2
        y //= 2
      else:
        x = (x + b) // 2
        y = (y - a) // 2
    if s >= sib:
      s -= sib
      prev_x -= x
      prev_y -= y
    else:
      sib -= s
      x -= prev_x
      y -= prev_y
  prev_x %= b
  if prev_x < 0:
    prev_x += b
  return (sib << tz, prev_x)

def floor_sum(n: int, m: int, a: int, b: int) -> int:
  ans = 0
  if a >= m:
    ans += (n - 1) * n // 2 * (a // m)
    a %= m
  if b >= m:
    ans += n * (b // m)
    b %= m
  y_max = (a * n + b) // m
  x_max = y_max * m - b
  if y_max == 0:
    return ans
  ans += (n - (x_max + a - 1) // a) * y_max
  ans += floor_sum(y_max, a, m, (a - x_max % a) % a)
  return ans

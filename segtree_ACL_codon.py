# AtCoder Library (ACL) - FenwickTree, SegTree & LazySegTree (Combined & Converted for Codon)

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

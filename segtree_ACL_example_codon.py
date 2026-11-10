# --- 1. FenwickTree (BIT) の使い方 ---
bit = FenwickTree(5)
bit.add(1, 10)
bit.add(3, 20)
print("FenwickTree sum(0, 4):", bit.sum(0, 4))  # 出力: 30


# --- 2. SegTree (通常のセグメント木) の使い方 ---
# 例: 区間最小値 (RMQ) を求めるセグメント木
op_seg = lambda a, b: min(a, b)
e_seg = lambda: float('inf') # または十分に大きな数

initial_v = [5, 2, 6, 3, 1]
seg = SegTree(op_seg, e_seg, initial_v)

print("SegTree prod(1, 4):", seg.prod(1, 4))  # 区間 [1, 4) の最小値 -> min(2, 6, 3) = 2

# 要素の更新（インデックス 2 の値を 0 に変更）
seg.set(2, 0)
print("SegTree prod(1, 4) after update:", seg.prod(1, 4))  # 出力: 0


# --- 3. LazySegTree (遅延評価セグメント木) の使い方 ---
# 例: 区間加算・区間総和クエリ
op_lazy = lambda a, b: a + b
e_lazy = lambda: 0
mapping = lambda f, x: x + f
composition = lambda f, g: f + g
id_ = 0

initial_v_lazy = [1, 2, 3, 4, 5]
lz_seg = LazySegTree(op_lazy, e_lazy, mapping, composition, id_, initial_v_lazy)

# 区間 [1, 4) に 10 を加算
lz_seg.apply(1, 4, 10)

# 区間 [0, 5) の総和を取得
print("LazySegTree all_prod:", lz_seg.all_prod())  # 出力: 45

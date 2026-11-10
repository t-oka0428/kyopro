def main():
  print("=== 1. DSU ===")
  dsu = DSU(4)
  dsu.merge(0, 1)
  dsu.merge(2, 3)
  print("same(0, 1):", dsu.same(0, 1))  # True

  print("\n=== 2. FenwickTree ===")
  bit = FenwickTree(5)
  bit.add(0, 10)
  bit.add(2, 20)
  print("sum(0, 3):", bit.sum(0, 3))    # 30

  print("\n=== 3. SegTree ===")
  seg = SegTree(lambda a, b: a + b, lambda: 0, [1, 2, 3, 4, 5])
  print("prod(1, 4):", seg.prod(1, 4))  # 9 (2+3+4)

  print("\n=== 4. LazySegTree ===")
  lz = LazySegTree(lambda a, b: a + b, lambda: 0, lambda f, x: x + f, lambda f, g: f + g, 0, [1, 2, 3, 4, 5])
  lz.apply(1, 4, 10)
  print("all_prod after apply:", lz.all_prod())  # 45

  print("\n=== 5. SCCGraph ===")
  scc = SCCGraph(3)
  scc.add_edge(0, 1)
  scc.add_edge(1, 2)
  scc.add_edge(2, 0)
  print("SCC groups:", scc.scc())

  print("\n=== 6. MFGraph (MaxFlow) ===")
  mf = MFGraph(3)
  #add_edge(始点,終点,容量)
  mf.add_edge(0, 1, 10)
  mf.add_edge(1, 2, 10)
  #get_edge(i) => i番目の辺の(始点,終点,容量,流量)
  print("Max Flow (0 -> 2):", mf.flow(0, 2))  # 10

  print("\n=== 7. MCFGraph (MinCostFlow) ===")
  mcf = MCFGraph(3)
  mcf.add_edge(0, 1, 10, 1)
  mcf.add_edge(1, 2, 10, 2)
  print("Min Cost Flow (0 -> 2, flow 5):", mcf.flow(0, 2, 5))  # 15

  print("\n=== 8. TwoSAT ===")
  ts = TwoSAT(2)
  ts.add_clause(0, True, 1, True)
  print("Satisfiable:", ts.satisfiable())

  print("\n=== 9. String Algorithms ===")
  print("Suffix Array of 'abracadabra':", suffix_array("abracadabra"))
  print("Z-Algorithm of 'abracadab':", z_algorithm("abracadab"))

  print("\n=== 10. Math Utilities ===")
  print("pow_mod(2, 10, 1000):", pow_mod(2, 10, 1000))
  #floor_sum(N,M,A,B) = sum {0 <= i < N} floor((Ai+B)//M)
  print("floor_sum(10, 3, 2, 1):", floor_sum(10, 3, 2, 1))

  print("\n=== 11. Convolution ===")
  a = [1, 2, 3]
  b = [4, 5, 6]
  print("convolution(998244353, a, b):", convolution(998244353, a, b))
  print("convolution_int(a, b):", convolution_int(a, b))

https://github.com/t-oka0428/kyopro/blob/main/custom_sort.py

#比較関数でsortしたいときに使用
#cmp_to_keyは遅いのでこちらで
def custom_sorted(arr):
  if len(arr) <= 1:
    return arr

  stack = [(0, len(arr) - 1)]
  while stack:
    left, right = stack.pop()
    if left >= right:
      continue

    # ピボットの選択（中央の要素を取るのが一般的）
    pivot = arr[(left + right) // 2]

    i, j = left, right
    while i <= j:
      # m1 = (arr[i] < pivot) とする
      while i <= j and True: # Todo:Trueをm1に変更
        i += 1

      # m2 = (pivot < arr[j]) とする
      while i <= j and True: # Todo:Trueをm2に変更
        j -= 1

      if i <= j:
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1

    # 分割した区間をスタックに追加
    if left < j:
      stack.append((left, j))
    if i < right:
      stack.append((i, right))

  return arr

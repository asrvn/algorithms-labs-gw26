def bubble_sort(arr):
  n = len(arr)
  flag = False


  for i in range(n):
    print(f"pass: {i}")
    swapped = False
    for j in range(0, n - i - 1):
      print(f"Comparison: {arr[j]} > {arr[j + 1]}", end = "; ")
      if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        flag = True
        swapped = True
      print(arr , end = "; ")
      if flag:
        print("Swap")
      else:
        print("Keep")
      flag = False
    if not swapped:
      break
  return arr

print(bubble_sort([5, 2, 9, 1, 5, 6]))
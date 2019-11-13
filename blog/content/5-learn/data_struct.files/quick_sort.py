def quick_sort(collection):
  '''简单版, 需要额外的 O(n) 的空间'''
  length = len(collection)
  if length <= 1:
    return collection
  else:
    # Use the last element as the first pivot
    pivot = collection.pop()
    # Put elements greater than pivot in greater list
    # Put elements lesser than pivot in lesser list
    greater, lesser = [], []
    for element in collection:
      if element > pivot:
        greater.append(element)
      else:
        lesser.append(element)
    return quick_sort(lesser) + [pivot] + quick_sort(greater)


def partition(array, left, right, pivot_index):
  '''就地划分'''
  pivot_val = array[pivot_index]
  array[pivot_index], array[right] = array[right], array[pivot_index]

  index = left
  for i in range(left, right):
    if array[i] <= pivot_val:
      array[index], array[i] = array[i], array[index]
      index += 1

  array[right], array[index] = array[index], array[right]
  return index


def quick_sort_in_place(array, left, right):
  '''就地排序版快速排序'''
  if right > left:
    pivot_index = left
    new_pivot_index = partition(array, left, right, pivot_index)
    quick_sort_in_place(array, left, new_pivot_index - 1)
    quick_sort_in_place(array, new_pivot_index + 1, right)


def quicksort(alist, first, last):
  '''就地排序版'''
  if first >= last:
    return
  mid_value = alist[first]
  low = first
  high = last
  while low < high:
    while low < high and alist[high] >= mid_value:
      high -= 1
    alist[low] = alist[high]
    while low < high and alist[low] < mid_value:
      low += 1
    alist[high] = alist[low]
  alist[low] = mid_value
  quicksort(alist, first, low - 1)
  quicksort(alist, low + 1, last)


if __name__ == '__main__':
  array = [3, 7, 8, 5, 2, 1, 9, 5, 4]
  quicksort(array, 0, len(array) - 1)
  print(array)

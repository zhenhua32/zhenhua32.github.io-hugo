+++
title = "核心数据结构"
date =  2019-11-13T12:39:07+08:00
weight = 1
+++

## 简介

可以阅读一下 `程序员面试经典(第6版)`, 其中第 7 章是可以公开阅读的,
[第 7 章 技术面试题](https://www.ituring.com.cn/book/tupubarticle/27952).

里面介绍了一下解面试题的技巧, 但第一步是熟练掌握核心的数据结构算法和概念.

| 数据结构           | 算法         | 概念            |
| ------------------ | ------------ | --------------- |
| 链表               | 广度优先搜索 | 位操作          |
| 树、单词查找树、图 | 深度优先搜索 | 内存（堆和栈）  |
| 栈和队列           | 二分查找     | 递归            |
| 堆                 | 归并排序     | 动态规划        |
| 向量/数组列表      | 快排         | 大 O 时间及空间 |
| 散列表             |              |                 |

只记录最基础常见的内容, Python 实现.

## 数据结构

### 链表

链表是一种线性表, 通过在每个节点上存储下一个节点的指针, 来实现对整个链表的访问.

链表插入删除可以达到 O(1), 查找需要 O(n).

```python
class Node:
  def __init__(self, item, next):
    self.item = item
    self.next = next


class LinkedList:
  def __init__(self):
    self.head = None

  def add(self, item):
    self.head = Node(item, self.head)

  def remove(self):
    if self.is_empty():
      return None
    else:
      item = self.head.item
      self.head = self.head.next
      return item

  def is_empty(self):
    return self.head is None

```

### 树

#### 二叉树

二叉树是每个节点最多只有两个子节点的树.
完全二叉树是二叉树的特例, 除了最后一层, 其余层都是满的, 且最后一层要么是满的, 要么只在右边缺少连续若干个节点.
满二叉树是所有层都是满的二叉树.

```python
class Node:  # This is the Class Node with constructor that contains data variable to type data and left,right pointers.
  def __init__(self, data):
    self.data = data
    self.left = None
    self.right = None


def display(tree):  # In Order traversal of the tree

  if tree is None:
    return

  if tree.left is not None:
    display(tree.left)

  print(tree.data)

  if tree.right is not None:
    display(tree.right)

  return


def depth_of_tree(tree):  # This is the recursive function to find the depth of binary tree.
  if tree is None:
    return 0
  else:
    depth_l_tree = depth_of_tree(tree.left)
    depth_r_tree = depth_of_tree(tree.right)
    if depth_l_tree > depth_r_tree:
      return 1 + depth_l_tree
    else:
      return 1 + depth_r_tree


def is_full_binary_tree(tree):  # This functions returns that is it full binary tree or not?
  if tree is None:
    return True
  if (tree.left is None) and (tree.right is None):
    return True
  if (tree.left is not None) and (tree.right is not None):
    return is_full_binary_tree(tree.left) and is_full_binary_tree(tree.right)
  else:
    return False
```

#### 二叉树的遍历

访问二叉树可以分解为 3 个步骤, 访问左子树, 访问根节点, 访问右子树. 分别用 LDR 表示, 根据根节点的访问顺序, 可以分为

- 前序遍历 DLR
- 中序遍历 LDR
- 后序遍历 LRD

深度优先遍历是指从根节点出发, 优先访问最远的节点, 前中后序遍历都是深度优先遍历的特例.

广度优先遍历时指优先访问离根节点最近的节点, 又称为层次遍历, 通常借助队列实现.

```python
"""
This is pure python implementation of tree traversal algorithms
"""
import queue
from typing import List


class TreeNode:
  def __init__(self, data):
    self.data = data
    self.right = None
    self.left = None

def pre_order(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> pre_order(root)
    1 2 4 5 3 6 7
    """
  if not isinstance(node, TreeNode) or not node:
    return
  print(node.data, end=" ")
  pre_order(node.left)
  pre_order(node.right)


def in_order(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> in_order(root)
    4 2 5 1 6 3 7
    """
  if not isinstance(node, TreeNode) or not node:
    return
  in_order(node.left)
  print(node.data, end=" ")
  in_order(node.right)


def post_order(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> post_order(root)
    4 5 2 6 7 3 1
    """
  if not isinstance(node, TreeNode) or not node:
    return
  post_order(node.left)
  post_order(node.right)
  print(node.data, end=" ")


def level_order(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> level_order(root)
    1 2 3 4 5 6 7
    """
  if not isinstance(node, TreeNode) or not node:
    return
  q: queue.Queue = queue.Queue()
  q.put(node)
  while not q.empty():
    node_dequeued = q.get()
    print(node_dequeued.data, end=" ")
    if node_dequeued.left:
      q.put(node_dequeued.left)
    if node_dequeued.right:
      q.put(node_dequeued.right)


# iteration version
def pre_order_iter(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> pre_order_iter(root)
    1 2 4 5 3 6 7
    """
  if not isinstance(node, TreeNode) or not node:
    return
  stack: List[TreeNode] = []
  n = node
  while n or stack:
    while n:  # start from root node, find its left child
      print(n.data, end=" ")
      stack.append(n)
      n = n.left
    # end of while means current node doesn't have left child
    n = stack.pop()
    # start to traverse its right child
    n = n.right


def in_order_iter(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> in_order_iter(root)
    4 2 5 1 6 3 7
    """
  if not isinstance(node, TreeNode) or not node:
    return
  stack: List[TreeNode] = []
  n = node
  while n or stack:
    while n:
      stack.append(n)
      n = n.left
    n = stack.pop()
    print(n.data, end=" ")
    n = n.right


def post_order_iter(node: TreeNode) -> None:
  """
    >>> root = TreeNode(1)
    >>> tree_node2 = TreeNode(2)
    >>> tree_node3 = TreeNode(3)
    >>> tree_node4 = TreeNode(4)
    >>> tree_node5 = TreeNode(5)
    >>> tree_node6 = TreeNode(6)
    >>> tree_node7 = TreeNode(7)
    >>> root.left, root.right = tree_node2, tree_node3
    >>> tree_node2.left, tree_node2.right = tree_node4 , tree_node5
    >>> tree_node3.left, tree_node3.right = tree_node6 , tree_node7
    >>> post_order_iter(root)
    4 5 2 6 7 3 1
    """
  if not isinstance(node, TreeNode) or not node:
    return
  stack1, stack2 = [], []
  n = node
  stack1.append(n)
  while stack1:  # to find the reversed order of post order, store it in stack2
    n = stack1.pop()
    if n.left:
      stack1.append(n.left)
    if n.right:
      stack1.append(n.right)
    stack2.append(n)
  while stack2:  # pop up from stack2 will be the post order
    print(stack2.pop().data, end=" ")

```

#### 单词查找树

单词查找树, trie, 又叫做前缀树或字典树. 常用于搜索提示.

```python
"""
A Trie/Prefix Tree is a kind of search tree used to provide quick lookup
of words/patterns in a set of words. A basic Trie however has O(n^2) space complexity
making it impractical in practice. It however provides O(max(search_string, length of longest word))
lookup time making it an optimal approach when space is not an issue.
"""


class TrieNode:
  def __init__(self):
    self.nodes = dict()  # Mapping from char to TrieNode
    self.is_leaf = False  # 叶节点是没有值的, 即 nodes 是空的

  def insert_many(self, words: [str]):
    """
    Inserts a list of words into the Trie
    :param words: list of string words
    :return: None
    """
    for word in words:
      self.insert(word)

  def insert(self, word: str):
    """
    Inserts a word into the Trie
    :param word: word to be inserted
    :return: None
    """
    curr = self
    for char in word:
      if char not in curr.nodes:
        curr.nodes[char] = TrieNode()
      curr = curr.nodes[char]
    curr.is_leaf = True

  def find(self, word: str) -> bool:
    """
    Tries to find word in a Trie
    :param word: word to look for
    :return: Returns True if word is found, False otherwise
    """
    curr = self
    for char in word:
      if char not in curr.nodes:
        return False
      curr = curr.nodes[char]
    return curr.is_leaf

  def delete(self, word: str):
    """
    Deletes a word in a Trie
    :param word: word to delete
    :return: None
    """
    def _delete(curr: TrieNode, word: str, index: int):
      if index == len(word):
        # If word does not exist
        if not curr.is_leaf:
          return False
        curr.is_leaf = False
        return len(curr.nodes) == 0
      char = word[index]
      char_node = curr.nodes.get(char)
      # If char not in current trie node
      if not char_node:
        return False
      # Flag to check if node can be deleted
      delete_curr = _delete(char_node, word, index + 1)
      if delete_curr:
        del curr.nodes[char]
        return len(curr.nodes) == 0
      return delete_curr

    _delete(self, word, 0)

```

### 栈和队列

栈是一种线性数据结构, 以后进先出 LIFO 的原理运作.

队列是一种线性数据结构, 以先进先出 FIFO 的原理运作.

### 堆

堆是一种特殊的树结构, 给定堆中的任意节点 P 和 C, 如果 P 是 C 的祖先节点, 那么 P 的值总数小于等于(或大于等于) C 的值.

堆根据判断条件, 可以分为最小堆和最大堆.

堆通常用于事件模拟, 可以实现排序即堆排序.

```python

```

### 散列表

散列表(哈希表)是根据键通过计算直接访问内存存储位置的数据结构. 这个映射函数叫做散列函数, 存储数据的数组叫做散列表.

```python
from number_theory.prime_numbers import next_prime


class HashTable:
  """
  Basic Hash Table example with open addressing and linear probing
  """
  def __init__(self, size_table, charge_factor=None, lim_charge=None):
    self.size_table = size_table
    self.values = [None] * self.size_table
    self.lim_charge = 0.75 if lim_charge is None else lim_charge
    self.charge_factor = 1 if charge_factor is None else charge_factor
    self.__aux_list = []
    self._keys = {}

  def keys(self):
    return self._keys

  def balanced_factor(self):
    return sum([1 for slot in self.values if slot is not None]) / (self.size_table * self.charge_factor)

  def hash_function(self, key):
    return key % self.size_table

  def _step_by_step(self, step_ord):

    print("step {0}".format(step_ord))
    print([i for i in range(len(self.values))])
    print(self.values)

  def bulk_insert(self, values):
    i = 1
    self.__aux_list = values
    for value in values:
      self.insert_data(value)
      self._step_by_step(i)
      i += 1

  def _set_value(self, key, data):
    self.values[key] = data
    self._keys[key] = data

  def _colision_resolution(self, key, data=None):
    new_key = self.hash_function(key + 1)

    while self.values[new_key] is not None and self.values[new_key] != key:

      if self.values.count(None) > 0:
        new_key = self.hash_function(new_key + 1)
      else:
        new_key = None
        break

    return new_key

  def rehashing(self):
    survivor_values = [value for value in self.values if value is not None]
    self.size_table = next_prime(self.size_table, factor=2)
    self._keys.clear()
    self.values = [None] * self.size_table  # hell's pointers D: don't DRY ;/
    map(self.insert_data, survivor_values)

  def insert_data(self, data):
    key = self.hash_function(data)

    if self.values[key] is None:
      self._set_value(key, data)

    elif self.values[key] == data:
      pass

    else:
      colision_resolution = self._colision_resolution(key, data)
      if colision_resolution is not None:
        self._set_value(colision_resolution, data)
      else:
        self.rehashing()
        self.insert_data(data)

```

## 算法

### 二分查找

二分查找是在有序数组章查找某一个元素的搜索算法.

时间复杂度是 O(log n).

```python
"""
This is pure python implementation of binary search algorithm
For doctests run following command:
python -m doctest -v binary_search.py
or
python3 -m doctest -v binary_search.py
For manual testing run:
python binary_search.py
"""
import bisect


def binary_search(sorted_collection, item):
  """Pure implementation of binary search algorithm in Python
    Be careful collection must be ascending sorted, otherwise result will be
    unpredictable
    :param sorted_collection: some ascending sorted collection with comparable items
    :param item: item value to search
    :return: index of found item or None if item is not found
    Examples:
    >>> binary_search([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search([0, 5, 7, 10, 15], 6)
    """
  left = 0
  right = len(sorted_collection) - 1

  while left <= right:
    midpoint = left + (right - left) // 2
    current_item = sorted_collection[midpoint]
    if current_item == item:
      return midpoint
    elif item < current_item:
      right = midpoint - 1
    else:
      left = midpoint + 1
  return None


def binary_search_std_lib(sorted_collection, item):
  """Pure implementation of binary search algorithm in Python using stdlib
    Be careful collection must be ascending sorted, otherwise result will be
    unpredictable
    :param sorted_collection: some ascending sorted collection with comparable items
    :param item: item value to search
    :return: index of found item or None if item is not found
    Examples:
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 6)
    """
  index = bisect.bisect_left(sorted_collection, item)
  if index != len(sorted_collection) and sorted_collection[index] == item:
    return index
  return None


def binary_search_by_recursion(sorted_collection, item, left, right):
  """Pure implementation of binary search algorithm in Python by recursion
    Be careful collection must be ascending sorted, otherwise result will be
    unpredictable
    First recursion should be started with left=0 and right=(len(sorted_collection)-1)
    :param sorted_collection: some ascending sorted collection with comparable items
    :param item: item value to search
    :return: index of found item or None if item is not found
    Examples:
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 6)
    """
  if right < left:
    return None

  midpoint = left + (right - left) // 2

  if sorted_collection[midpoint] == item:
    return midpoint
  elif sorted_collection[midpoint] > item:
    return binary_search_by_recursion(sorted_collection, item, left, midpoint - 1)
  else:
    return binary_search_by_recursion(sorted_collection, item, midpoint + 1, right)

```

]

### 快速排序

平均情况下时间复杂度是 O(n log n), 最坏的情况下是 O(n^2).

```python
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

```

## 参考

[TheAlgorithms Python](https://github.com/TheAlgorithms/Python): 代码实现基本来自这里.

{{%attachments title="相关代码文件" pattern=".*(py)"/%}}

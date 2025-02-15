import random
import time


class DoublyLinkedListNode:
    def __init__(self, key, value):
        self.data = (key, value)
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = DoublyLinkedListNode(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node
        if not self.tail:
            self.tail = new_node
        return new_node

    def remove_last(self):
        if not self.tail:
            return None
        node = self.tail
        if self.tail.prev:
            self.tail.prev.next = None
        self.tail = self.tail.prev
        if not self.tail:
            self.head = None
        return node

    def remove(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                if current_node.prev:
                    current_node.prev.next = current_node.next
                else:
                    self.head = current_node.next
                if current_node.next:
                    current_node.next.prev = current_node.prev
                else:
                    self.tail = current_node.prev
                    current_node.prev = None
                    current_node.next = None
                return True
            current_node = current_node.next
        return False

    def move_to_front(self, node):
        if node is self.head:
            return
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node is self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last and last.data[0] in self.cache:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node


def range_sum_no_cache(array: list, L, R):
    return sum(array[L:R + 1])


def update_no_cache(array: list, index: int, value):
    array[index] = value


def range_sum_with_cache(array: list, L, R):
    global hits_count
    key = (L, R)
    cached_value = lru_cache.get(key)
    if cached_value and cached_value is not None and cached_value != -1:
        hits_count += 1
        return cached_value
    result = sum(array[L:R + 1])
    lru_cache.put(key, result)
    return result


def update_with_cache(array: list, index: int, value):
    global clears_count
    array[index] = value
    keys_to_remove = [key for key in lru_cache.cache.keys() if key[0] <= index <= key[1]]
    if len(keys_to_remove) > 0:
        clears_count += 1
        for key in keys_to_remove:
            del lru_cache.cache[key]
            lru_cache.list.remove(key)




if __name__ == "__main__":
    lru_cache = LRUCache(1000)
    hits_count = 0
    ranges_count = 0
    clears_count = 0
    combination_count_sqrt = 45
    arr = [random.randint(1, 1000) for _ in range(100_000)]
    queries = []
    for _ in range(50_000):
        if random.random() < 0.8:
            L, R = sorted([random.randint(50000, 50000 + combination_count_sqrt), random.randint(80000, 80000 + combination_count_sqrt)])
            queries.append(('Range', L, R))
            ranges_count += 1
        else:
            index, value = random.randint(0, 50000 + combination_count_sqrt), random.randint(1, 1000)
            queries.append(('Update', index, value))

    array = arr[:]
    start = time.time()
    for query in queries:
        match query[0]:
            case 'Range':
                range_sum_no_cache(array, query[1], query[2])
            case 'Update':
                update_no_cache(array, query[1], query[2])
    print(f'Execution time without cache: {time.time() - start:.4f} sec')

    array = arr[:]
    start = time.time()
    for query in queries:
        match query[0]:
            case 'Range':
                range_sum_with_cache(array, query[1], query[2])
            case 'Update':
                update_with_cache(array, query[1], query[2])
    print(f'Execution time with LRU-cache: {time.time() - start:.4f} sec')

    print(f'Queries count: {len(queries)}')
    print(f'Ranges count: {ranges_count}')
    print(f'Unique ranges count: {combination_count_sqrt ** 2}')
    print(f'Hits count: {hits_count}')
    print(f'Hits percent: {hits_count*100/ranges_count:.2f} %')




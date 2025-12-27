class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Додавання в кінець (для тестів)
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    # Друк списку
    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data, end=" -> ")
            cur = cur.next
        print("None")

    # 1) Реверсування (зміна посилань)
    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    # 2) Сортування (Merge Sort для linked list)
    def sort(self):
        self.head = self._merge_sort(self.head)

    def _merge_sort(self, head):
        if head is None or head.next is None:
            return head

        middle = self._get_middle(head)
        right_head = middle.next
        middle.next = None  # розрізаємо список на 2 частини

        left_sorted = self._merge_sort(head)
        right_sorted = self._merge_sort(right_head)

        return self._merge(left_sorted, right_sorted)

    def _get_middle(self, head):
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def _merge(self, left, right):
        dummy = Node(0)
        tail = dummy

        while left and right:
            if left.data <= right.data:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next

        tail.next = left if left else right
        return dummy.next

    # 3) Злиття двох ВЖЕ відсортованих списків в один відсортований
    @staticmethod
    def merge_sorted_lists(l1_head, l2_head):
        dummy = Node(0)
        tail = dummy

        while l1_head and l2_head:
            if l1_head.data <= l2_head.data:
                tail.next = l1_head
                l1_head = l1_head.next
            else:
                tail.next = l2_head
                l2_head = l2_head.next
            tail = tail.next

        tail.next = l1_head if l1_head else l2_head
        return dummy.next


if __name__ == "__main__":
    print("=== Початковий список ===")
    ll = LinkedList()
    for value in [4, 2, 5, 1, 3]:
        ll.append(value)
    ll.print_list()

    print("\n=== Реверсування ===")
    ll.reverse()
    ll.print_list()

    print("\n=== Сортування ===")
    ll.sort()
    ll.print_list()

    print("\n=== Злиття двох відсортованих списків ===")
    l1 = LinkedList()
    l2 = LinkedList()

    for v in [1, 3, 5]:
        l1.append(v)
    for v in [2, 4, 6]:
        l2.append(v)

    merged = LinkedList()
    merged.head = LinkedList.merge_sorted_lists(l1.head, l2.head)
    merged.print_list()

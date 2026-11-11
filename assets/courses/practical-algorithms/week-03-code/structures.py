class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def linked(values):
    dummy = tail = ListNode()
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def linked_values(head):
    result, seen = [], set()
    while head:
        if head in seen:
            raise ValueError("cycle in linked list")
        seen.add(head)
        result.append(head.val)
        head = head.next
    return result

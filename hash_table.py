class Contact:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        new_node = Node(key, Contact(key, value))

        # Empty slot: new node becomes the head
        if self.data[index] is None:
            self.data[index] = new_node
            return

        # Walk the chain: update if the key exists, otherwise append at the tail
        current = self.data[index]
        while True:
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                current.next = new_node
                return
            current = current.next

    def search(self, key):
        current = self.data[self.hash_function(key)]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self):
        for i in range(self.size):
            current = self.data[i]
            if current is None:
                print(f"Index {i}: Empty")
            else:
                line = f"Index {i}:"
                while current:
                    line += f" - {current.value}"
                    current = current.next
                print(line)


if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()

    table.insert("Joao", "909-876-1234")
    table.insert("Nino", "111-555-0002")
    table.print_table()

    contact = table.search("Joao")
    print("\nSearch result:", contact)

    # Edge case 1: collisions
    table.insert("Nevan", "111-222-3333")
    table.insert("Christine", "222-333-1111")
    table.print_table()

    # Edge case 2: duplicate key
    table.insert("Nino", "999-444-9999")
    table.print_table()

    # Edge case 3: missing key
    print(table.search("Sammy"))


"""
DESIGN MEMO

A hash table is the right structure for fast lookups because it turns a name
directly into an array index. Instead of scanning every contact, the hash
function computes where a contact should live, so insert and search take
roughly constant time on average, no matter how many entries are stored. A
list would need to check names one by one, which gets slower as the contact
list grows.

I handled collisions with separate chaining. Each array slot holds either None
or the head of a linked list of Node objects. When two names hash to the same
index, like "Nino" and "Nevan", the new node is added to the end of that index's
chain. During insert I walk the chain first: if the key already exists, I
update the contact's number instead of adding a duplicate. Search uses the
same walk and returns None if the name is not found. My hash function sums the
ord() values of each character and takes the remainder by the table size.

The tradeoff is that a poor hash function or a small table creates long
chains, and lookups drift toward linear time. Keeping the table size
reasonable relative to the number of contacts keeps chains short.

An engineer would choose a hash table over a list or tree when the main
operations are exact-match lookups, inserts, and updates by key, and speed
matters more than ordering. A balanced tree keeps keys sorted and supports
range queries in O(log n), but a hash table is usually faster for simple key
lookups. If I needed contacts in alphabetical order, I would choose a tree.
"""
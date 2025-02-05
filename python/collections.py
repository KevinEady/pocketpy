from typing import TypeVar, Iterable

def Counter[T](iterable: Iterable[T]):
    a: dict[T, int] = {}
    for x in iterable:
        if x in a:
            a[x] += 1
        else:
            a[x] = 1
    return a


class defaultdict(dict):
    def __init__(self, default_factory, *args):
        super().__init__(*args)
        self.default_factory = default_factory

    def __missing__(self, key):
        self[key] = self.default_factory()
        return self[key]

    def __repr__(self) -> str:
        return f"defaultdict({self.default_factory}, {super().__repr__()})"

    def copy(self):
        return defaultdict(self.default_factory, self)


class deque[T]:
    _data: list[T]
    _head: int
    _tail: int
    _capacity: int

    def __init__(self, iterable: Iterable[T] = None):
        self._data = [None] * 8 # type: ignore
        self._head = 0
        self._tail = 0
        self._capacity = len(self._data)

        if iterable is not None:
            self.extend(iterable)

    def __resize_2x(self):
        backup = list(self)
        self._capacity *= 2
        self._head = 0
        self._tail = len(backup)
        self._data.clear()
        self._data.extend(backup)
        self._data.extend([None] * (self._capacity - len(backup)))

    def append(self, x: T):
        self._data[self._tail] = x
        self._tail = (self._tail + 1) % self._capacity
        if (self._tail + 1) % self._capacity == self._head:
            self.__resize_2x()

    def appendleft(self, x: T):
        self._head = (self._head - 1) % self._capacity
        self._data[self._head] = x
        if (self._tail + 1) % self._capacity == self._head:
            self.__resize_2x()

    def copy(self):
        return deque(self)
    
    def count(self, x: T) -> int:
        n = 0
        for item in self:
            if item == x:
                n += 1
        return n
    
    def extend(self, iterable: Iterable[T]):
        for x in iterable:
            self.append(x)

    def extendleft(self, iterable: Iterable[T]):
        for x in iterable:
            self.appendleft(x)
    
    def pop(self) -> T:
        if self._head == self._tail:
            raise IndexError("pop from an empty deque")
        self._tail = (self._tail - 1) % self._capacity
        return self._data[self._tail]
    
    def popleft(self) -> T:
        if self._head == self._tail:
            raise IndexError("pop from an empty deque")
        x = self._data[self._head]
        self._head = (self._head + 1) % self._capacity
        return x
    
    def clear(self):
        i = self._head
        while i != self._tail:
            self._data[i] = None # type: ignore
            i = (i + 1) % self._capacity
        self._head = 0
        self._tail = 0

    def rotate(self, n: int = 1):
        if len(self) == 0:
            return
        if n > 0:
            n = n % len(self)
            for _ in range(n):
                self.appendleft(self.pop())
        elif n < 0:
            n = -n % len(self)
            for _ in range(n):
                self.append(self.popleft())

    def __len__(self) -> int:
        return (self._tail - self._head) % self._capacity

    def __contains__(self, x: object) -> bool:
        for item in self:
            if item == x:
                return True
        return False
    
    def __iter__(self):
        i = self._head
        while i != self._tail:
            yield self._data[i]
            i = (i + 1) % self._capacity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, deque):
            return NotImplemented
        if len(self) != len(other):
            return False
        for x, y in zip(self, other):
            if x != y:
                return False
        return True
    
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, deque):
            return NotImplemented
        return not self == other
    
    def __repr__(self) -> str:
        return f"deque({list(self)!r})"


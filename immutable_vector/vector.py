import contextlib
import math
from typing import *

from typing_extensions import *

from .utils import is_power_of

T = TypeVar("T")
S = TypeVar("S")

# Constants that define the shape of the tree structure.
# In production, BITS would likely be log_2(32) = 5, like that of Clojure's
# Vector implemenetation.

# Levels of the tree, also used to slice up a given index into
# the vector into BITS intervals. So 4 = b0100 would be broken up into
# 01 and 00.
BITS = 2
# Width of the leaf nodes.
WIDTH = 1 << BITS
# Mask to slice up the aforesaid index, or key.
MASK = WIDTH - 1


NodeType = List[Union[Optional[T], "Node[T]"]]


class Node(Generic[T]):
    def __init__(self, children: Optional[NodeType[T]] = None):
        if children is not None:
            self.children = children + [None] * (WIDTH - len(children))
        else:
            self.children = [None] * WIDTH

    def copy(self):
        return Node(list(self.children))


class Vector(Sequence[Optional[T]]):
    def __init__(self, vals: List[T]):
        self.root: Node[T] = Node()
        self.length = 0
        self.mutation = False
        self.leaf: Optional[Node[T]] = None

        self.mutate()
        for val in vals:
            self.append(val)
        self.mutate()

    def __len__(self) -> int:
        return self.length

    @overload
    def __getitem__(self, key: int) -> T:
        pass

    @overload
    def __getitem__(self, key: slice) -> "Vector[T]":
        pass

    def __getitem__(self, key: Union[int, slice]) -> Union[T, "Vector[T]"]:
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return Vector([self[i] for i in range(start, stop, step)])
        elif isinstance(key, int):
            key = key + self.length if key < 0 else key
            if key > self.length - 1:
                raise IndexError
            else:
                return self._at(key)
        else:
            raise TypeError(f"Invalid argument type: {type(key)}")

    @staticmethod
    def _create(root: Node[T], length: int) -> "Vector":
        out: "Vector" = Vector([])
        out.root = root
        out.length = length
        return out

    def _reduce_node(
        self,
        key: int,
        reducer: Callable[[S, int, int], S],
        init: S,
        depth: Optional[int] = None,
    ) -> S:
        """Low-level list reduction API.

        Args:
            key (int): leaf child key index. For example, if you wanted to grab the last element
            of an array of n elements, key = n.
            reducer (Callable[[S, int, int], S]): Reduction function that requires:
                a reducer value of type S,
                the current level in the tree **(0-indexed from the bottom up)**,
                a current index into said level. 
            init (S): initial value to reduce upon.
            depth (Optional[int], optional): depth to traverse down to. Defaults to the list's max depth.

        Returns:
            S: the reduced value.
        """
        depth = self.depth() if depth is None else depth

        acc = init

        for level in range(depth, 0, -1):
            ix = (key >> (level * BITS)) & MASK
            acc = reducer(acc, level, ix)

        return acc

    def _at(self, key: int) -> T:
        """Returns an element located at index `key`.
        """
        leaf_ix = key & MASK

        def reducer(node: Node[T], level: int, ix: int) -> Node[T]:
            return node.children[ix]

        leaf = self._reduce_node(key, reducer, self.root)
        val = leaf.children[leaf_ix]
        # Save the leaf node for later use.
        self.leaf = leaf
        return cast(T, val)

    def depth(self) -> int:
        return 0 if self.length == 0 else math.floor(math.log(self.length, WIDTH))

    def mutate(self) -> None:
        self.mutation = not self.mutation

    def append(self, val: T) -> "Vector":
        """There's 3 cases when appending, in order initial possibility:
         1. Root overflow: there's no more space in the entire tree: thus we must
         create an entirely new root, whereof's left branch is the current root.

         2. There's no room in the left branch, and the right branch is None: thus we must
         create a right branch and fill its first element with "value".

         3. There's space in the current branch: we simply insert "value" here,
         path copying on the way down.
        """
        root = Node(list(self.root.children)) if not self.mutation else self.root
        length = self.length + 1
        key = self.length
        leaf_ix = key & MASK

        # Case 1.
        if is_power_of(self.length, WIDTH):
            root = Node([root])

        def reducer(node: Node[T], level: int, ix: int) -> Node[T]:
            # Case 2.
            children = node.children[ix]

            if children is None:
                node.children[ix] = Node()
            else:
                node.children[ix] = children.copy() if not self.mutation else children
            return node.children[ix]

        leaf = self._reduce_node(key, reducer, root)
        # Case 3.
        leaf.children[leaf_ix] = val

        if not self.mutation:
            return self._create(root, length)
        else:
            self.root = root
            self.length = length
            return self

    def pop(self) -> "Vector":
        """There's 3.5 cases when popping, in order of initial possibility:
        1. The right-most leaf node has at least one element in it: we simply set it to None.

        2. The right-most leaf node is all "None"s after popping: we set this entire node to None.

        3. The current length is a power of WIDTH, therefore an entire branch needs trimming:
        we set the parent node, or previous leaf, equal to the left-most, or zeroth, child leaf.
        
        3a. If the length == WIDTH, we must set the root element equal to the left-most child, or prev_leaf.
            Denoted as an "a" case as reference semantics, not logic, force this special case.
        """
        root = Node(list(self.root.children)) if not self.mutation else self.root
        length = self.length - 1
        key = self.length - 1
        leaf_ix = key & MASK

        def reducer(nodes: Tuple[Node[T], Node[T]], level: int, ix: int):
            prev_node, node = nodes
            children = node.children[ix]

            node.children[ix] = children.copy() if not self.mutation else children

            # Case 2.
            # If we're at the last level and our index to pop is the zeroth one
            # we delete the entire branch. This is easier to detect inside the
            # reduction.
            if level == 1 and leaf_ix == 0:
                node.children[ix] = None
                return node, None
            else:
                return node, node.children[ix]

        prev_leaf, leaf = self._reduce_node(key, reducer, (root, root))

        # Case 1.
        if leaf is not None:
            leaf.children[leaf_ix] = None

        # Case 3.
        if is_power_of(self.length, WIDTH):
            prev_leaf = prev_leaf.children[0]

        # Case 3a.
        if self.length == WIDTH:
            root = prev_leaf

        if not self.mutation:
            return self._create(root, length)
        else:
            self.root = root
            self.length = length
            return self

    def copy(self) -> "Vector":
        out = self.append(None)
        return out.pop()

    def concat(self, *args: "Vector") -> "Vector":
        lists: List["Vector"] = list(args)
        base = self.copy() if not self.mutation else self
        mutation = self.mutation

        base.mutation = True
        for sub_list in lists:
            sub_list.for_each(lambda x, i: base.append(x))

        base.mutation = mutation

        return base

    def splice(self, start: int, vals: List[T]) -> "Vector":
        """Split the list into two halves, starting at `start`,
        then insert all values in `vals` into the middle. Finally,
        rejoin the three lists into one and return.
        """
        out_list: List[T] = []

        self.for_each(lambda x, i: out_list.append(x), 0, start)
        out_list += vals
        self.for_each(lambda x, i: out_list.append(x), start)

        return Vector(out_list)

    def slice(self, start: Optional[int] = None, end: Optional[int] = None) -> "Vector":
        """Slice the list into a section starting at `start` and ending at `end`.
        If start is None, return a copy.
        If end is None, end = self.length + 1.
        If end is < 0, end's value wraps around; end += self.length.
        """
        if start is None:
            return self.copy()
        else:
            out = self.copy()
            return out[start:end]

    def for_each(
        self, func: Callable[[T, int], Any], start: int = 0, end: Optional[int] = None,
    ) -> None:
        """Optimized iteration over the list: we save the leaf node value to reuse as long
        as we can, or until the current index & MASK == 0. Asymptotically equivalent to the
        naïve self.at loop, but more efficient in practice. 

        Args:
            func (Callable[[T, int], None]): callback that accepts:
            the current value,
            the current index?.
            start (int): starting position, defaults to 0.
            end (Optional[int]): ending position, defaults to self.length. If end < 0, end += self.length.

        """
        self.leaf = None
        end = self.length if end is None else end + self.length if end < 0 else end

        for i in range(start, end):
            leaf_ix = i & MASK

            if leaf_ix == 0 or self.leaf is None:
                curr_val: T = self._at(i)
                func(curr_val, i)
            else:
                curr_val = self.leaf.children[leaf_ix]
                func(curr_val, i)

    def reduce(self, func: Callable[[S, T], S], init: Optional[T] = None) -> S:
        start = 0

        if init is None:
            start = 1
            init = self._at(0)

        acc: S = cast(S, init)

        def _func(curr_val: T, i: int) -> None:
            nonlocal acc
            acc = func(acc, curr_val)

        self.for_each(_func, start)

        return acc


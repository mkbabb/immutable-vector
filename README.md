# `immutable-vector.py`

A typed and functional Python implementation of a series of immutable, or rather
_persistent_, data structures, namely: an immutable [`vector`](src/vector.py).

Based off of the wonderful work by Rich Hickey (`Clojure`'s Vector) and Phil Bagwell
([`Bagwell, Phil. (2001). Ideal Hash Trees.`](https://pdfs.semanticscholar.org/4fc2/40d0d9e690cb9b0bcb2f8a5e5ca918b01410.pdf))

## Features

#### ⌨️ Typing

Typed and statically analyzed using `mypy`, allowing for better syntax highlighting,
code completion, and of course, compile-time error checking. Coded in idiomatic, modern
Python.

#### 🛠 Functional

Implements functional array interfaces similar to that of `JavaScript`. Thus, we strive
to be _relatively_ complient to the Array prototype standards set forth by EMCA: see the
spec [here](https://www.ecma-international.org/ecma-262/5.1/#sec-15.4) and a great MDN
article here
[here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#instance_methods)

#### (soon to be) ⚡️Fast

Utilizes a
[hash array mapped trie](https://en.wikipedia.org/wiki/Hash_array_mapped_trie) data
structure for competitive performance when compared to a typical contiguous array
implementation.

_soon to be_ qualifier, as a future goal is to provide Python bindings to a
re-implemented C API hereof.

## Technical Details

TODO

## Benchmarks

TODO

## Further Reading

Of course, the paper by Phil Bagwell cited at the beginning is great, but I used many
other resources along the way. Here's a collection (in no particular order) of articles,
videos, and other projects of a similar kind, that I found useful:

### Articles:

-   [Wonderful series of articles explaining Clojure's Vector implementation](https://hypirion.com/musings/understanding-persistent-vector-pt-1)

### Videos:

-   [CppCon 2017: Juan Pedro Bolivar Puente “Postmodern immutable data structures”](https://www.youtube.com/watch?v=sPhpelUfu8Q)
-   [CppCon 2017: Phil Nash “The Holy Grail! A Hash Array Mapped Trie for C++”](https://www.youtube.com/watch?v=imrSQ82dYns)

### Projects:

-   [Clojure's Vector implementation](https://github.com/clojure/clojure/blob/0b73494c3c855e54b1da591eeb687f24f608f346/src/jvm/clojure/lang/PersistentVector.java)
-   The fantastic [`immer`](https://github.com/arximboldi/immer)

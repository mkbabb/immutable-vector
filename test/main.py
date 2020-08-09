from immutable_vector import Vector


if __name__ == "__main__":
    items = [0, 1, 2, 3, 4, 5]

    v0 = Vector(items)
    v1 = v0.splice(1, [99])

    total = v1.reduce(lambda x, y: x + y)

    # l0 = Vector(list(range(5)))
    # l1 = Vector(list(range(18, 18 * 2)))

    # l3 = l0.splice(1, [99])

    # for i in range(l3.size):
    #     print(l3.at(i))

    # l1 = l0.pop()
    # l2 = l0.pop()

    # for i in range(l1.size):
    #     t1, child1 = l1.at(i)
    #     t2, child2 = l2.at(i)

    #     print(t1, id(child1) == id(child2))

    # print("o")

_at
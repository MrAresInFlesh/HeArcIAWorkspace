import time
import State
import Viewer

"""
Main file to test the taquin problem and the algorithm to
solve it.
Author : Simon Meier, INF3 dlm-a
"""


def result(v1, v2):
    """
    """
    print("\n-----------------------------")
    print("border : {}".format(len(v1)))
    print("history: {}".format(len(v2)))
    return None


def search(init, final, show_it=True):
    """

    """
    brd = [init]
    history = set()
    show_limit = 20
    if show_it:
        print("Iterations (history length) :")
        print("-----------------------------")
    while brd:
        st = brd.pop()
        history.add(st)
        if st.final(final):
            result(brd, history)
            return st
        opers = st.applicableOps()
        for op in opers:
            new_state = st
            if (new_state not in history) and new_state.legal():
                brd.append(new_state)
        if show_it:
            print("|" + "{}".format(len(history)), end='')
            if (len(history) % show_limit) == 19:
                print('')
    return None


def g(values, goal):
    """
    BRIEF :
        calculate the number of wrong placed numbers
        in the taquin.
    RETURN : int
    """
    _heuristic1 = 0
    for k, v in zip(values, goal):
        for element1, element2 in zip(k, v):
            if element1 != element2:
                _heuristic1 += 1
    return int(_heuristic1)


def h(values, goal):
    """
    BRIEF:
        calculate the manhattan distance that each
        numbers has from its goal.
    RETURN : int
    """
    _h = 0
    for v, line in enumerate(goal):
        for k, e in enumerate(line):
            if e != 0:
                position = State.State.search_x(values, e)
                _h += abs(position[0] - v) + abs(position[1] - k)
    return _h


def astar(init, final, heuristic):
    brd = {init: (0, heuristic)}
    history = {}

    # f(n) = g(n) + h(n)
    # g(n) = number of step (less expensive path)
    # h(n) = number of wrong placed numbers (heuristic of the next step)

    while brd:
        _state = list(brd.keys())[0]
        f_state, g_state, = brd[_state]
        brd.pop(_state)

        if _state.final(final):
            result(brd, history)
            return _state

        ops = _state.applicableOps()

        for op in ops:
            new = _state.apply(op)
            g = g_state + 1

            # calculate f
            f = g_state + h(new.values, final)
            _f = f
            if new not in brd:
                brd[new] = [f, g]

            if new in brd or new in history:
                if (new in brd and brd[new][1] > g) or (new in history and history[new][1] > g):
                    brd[new] = [f, g]

        brd = {k: v for k, v in sorted(brd.items(), key=lambda item: item[1][0])}
        history[_state] = [f_state, g_state]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # few iterations
    taquin_easy = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    # about few hundred iterations
    taquin_medium = [
        [0, 1, 2],
        [7, 4, 3],
        [5, 8, 6]
    ]

    # about 140'000 iterations
    taquin_hard = [
        [4, 0, 2],
        [3, 5, 1],
        [6, 7, 8]
    ]

    taquin_impossible = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]

    final_values = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    init_state = taquin_hard

    start = time.time()
    result = astar(State.State(init_state), final_values, h(init_state, final_values))

    if result is not None:
        print("Solution found!")
        print("h = ", h(init_state, final_values))
        print(f"Execution time: {time.time() - start} seconds")

        winning_path = []
        while result.parent is not None:
            winning_path.insert(0, result)
            result = result.parent
        winning_path.insert(0, result)
        with Viewer.TaquinViewerHTML('example.html') as viewer:
            for i, state in enumerate(winning_path):
                viewer.add_taquin_state(state.values, title=i)
    else:
        print("Solution not found!!")

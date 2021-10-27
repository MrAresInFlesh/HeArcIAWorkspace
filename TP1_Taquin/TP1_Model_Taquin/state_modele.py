class State(object):

    def __init__(self, values, parent=None):
        self.values = values
        self.parent = parent

    def legal(self):
        return True

    def final(self, final_values):
        return self.values == final_values

    def __hash__(self):
        return str(self).__hash__()

    def __str__(self):
        return str(self.values)

    def __eq__(self, other):
        return self.values == other.values

    @staticmethod
    def swap(values, x1, y1, x2, y2):
        pass
        # swap two cases in the plate of the puzzle
        # hint: a deepcopy is needed

    def applicable_operators(self):
        #list of new values after the application of possible operators
        pass

    def apply(self, op):
        return State(op, self)

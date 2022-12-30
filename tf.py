"""file for TF class"""

class TF:
    """basically an enum + dictionary for True/False/None"""

    def __init__(self):
        self._t: int = 0
        self._f: int = 0
        self._n: int = 0

    @property
    def trues(self) -> int:
        return self._t

    @property
    def falses(self) -> int:
        return self._f

    @property
    def nones(self) -> int:
        return self._n

    def incr_t(self, increment_by=1) -> None:
        self._t += increment_by

    def incr_f(self, increment_by=1) -> None:
        self._f += increment_by

    def incr_n(self, increment_by=1) -> None:
        self._n += increment_by


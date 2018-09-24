import datetime
import random
import typing
import unittest
from collections import OrderedDict


class Passage:
    def __init__(self, aos: datetime.datetime):
        self.aos = aos


class PassagesByDay:
    def __init__(self):
        self.passages = []
        self._sorted = True

    def add_passage(self, passage: Passage):
        self.passages.append(passage)
        self._sorted = False

    def get_passages_after(self, day: datetime.date) -> typing.Iterable[Passage]:
        if not self._sorted:
            self.passages.sort(key=lambda d: d.aos)
            self._sorted = True

        dt = datetime.datetime(day.year, day.month, day.day)
        start_position = self._rec_find_start_position(dt, 0, len(self.passages) - 1)
        if start_position < 0:
            return
        for i in range(start_position, len(self.passages)):
            yield self.passages[i]

    def get_passages_by_day(self, day: datetime.date) -> typing.Dict[datetime.date, typing.List[Passage]]:
        result = OrderedDict()
        for passage in self.get_passages_after(day):
            cur_day = passage.aos.date()
            assert cur_day >= day
            result.setdefault(cur_day, []).append(passage)
        return result

    def _rec_find_start_position(self, dt: datetime.datetime, start_idx: int, end_idx: int):
        if end_idx - start_idx <= 1:
            return start_idx if self.passages[start_idx].aos == dt else end_idx
        mid = (start_idx + end_idx) // 2
        if self.passages[start_idx].aos <= dt <= self.passages[mid].aos:
            return self._rec_find_start_position(dt, start_idx, mid)
        if self.passages[mid].aos <= dt <= self.passages[end_idx].aos:
            return self._rec_find_start_position(dt, mid, end_idx)
        return -1


class Test(unittest.TestCase):
    _NUM_DAYS_AFTER = 100

    def setUp(self):
        self.start_ts = int(datetime.datetime.utcnow().timestamp() * 1000)
        step = 3600000 * 24
        self.passages = [
            Passage(datetime.datetime.fromtimestamp(t / 1000))
            for t in range(self.start_ts, self.start_ts + 365 * step, step)
            ]
        random.shuffle(self.passages)
        self.sut = PassagesByDay()
        for p in self.passages:
            self.sut.add_passage(p)
        self.day = \
            datetime.datetime.fromtimestamp(self.start_ts / 1000) + \
            datetime.timedelta(days=365 - self._NUM_DAYS_AFTER)
        self.day = self.day.date()

    def test_get_passages_after(self):
        passages = list(self.sut.get_passages_after(self.day))
        self.assertEqual(100, len(passages))

    def test_get_by_day(self):
        passages_by_day = self.sut.get_passages_by_day(self.day)
        self.assertEqual(100, len(passages_by_day))
        previous_day = None
        for cur_day, passages in passages_by_day.items():
            self.assertTrue(self.day <= cur_day)
            if previous_day is not None:
                self.assertEqual(cur_day, previous_day + datetime.timedelta(days=1))
            previous_day = cur_day
            for passage in passages:
                self.assertEqual(cur_day, passage.aos.date())

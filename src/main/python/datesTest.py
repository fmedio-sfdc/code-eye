import unittest
import dates
from dateutil import parser

class TestDates(unittest.TestCase):

    def test_get_clo(self):
        alldates = {'208': {'clo': parser.parse("2016/11/18")}, '210': {'clo': parser.parse("2017/3/31")}}
        cloDates = dates.get_clo_list(alldates)
        self.assertEqual(len(cloDates), 2)
        self.assertEqual(cloDates["date.main.208"], parser.parse("2016/11/18"))
        self.assertEqual(cloDates["date.main.210"], parser.parse("2017/3/31"))

    def test_read_dates(self):
        diffs = dates.get_date_diffs({'a':parser.parse('2016/12/30').date(), 'b':parser.parse('2017/1/2').date()}, '2017/1/1')
        self.assertEqual(diffs['date.a'], 2)
        self.assertEqual(diffs['date.b'], -1)

    labeledDates = {"d1":parser.parse("2018/2/6"), "d2":parser.parse("2018/2/7")}

    def test_1_day_before_first_date(self):
        (label, days) = dates.daysBefore("2018/2/5", TestDates.labeledDates)
        self.assertEqual(label, "d1")
        self.assertEqual(days.days, -1)

    def test_day_equals_second_date(self):
        (label, days) = dates.daysBefore("2018/2/7", TestDates.labeledDates)
        self.assertEqual(label, "d2")
        self.assertEqual(days.days, 0)

if __name__ == '__main__':
    unittest.main()


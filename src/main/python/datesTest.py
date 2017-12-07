import unittest
import dates
from dateutil import parser

class TestDates(unittest.TestCase):

    def test_read_dates(self):
        diffs = dates.get_date_diffs({'a':parser.parse('2016/12/30').date(), 'b':parser.parse('2017/1/2').date()}, '2017/1/1')
        self.assertEqual(diffs['a'], 2)
        self.assertEqual(diffs['b'], -1)

if __name__ == '__main__':
    unittest.main()


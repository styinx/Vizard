from unittest import main, TestCase
from source.data import Series


class SeriesTest(TestCase):
    def testAddValue(self):

        s = Series()
        s.add(1)
        self.assertEqual(s.values, {0: 1})


if __name__ == "__main__":
    main()

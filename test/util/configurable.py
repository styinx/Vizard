from unittest import main, TestCase

from source.util import Configurable


class ConfigurableTest(TestCase):
    def testSetItem(self):

        c = Configurable()
        c["name"] = "peter pan"
        self.assertEqual(c["name"], "peter pan")
        self.assertEqual(c.name, "peter pan")


if __name__ == "__main__":
    main()

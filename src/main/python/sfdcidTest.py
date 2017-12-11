import unittest
import sfdcid

class Testsfdcid(unittest.TestCase):

    def test_14_digit_gusId(self):
        self.assertEqual(sfdcid.to15('12345678901234'), '')

    def test_15_digit_gusId(self):
        self.assertEqual(sfdcid.to15('123456789012345'), '123456789012345')

    def test_16_digit_gusId(self):
        self.assertEqual(sfdcid.to15('1234567890123456'), '123456789012345')

    def test_19_digit_gusId(self):
        self.assertEqual(sfdcid.to15('1234567890123456789'), '123456789012345')

if __name__ == '__main__':
    unittest.main()


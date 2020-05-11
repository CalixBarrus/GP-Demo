import unittest

from gp_framework import report as rep


class TestReportModule(unittest.TestCase):
    def test_transpose_list_of_lists(self):
        input_list = [['a', 'b', 'c', 'd', 'e'], ['f', 'g', 'h', 'i', 'j'], ['k', 'l', 'm', 'n', 'o']]
        expected_output = [['a', 'f', 'k'], ['b', 'g', 'l'], ['c', 'h', 'm'], ['d', 'i', 'n'], ['e', 'j', 'o']]
        actual_output = rep._transpose_list_of_lists(input_list)
        self.assertEqual(actual_output, expected_output)

    def test_combine_list_elements_group_size_2(self):
        input_list = [i*2 for i in range(10)]
        expected_output = [1, 5, 9, 13, 17]
        actual_output = rep._combine_list_elements(input_list, 2)
        self.assertEqual(actual_output, expected_output)

    def test_combine_list_elements_group_size_3(self):
        input_list = [i for i in range(10)]
        expected_output = [1, 4, 7, 9]
        actual_output = rep._combine_list_elements(input_list, 3)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()

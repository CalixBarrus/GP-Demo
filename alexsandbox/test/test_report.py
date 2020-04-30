from alexsandbox import report as rep


def test_transpose_list_of_lists():
    input_list = [['a', 'b', 'c', 'd', 'e'], ['f', 'g', 'h', 'i', 'j'], ['k', 'l', 'm', 'n', 'o']]
    expected_output = [['a', 'f', 'k'], ['b', 'g', 'l'], ['c', 'h', 'm'], ['d', 'i', 'n'], ['e', 'j', 'o']]
    actual_output = rep.transpose_list_of_lists(input_list)
    assert actual_output == expected_output


def test_combine_list_elements_group_size_2():
    input_list = [i*2 for i in range(10)]
    expected_output = [1, 5, 9, 13, 17]
    actual_output = rep.combine_list_elements(input_list, 2)
    assert actual_output == expected_output


def test_combine_list_elements_group_size_3():
    input_list = [i for i in range(10)]
    expected_output = [1, 4, 7, 9]
    actual_output = rep.combine_list_elements(input_list, 3)
    assert actual_output == expected_output
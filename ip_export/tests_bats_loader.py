from hamcrest import assert_that, equal_to
from unittest import TestCase

from bats_loader import MyList, get_time


class TestMyList(TestCase):
    def test_empty_list(self):
        # GIVEN
        my_list = MyList()

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to('[]'))

    def test_to_str_empty(self):
        # GIVEN
        my_list = MyList()

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to('[]'))

    def test_to_str_1_element(self):
        # GIVEN
        my_list = MyList()
        my_list.append(100)

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to('[0x64]'))

    def test_to_str_leading_zeroes(self):
        # GIVEN
        my_list = MyList()
        my_list.from_bytearray([ 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9] )

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to(
            """[0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08 0x09]"""))

    def test_append_and_prepend(self):
        # GIVEN
        my_list = MyList()

        # WHEN
        my_list.append(5)
        my_list.append_list([6, 7, 8, 9])
        my_list.prepend_list([1, 2, 3, 4])

        # THEN
        assert_that(my_list.to_str(no_x=True), equal_to(
            "[01 02 03 04 05 06 07 08 09]"))

class TestTime(TestCase):
    def test_get_time(self):
        # GIVEN
        time_in_s = 34_200
        my_list = MyList();

        # WHEN
        get_time(time_in_s, my_list);

        # THEN
        assert_that(my_list.get_length(), equal_to(6))
        assert_that(my_list.to_str(no_x=True), equal_to(
            "[06 20 98 85 00 00]"))

class TestSeqUnitHdr(TestCase):
    def test_get_seq_unit_hdr(self):
        # GIVEN
        out_list = MyList()

        time_in_s = 34_200
        time_msg = get_time(time_in_s, out_list)

        # WHEN
        # Can I append all of the arrays?
        # THEN

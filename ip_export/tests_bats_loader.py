from hamcrest import assert_that, equal_to, has_length
from unittest import TestCase

from bats_loader import MyList, get_time, get_seq_unit_hdr


class TestMyList(TestCase):
    def test_empty_list(self):
        # GIVEN
        my_list = MyList()

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to("[]"))

    def test_to_str_empty(self):
        # GIVEN
        my_list = MyList()

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to("[]"))

    def test_to_str_1_element(self):
        # GIVEN
        my_list = MyList()
        my_list.append(100)

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(to_str, equal_to("[0x64]"))

    def test_to_str_leading_zeroes(self):
        # GIVEN
        my_list = MyList()
        my_list.from_array([0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9])

        # WHEN
        to_str = my_list.to_str()

        # THEN
        assert_that(
            to_str, equal_to("""[0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08 0x09]""")
        )

    def test_append_and_prepend(self):
        # GIVEN
        my_list = MyList()

        # WHEN
        my_list.append(5)
        my_list.append_list([6, 7, 8, 9])
        my_list.prepend_list([1, 2, 3, 4])

        # THEN
        assert_that(my_list.to_str(no_x=True), equal_to("[01 02 03 04 05 06 07 08 09]"))

    def test_get_word_below_8(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([0xab, 0xcd, 0xef, 0x19])

        # WHEN
        word = my_list.get_word(0)
        num_words = my_list.get_num_words()

        # THEN
        print(f'word: {hex(word)}')
        print(f'num_words: {num_words}')
        assert_that(word, equal_to(0xabcdef1900000000))


class TestTime(TestCase):
    def test_get_time(self):
        # GIVEN
        time_in_s = 34_200
        my_list = MyList()

        # WHEN
        get_time(time_in_s, my_list)

        # THEN
        assert_that(my_list.get_length(), equal_to(6))
        assert_that(my_list.to_str(no_x=True), equal_to("[06 20 98 85 00 00]"))


class TestSeqUnitHdr(TestCase):
    def test_get_seq_unit_hdr_1_Time(self):
        # GIVEN
        out_list = MyList()
        time_in_s = 34_200

        # WHEN
        time_msg = get_time(time_in_s, out_list)
        seq_unit_hdr = get_seq_unit_hdr(hdr_seq=1, hdr_count=1, msgs_array=out_list)

        # THEN
        assert_that(seq_unit_hdr, equal_to(0))
        assert_that(out_list.to_array(), has_length(14))
        assert_that(
            out_list.to_str(),
            equal_to(
                "[0x0E 0x00 0x02 0x01 0x01 0x00 0x00 0x00 0x06 0x20 0x98 0x85 0x00 0x00]"
            ),
        )
        assert_that(
            out_list.to_array(),
            equal_to([0xE, 0, 0x2, 0x1, 0x1, 0x0, 0x0, 0x0, 0x6, 0x20, 152, 133, 0, 0]),
        )

    def test_get_seq_unit_hdr_Time_AddOrder(self):
        # GIVEN
        out_list = MyList()
        time_in_s = 34_199

        # WHEN
        time_msg = get_time(time_in_s, out_list)
        seq_unit_hdr = get_seq_unit_hdr(hdr_seq=1, hdr_count=1, msgs_array=out_list)

        # THEN
        assert_that(seq_unit_hdr, equal_to(0))
        assert_that(out_list.to_array(), has_length(14))
        assert_that(
            out_list.to_str(),
            equal_to(
                "[0x0E 0x00 0x02 0x01 0x01 0x00 0x00 0x00 0x06 0x20 0x97 0x85 0x00 0x00]"
            ),
        )
        assert_that(out_list.get_word(1), equal_to(0xE00020101000000))

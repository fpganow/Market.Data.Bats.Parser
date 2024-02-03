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


    def test_get_num_words_len_0(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()

        # THEN
        assert_that(my_list_len, equal_to(0))
        assert_that(is_aligned, equal_to(True))


    def test_get_num_words_len_1(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([0x1])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()
        my_word = my_list.get_word(0)
        byte_enables = my_list.get_byte_enables(0)

        # THEN
        assert_that(my_list_len, equal_to(1))
        assert_that(is_aligned, equal_to(False))
        assert_that(my_word, equal_to(0x0100_0000_0000_0000))
        assert_that(byte_enables, equal_to(0b1000_0000))


    def test_get_num_words_len_7(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()
        my_word = my_list.get_word(0)
        byte_enables = my_list.get_byte_enables(0)

        # THEN
        assert_that(my_list_len, equal_to(1))
        assert_that(is_aligned, equal_to(False))
        assert_that(my_word, equal_to(0x0102_0304_0506_0700))
        assert_that(byte_enables, equal_to(0b1111_1110))


    def test_get_num_words_len_8(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()
        my_word = my_list.get_word(0)
        byte_enables = my_list.get_byte_enables(0)

        # THEN
        assert_that(my_list_len, equal_to(1))
        assert_that(is_aligned, equal_to(True))
        assert_that(my_word, equal_to(0x0102_0304_0506_0708))
        assert_that(byte_enables, equal_to(0b1111_1111))


    def test_get_num_words_len_16(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([
            0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8,
            0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10
            ])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()

        word_1 = my_list.get_word(0)
        byte_enables_1 = my_list.get_byte_enables(0)

        word_1 = my_list.get_word(1)
        byte_enables_2 = my_list.get_byte_enables(0)

        # THEN
        assert_that(my_list_len, equal_to(2))
        assert_that(is_aligned, equal_to(True))

        assert_that(word_1, equal_to(0x0102_0304_0506_0708))

        assert_that(word_2, equal_to(0x090a_0b0c_0d0e_0f10))


    def test_get_num_words_len_32(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([
             0x1,  0x2,  0x3,  0x4,  0x5,  0x6,  0x7,  0x8,
             0x9,  0xa,  0xb,  0xc,  0xd,  0xe,  0xf, 0x10,
            0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
            0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20,
            ])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()
        first_word = my_list.get_word(0)
        first_word_byte_enables = my_list.get_byte_enables(0)
        last_word = my_list.get_word(3)
        last_word_byte_enables = my_list.get_byte_enables(0)

        # THEN
        assert_that(my_list_len, equal_to(4))
        assert_that(is_aligned, equal_to(True))
        assert_that(first_word, equal_to(0x0102_0304_0506_0708))
        assert_that(last_word, equal_to(0x191a_1b1c_1d1e_1f20))


    def test_get_num_words_len_27(self):
        # GIVEN
        my_list = MyList()
        my_list.append_list([
             0x1,  0x2,  0x3,  0x4,  0x5,  0x6,  0x7,  0x8,
             0x9,  0xa,  0xb,  0xc,  0xd,  0xe,  0xf, 0x10,
            0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
            0x19, 0x1a, 0x1b
            ])

        # WHEN
        my_list_len = my_list.get_num_words()
        is_aligned = my_list.is_aligned()
        first_word = my_list.get_word(0)
        last_word = my_list.get_word(3)

        # THEN
        assert_that(my_list_len, equal_to(4))
        assert_that(is_aligned, equal_to(False))
        assert_that(first_word, equal_to(0x0102_0304_0506_0708))
        assert_that(last_word, equal_to(0x191a_1b00_0000_0000))


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
        assert_that(out_list.get_word(0), equal_to(0x0e00_0201_0100_0000))
        assert_that(out_list.get_word(1), equal_to(0x0620_9785_0000_0000))

from hamcrest import assert_that, equal_to, has_length, instance_of
from unittest import TestCase

from bats_loader import (
    MyList,
    get_seq_unit_hdr,
    get_time,
    get_add_order_long, get_add_order_short, get_add_order_expanded,
    get_order_executed, get_order_executed_at_price_size,
    get_reduce_size_long, get_reduce_size_short,
    get_modify_order_long, get_modify_order_short,
    get_delete_order,
    get_trade_long, get_trade_short, get_trade_expanded
)
from cboe_pitch.time import Time
from cboe_pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from cboe_pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from cboe_pitch.message_factory import MessageFactory


def dump_bytes(msg_bytes):
    bytes_copy = msg_bytes.copy()
    slick = None
    while len(bytes_copy) > 0:
        slick = bytes_copy[0:8]
        line_str = ', '.join([f'{x:#04x}' for x in slick])
        print(f'\t{line_str}, ')
        bytes_copy = bytes_copy[8:]


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

        word_2 = my_list.get_word(1)
        byte_enables_2 = my_list.get_byte_enables(0)

        # THEN
        assert_that(my_list_len, equal_to(2))
        assert_that(is_aligned, equal_to(True))

        assert_that(word_1, equal_to(0x0102_0304_0506_0708))
        assert_that(byte_enables_1, equal_to(0b1111_1111))

        assert_that(word_2, equal_to(0x090a_0b0c_0d0e_0f10))
        assert_that(byte_enables_2, equal_to(0b1111_1111))


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
        first_word_be = my_list.get_byte_enables(0)

        last_word = my_list.get_word(3)
        last_word_be = my_list.get_byte_enables(3)

        # THEN
        assert_that(my_list_len, equal_to(4))
        assert_that(is_aligned, equal_to(True))

        assert_that(first_word, equal_to(0x0102_0304_0506_0708))
        assert_that(first_word_be, equal_to(0b1111_1111))

        assert_that(last_word, equal_to(0x191a_1b1c_1d1e_1f20))
        assert_that(last_word_be, equal_to(0b1111_1111))


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
        first_word_be = my_list.get_byte_enables(0)

        last_word = my_list.get_word(3)
        last_word_be = my_list.get_byte_enables(3)

        # THEN
        assert_that(my_list_len, equal_to(4))
        assert_that(is_aligned, equal_to(False))

        assert_that(first_word, equal_to(0x0102_0304_0506_0708))
        assert_that(first_word_be, equal_to(0b1111_1111))

        assert_that(last_word, equal_to(0x191a_1b00_0000_0000))
        assert_that(first_word_be, equal_to(0b1111_1111))


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

        # AGAIN
        parsed_msg = MessageFactory.from_bytes(my_list.to_bytearray())
        assert_that(parsed_msg, instance_of(Time))
        assert_that(parsed_msg.time(), equal_to(34_200))


class TestAddOrder(TestCase):
    def test_get_add_order_long_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        side_indicator = "B"
        quantity = 95_000
        symbol = "AAPL"
        price = 0.905

        my_list = MyList()

        # WHEN
        msg_bytes = get_add_order_long(time_offset=time_offset,
                                       order_id=order_id,
                                       side_indicator=side_indicator,
                                       quantity=quantity,
                                       symbol=symbol,
                                       price=price,
                                       out_list=my_list)

        # THEN
        assert_that(my_list.get_length(), equal_to(34))
        assert_that(my_list.to_array(), equal_to([
            0x22, 0x21, 0xe0, 0xab,  0x0,  0x0, 0x4f, 0x52, 
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x42, 0x18,
            0x73,  0x1,  0x0, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x5a, 0x23,  0x0,  0x0,  0x0,  0x0,  0x0, 
            0x0, 0x1]))

        # AGAIN
        parsed_msg = MessageFactory.from_bytes(my_list.to_bytearray())
        assert_that(parsed_msg, instance_of(AddOrderLong))
        assert_that(parsed_msg.time_offset(), equal_to(44_000))
        assert_that(parsed_msg.order_id(), equal_to("ORID0001"))
        assert_that(parsed_msg.side(), equal_to("B"))
        assert_that(parsed_msg.quantity(), equal_to(95_000))
        assert_that(parsed_msg.symbol(), equal_to("AAPL"))
        assert_that(parsed_msg.price(), equal_to(0.905))


    def test_get_add_order_short_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        side_indicator = "B"
        quantity = 20_000
        symbol = "AAPL"
        price = 1.95

        my_list = MyList()

        # WHEN
        msg_bytes = get_add_order_short(time_offset=time_offset,
                                       order_id=order_id,
                                       side_indicator=side_indicator,
                                       quantity=quantity,
                                       symbol=symbol,
                                       price=price,
                                       out_list=my_list)

        # THEN
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x22, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x42, 0x20,
            0x4e, 0x41, 0x41, 0x50, 0x4c, 0x20, 0x20, 0xc3,
            0x00, 0x01
            ]))

        # AGAIN
        parsed_msg = MessageFactory.from_bytes(my_list.to_bytearray())
        assert_that(parsed_msg, instance_of(AddOrderShort))
        assert_that(parsed_msg.time_offset(), equal_to(44_000))
        assert_that(parsed_msg.order_id(), equal_to("ORID0001"))
        assert_that(parsed_msg.side(), equal_to("B"))
        assert_that(parsed_msg.quantity(), equal_to(20_000))
        assert_that(parsed_msg.symbol(), equal_to("AAPL"))
        assert_that(parsed_msg.price(), equal_to(1.95))


    def test_get_add_order_expanded_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        side_indicator = "B"
        quantity = 95_000
        symbol = "AAPL"
        price = 0.905
        customer_indicator = "C"
        participant_id = "MPID"

        my_list = MyList()

        # WHEN
        msg_bytes = get_add_order_expanded(time_offset=time_offset,
                                       order_id=order_id,
                                       side_indicator=side_indicator,
                                       quantity=quantity,
                                       symbol=symbol,
                                       price=price,
                                       customer_indicator=customer_indicator,
                                       participant_id=participant_id,
                                       out_list=my_list)

        # THEN
        assert_that(my_list.get_length(), equal_to(41))
        assert_that(my_list.to_array(), equal_to([
            0x29, 0x2f, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x42, 0x18,
            0x73, 0x01, 0x00, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x20, 0x20, 0x5a, 0x23, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0x4d, 0x50, 0x49, 0x44,
            0x43,
        ]))

        # AGAIN
        parsed_msg = MessageFactory.from_bytes(my_list.to_bytearray())
        assert_that(parsed_msg, instance_of(AddOrderExpanded))
        assert_that(parsed_msg.time_offset(), equal_to(44_000))
        assert_that(parsed_msg.order_id(), equal_to("ORID0001"))
        assert_that(parsed_msg.side(), equal_to("B"))
        assert_that(parsed_msg.quantity(), equal_to(95_000))
        assert_that(parsed_msg.symbol(), equal_to("AAPL"))
        assert_that(parsed_msg.price(), equal_to(0.905))


class TestOrderExecuted(TestCase):
    def test_order_executed_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        executed_quantity = 95_000
        execution_id = "EXEI0001"

        my_list = MyList()

        # WHEN
        msg_bytes = get_order_executed(time_offset=time_offset,
                                       order_id=order_id,
                                       executed_quantity=executed_quantity,
                                       execution_id=execution_id,
                                       out_list=my_list)

        # THEN
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x18, 0x73,
            0x01, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))

        # AGAIN
        parsed_msg = MessageFactory.from_bytes(my_list.to_bytearray())
        assert_that(parsed_msg, instance_of(OrderExecuted))
        assert_that(parsed_msg.time_offset(), equal_to(44_000))
        assert_that(parsed_msg.order_id(), equal_to("ORID0001"))
        assert_that(parsed_msg.executed_quantity(), equal_to(95_000))
        assert_that(parsed_msg.execution_id(), equal_to("EXEI0001"))


    def test_order_executed_at_price_size_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        executed_quantity = 50
        remaining_quantity = 150
        price = 95.09
        execution_id = "EXEI0001"

        my_list = MyList()

        # WHEN
        msg_bytes = get_order_executed_at_price_size(time_offset=time_offset,
                                                     order_id=order_id,
                                                     executed_quantity=executed_quantity,
                                                     remaining_quantity=remaining_quantity,
                                                     execution_id=execution_id,
                                                     price=price,
                                                     out_list=my_list)

        # THEN
        dump_bytes(my_list.to_bytearray())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))

        # AGAIN
        parsed_msg = MessageFactory.from_bytes(my_list.to_bytearray())
        assert_that(parsed_msg, instance_of(OrderExecutedAtPriceSize))
        assert_that(parsed_msg.time_offset(), equal_to(44_000))
        assert_that(parsed_msg.order_id(), equal_to("ORID0001"))
        assert_that(parsed_msg.executed_quantity(), equal_to(95_000))
        assert_that(parsed_msg.execution_id(), equal_to("EXEI0001"))


class TestReduceSize(TestCase):
    def test_reduce_size_long_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        canceled_quantity = 50

        my_list = MyList()

        # WHEN
        msg_bytes = get_reduce_size_long(time_offset=time_offset,
                                         order_id=order_id,
                                         canceled_quantity=canceled_quantity,
                                         out_list=my_list)

        # THEN
        dump_bytes(my_list.to_bytearray())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))

    def test_reduce_size_short_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        canceled_quantity = 150

        my_list = MyList()

        # WHEN
        msg_bytes = get_reduce_size_short(time_offset=time_offset,
                                          order_id=order_id,
                                          canceled_quantity=canceled_quantity,
                                          out_list=my_list)

        # THEN
        dump_bytes(my_list.to_bytearray())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))


class TestModifyOrder(TestCase):
    def test_modify_order_long_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        quantity = 150
        price = 150.25

        my_list = MyList()

        # WHEN
        msg_bytes = get_modify_order_long(time_offset=time_offset,
                                          order_id=order_id,
                                          quantity=quantity,
                                          price=price,
                                          out_list=my_list)

        # THEN
        dump_bytes(my_list.to_array())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))

    def test_modify_order_short_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        quantity = 150
        price = 150.25

        my_list = MyList()

        # WHEN
        msg_bytes = get_modify_order_short(time_offset=time_offset,
                                          order_id=order_id,
                                          quantity=quantity,
                                          price=price,
                                          out_list=my_list)

        # THEN
        dump_bytes(my_list.to_array())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))


class TestDeleteOrder(TestCase):
    def test_delete_order_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"

        my_list = MyList()

        # WHEN
        msg_bytes = get_delete_order(time_offset=time_offset,
                                     order_id=order_id,
                                     out_list=my_list)

        # THEN
        dump_bytes(my_list.to_array())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))


class TestTrade(TestCase):
    def test_trade_long_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        side_indicator = "B"
        quantity = 150
        symbol = "AAPL"
        price = 0.905
        execution_id = "EXEI0001"

        my_list = MyList()

        # WHEN
        msg_bytes = get_trade_long(time_offset=time_offset,
                                     order_id=order_id,
                                     side_indicator=side_indicator,
                                     quantity=quantity,
                                     symbol=symbol,
                                     price=price,
                                     execution_id=execution_id,
                                     out_list=my_list)

        # THEN
        dump_bytes(my_list.to_array())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))

    def test_trade_short_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        side_indicator = "B"
        quantity = 150
        symbol = "AAPL"
        price = 0.905
        execution_id = "EXEI0001"

        my_list = MyList()

        # WHEN
        msg_bytes = get_trade_short(time_offset=time_offset,
                                    order_id=order_id,
                                    side_indicator=side_indicator,
                                    quantity=quantity,
                                    symbol=symbol,
                                    price=price,
                                    execution_id=execution_id,
                                    out_list=my_list)

        # THEN
        dump_bytes(my_list.to_array())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))

    def test_trade_expanded_create(self):
        # GIVEN
        time_offset = 44_000
        order_id = "ORID0001"
        side_indicator = "B"
        quantity = 150
        symbol = "AAPL"
        price = 0.905
        execution_id = "EXEI0001"

        my_list = MyList()

        # WHEN
        msg_bytes = get_trade_expanded(time_offset=time_offset,
                                       order_id=order_id,
                                       side_indicator=side_indicator,
                                       quantity=quantity,
                                       symbol=symbol,
                                       price=price,
                                       execution_id=execution_id,
                                       out_list=my_list)

        # THEN
        dump_bytes(my_list.to_array())
        assert_that(my_list.get_length(), equal_to(26))
        assert_that(my_list.to_array(), equal_to([
            0x1a, 0x23, 0xe0, 0xab, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x32, 0x00,
            0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x30, 0x30,
            0x30, 0x31]))


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

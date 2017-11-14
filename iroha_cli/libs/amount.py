from primitive_pb2 import Amount, uint256

UINT64_NUMBER = int(18446744073709551616)

def amount_to_int(amount):
    """
    Translater Protobuf Amount -> python int type
    Args:
        amount ( `Amount` ) : protobuf amount type ( don't care precision )
    Returns:
        int: int value equal to arg amount.
    """
    res = int(0)
    res += int(amount.value.first)
    res *= UINT64_NUMBER
    res += int(amount.value.second)
    res *= UINT64_NUMBER
    res += int(amount.value.third)
    res *= UINT64_NUMBER
    res += int(amount.value.fourth)
    return res


def int_to_amount(int_num,precision=0):
    """
    Translater python int type -> Protobuf Amount
    Args:
        int_num ( int ): integer amount value ( python supportes Multiple precision )
        precision (int): precision value ( if you are client-side, you don't care )
    Returns:
        `Amount`: protobuf Amount structure equal to int_num
    """
    value = uint256()
    value.fourth = int(int_num % UINT64_NUMBER)
    int_num //= UINT64_NUMBER
    value.third = int(int_num % UINT64_NUMBER)
    int_num //= UINT64_NUMBER
    value.second = int(int_num % UINT64_NUMBER)
    int_num //= UINT64_NUMBER
    value.first = int(int_num)
    return Amount(
        value = value,
        precision = precision
    )


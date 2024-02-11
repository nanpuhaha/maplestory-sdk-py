def korean_format_number(n: int) -> str:
    """정수를 한글 형식으로 포맷팅된 문자열로 변환합니다.

    Args:
        n (int): 포맷팅할 정수입니다.

    Returns:
        str: 정수의 한글 형식으로 포맷팅된 문자열입니다.

    Examples:
        >>> korean_format_number(12345)
        '1만 2345'

        >>> korean_format_number(27439263548400)
        '27조 4392억 6354만 8400'

    References:
        이 함수는 정수를 1만 단위로 나누어 한글 형식으로 포맷팅된 문자열로 변환합니다.
        사용되는 단위는 "만", "억", "조", "경"입니다.
    """

    units = ["", "만", "억", "조", "경"]
    result = []
    unit_index = 0

    while n > 0:
        # 10000으로 나눈 나머지를 구하여 현재 단위의 숫자를 얻습니다.
        part = n % 10000
        if part > 0:  # 현재 단위의 값이 0이 아닌 경우에만 결과에 추가합니다.
            result.insert(0, f"{part}{units[unit_index]}")
        n //= 10000  # 다음 단위로 넘어갑니다.
        unit_index += 1

    return " ".join(result) if result else "0"

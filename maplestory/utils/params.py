from typing import Any


def remove_none_values(d: dict[str, Any] | None) -> dict[str, Any] | None:
    return None if d is None else {k: v for k, v in d.items() if v is not None}


def every_element_contains(lis: list[str], key: str) -> bool:
    return all(key in v for v in lis if v is not None)


def every_element_not_contains(lis: list[str], key: str) -> bool:
    return all(key not in v for v in lis if v is not None)

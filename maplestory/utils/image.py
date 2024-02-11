import base64
from io import BytesIO

import httpx
from PIL import Image


def get_image_from_url(url: str) -> Image.Image:
    """
    지정된 URL에서 이미지를 검색하고 PIL Image 객체로 반환합니다.

    Args:
        url (str): 검색할 이미지의 URL.

    Returns:
        Image.Image: PIL Image 객체로 반환된 검색된 이미지.

    Examples:
        >>> from maplestory.utils.image import get_image
        >>> url = "https://example.com/image.jpg"
        >>> image = get_image(url)
        >>> image.show()
    """
    """
    Get an image from the given URL and return it as a PIL Image object.

    Parameters:
        url (str): The URL of the image to retrieve.

    Returns:
        Image.Image: The retrieved image as a PIL Image object.

    Raises:
        httpx.RequestError: If there is an error while making the HTTP request.
        PIL.UnidentifiedImageError: If the retrieved content is not a valid image.

    Example:
        >>> url = "https://example.com/image.jpg"
        >>> image = get_image(url)
    """
    res = httpx.get(url)
    return Image.open(BytesIO(res.content))


def get_image_from_base64str(base64_string: str) -> Image.Image:
    """
    지정된 base64 문자열에서 이미지를 검색하고 PIL Image 객체로 반환합니다.

    Args:
        base64_string (str): 검색할 이미지의 base64 문자열.

    Returns:
        Image.Image: PIL Image 객체로 반환된 검색된 이미지.

    Examples:
        >>> from maplestory.utils.image import get_image_from_base64str
        >>> base64_string = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABsElEQVRIS+2VvUoDQRSGv2k0E
    """

    return Image.open(BytesIO(base64.b64decode(base64_string)))

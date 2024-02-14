import httpx
import pytest
from PIL import Image, UnidentifiedImageError

from maplestory.utils.image import get_image_from_base64str, get_image_from_url


class TestGetImage:
    # Can retrieve a valid image from a valid URL
    def test_retrieve_valid_image_from_valid_url(self):
        url = "https://ssl.nexon.com/s2/game/maplestory/renewal/common/logo.png"
        image = get_image_from_url(url)
        assert isinstance(image, Image.Image)

    # Raises httpx.RequestError when given an invalid URL
    def test_raises_request_error_when_given_invalid_url(self):
        url = "invalid_url"
        with pytest.raises(httpx.RequestError):
            get_image_from_url(url)


class TestGetImageFromBase64str:

    # The function should be able to decode and return a valid image from a valid base64 string.
    def test_valid_base64_string(self):
        base64_string = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="
        result = get_image_from_base64str(base64_string)
        assert isinstance(result, Image.Image)

    # The function should raise a ValueError if the input string is not a valid base64 string.
    def test_invalid_base64_string(self):
        base64_string = "invalid_base64_string"
        with pytest.raises(ValueError):
            get_image_from_base64str(base64_string)

    # The function should raise a OSError if the input string is a valid base64 string but not a valid image.
    def test_valid_base64_string_invalid_image(self):
        base64_string = "bWFwbGVzdG9yeQ=="  # 'maplestory' in base64
        with pytest.raises(
            UnidentifiedImageError,
            match=r"cannot identify image file <_io.BytesIO object at 0x.*>",
        ):
            get_image_from_base64str(base64_string)

    # The function should raise a TypeError if the input string is not a string.
    def test_non_string_input(self):
        base64_string = 12345
        with pytest.raises(
            TypeError,
            match=r"argument should be a bytes-like object or ASCII string, not 'int'",
        ):
            get_image_from_base64str(base64_string)

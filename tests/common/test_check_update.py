from datetime import datetime
from pathlib import Path

import httpx
import pytest

from maplestory.check_update import (
    APIInformation,
    add_api_information_to_file,
    decode_url,
    main,
    retrieve_api_result,
)

YAML_FILE_URL = "https://raw.githubusercontent.com/nanpuhaha/maplestory-py/main/data/22_캐릭터_정보_조회.yaml"


class TestDecodeUrl:
    # Decodes a URL with no special characters
    def test_decodes_url_with_no_special_characters(self):
        # Arrange
        url = "http://www.example.com"

        # Act
        result = decode_url(url)

        # Assert
        assert result == "http://www.example.com"

    # Decodes a URL with special characters
    def test_decodes_url_with_special_characters(self):
        # Arrange
        url = "http%3A%2F%2Fwww.example.com%2Fpath%3Fparam%3Dvalue"

        # Act
        result = decode_url(url)

        # Assert
        assert result == "http://www.example.com/path?param=value"

    # Decodes a URL with multiple special characters
    def test_decodes_url_with_multiple_special_characters(self):
        # Arrange
        url = "http%3A%2F%2Fwww.example.com%2Fpath%3Fparam%3Dvalue%26key%3D%23"

        # Act
        result = decode_url(url)

        # Assert
        assert result == "http://www.example.com/path?param=value&key=#"

    # Decodes an empty URL
    def test_decodes_empty_url(self):
        # Arrange
        url = ""

        # Act
        result = decode_url(url)

        # Assert
        assert result == ""

    # Decodes a URL with only special characters
    def test_decodes_url_with_only_special_characters(self):
        # Arrange
        url = "%23%24%25%26%2B%2C%2F%3A%3B%3D%3F%40"

        # Act
        result = decode_url(url)

        # Assert
        assert result == "#$%&+,/:;=?@"

    def test_decodes_url_with_percent_encoding(self):
        # Arrange
        url = "http%3A%2F%2Fwww.example.com%2Fpath%3Fparam%3Dvalue%26key%3D%23%"

        # Act
        result = decode_url(url)

        # Assert
        assert result == "http://www.example.com/path?param=value&key=#%"


class TestAddApiInformationToFile:
    # The function successfully adds 'x-fileName', 'x-updateDate', and 'x-fileUrl' to a YAML file.
    def test_adds_x_fields_to_yaml_file(self):
        # Create a temporary YAML file
        temp_file = Path("./data/22_캐릭터_정보_조회.yaml")

        # Create an instance of APIInformation
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="path1",
            fileName="file1",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=1,
            createEmpName="name1",
            updateEmpNo=1,
            updateEmpName="name1",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )

        # Call the function under test
        add_api_information_to_file(temp_file, api_info)

        # Read the modified YAML file
        with open(temp_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if the x-fields are added correctly
        assert "x-fileName:" in content
        assert "x-updateDate:" in content
        assert "x-fileUrl:" in content

        # Delete the temporary YAML file
        temp_file.unlink()

    # The function correctly inserts the new lines just before the 'servers:' section.
    def test_inserts_lines_before_servers_section(self):
        # Create a temporary YAML file with 'servers:' section
        temp_file = Path("temp.yaml")
        temp_file.write_text("servers:\n")

        dt = datetime.now()

        # Create an instance of APIInformation
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="path1",
            fileName="file1",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=1,
            createEmpName="name1",
            updateEmpNo=1,
            updateEmpName="name1",
            createDate=dt,
            updateDate=dt,
            isVisible=True,
        )

        # Call the function under test
        add_api_information_to_file(temp_file, api_info)

        # Read the modified YAML file
        with open(temp_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check if the lines are inserted correctly
        assert lines[0] == "  x-fileName: file1\n"
        assert lines[1] == f"  x-updateDate: '{dt}'\n"
        assert lines[2].startswith("  x-fileUrl:")
        assert lines[3] == "servers:\n"

        # Delete the temporary YAML file
        temp_file.unlink()

    # The YAML file is empty.
    def test_empty_yaml_file(self):
        # Create a temporary empty YAML file
        temp_file = Path("temp.yaml")
        temp_file.touch()

        # Create an instance of APIInformation
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="path1",
            fileName="file1",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=1,
            createEmpName="name1",
            updateEmpNo=1,
            updateEmpName="name1",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )

        # Call the function under test
        add_api_information_to_file(temp_file, api_info)

        # Read the modified YAML file
        with open(temp_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if the x-fields are added correctly
        assert "  x-fileName: file1\n" in content
        assert "  x-updateDate:" in content
        assert "  x-fileUrl:" in content

        # Delete the temporary YAML file
        temp_file.unlink()

    # The YAML file does not contain the 'servers:' section.
    def test_missing_servers_section(self):
        # Create a temporary YAML file without 'servers:' section
        temp_file = Path("temp.yaml")
        temp_file.write_text("key: value\n")

        # Create an instance of APIInformation
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="path1",
            fileName="file1",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=1,
            createEmpName="name1",
            updateEmpNo=1,
            updateEmpName="name1",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )

        # Call the function under test and expect a ValueError
        with pytest.raises(ValueError):
            add_api_information_to_file(temp_file, api_info)

        # Delete the temporary YAML file
        temp_file.unlink()

    # The 'x-fileName', 'x-updateDate', and 'x-fileUrl' fields already exist in the YAML file.
    def test_existing_x_fields_in_yaml_file(self):
        # Create a temporary YAML file with existing x-fields
        temp_file = Path("temp.yaml")
        temp_file.write_text(
            "x-fileName: existing_file\n"
            "x-updateDate: '2021-01-01 00:00:00'\n"
            "x-fileUrl: 'existing_url'\n"
            "servers:\n"
        )

        dt = datetime(2024, 1, 1)

        # Create an instance of APIInformation
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="path1",
            fileName="file1",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=1,
            createEmpName="name1",
            updateEmpNo=1,
            updateEmpName="name1",
            createDate=dt,
            updateDate=dt,
            isVisible=True,
        )

        # Call the function under test
        add_api_information_to_file(temp_file, api_info)

        # Read the modified YAML file
        with open(temp_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if the existing x-fields are overwritten correctly
        assert "  x-fileName: file1\n" in content
        assert "  x-updateDate: '2024-01-01 00:00:00'\n" in content
        assert f"  x-fileUrl: '{YAML_FILE_URL}'\n" in content

        # Delete the temporary YAML file
        temp_file.unlink()

    # The function raises a ValueError if the 'servers:' section is not found in the YAML file.
    def test_missing_servers_section_error(self):
        # Create a temporary YAML file without 'servers:' section
        temp_file = Path("temp.yaml")
        temp_file.write_text("key: value\n")

        # Create an instance of APIInformation
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="path1",
            fileName="file1",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=1,
            createEmpName="name1",
            updateEmpNo=1,
            updateEmpName="name1",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )

        # Call the function under test and expect a ValueError
        with pytest.raises(ValueError):
            add_api_information_to_file(temp_file, api_info)

        # Delete the temporary YAML file
        temp_file.unlink()


class TestAPIInformation:
    # APIInformation instance can be created with valid input values
    def test_valid_input_values(self):
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="/path/to/file",
            fileName="file.yaml",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=123,
            createEmpName="John%20Doe",
            updateEmpNo=456,
            updateEmpName="Jane%20Smith",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )
        assert api_info.id == 1
        assert api_info.gameId == "game1"
        assert api_info.categoryName == "category1"
        assert api_info.filePath == "/path/to/file"
        assert api_info.fileName == "file.yaml"
        assert api_info.fileUrl == "http://example.com/file.yaml"
        assert api_info.ordering == 1
        assert api_info.createEmpNo == 123
        assert api_info.createEmpName == "John Doe"
        assert api_info.updateEmpNo == 456
        assert api_info.updateEmpName == "Jane%20Smith"
        assert isinstance(api_info.createDate, datetime)
        assert isinstance(api_info.updateDate, datetime)
        assert api_info.isVisible is True

    # The 'download' method downloads the API information to the given directory
    def test_download_method(self, tmp_path):
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="/path/to/file",
            fileName="file.yaml",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=123,
            createEmpName="John%20Doe",
            updateEmpNo=456,
            updateEmpName="Jane%20Smith",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )
        directory = tmp_path / "downloads"
        directory.mkdir()
        filepath = api_info.download(directory)
        assert filepath.exists()
        assert filepath.is_file()

    # The 'download' method adds 'x-fileName', 'x-updateDate', and 'x-fileUrl' to the downloaded YAML file
    def test_download_method_adds_metadata(self, tmp_path):
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="/path/to/file",
            fileName="file.yaml",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=123,
            createEmpName="John%20Doe",
            updateEmpNo=456,
            updateEmpName="Jane%20Smith",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )
        directory = tmp_path / "downloads"
        directory.mkdir()
        filepath = api_info.download(directory)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "x-fileName:" in content
        assert "x-updateDate:" in content
        assert "x-fileUrl:" in content

    # The 'download' method raises an exception if the file cannot be downloaded
    def test_download_method_raises_exception_on_failure(self, tmp_path, monkeypatch):
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="/path/to/file",
            fileName="file.yaml",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=123,
            createEmpName="John%20Doe",
            updateEmpNo=456,
            updateEmpName="Jane%20Smith",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )
        directory = tmp_path / "downloads"
        directory.mkdir()
        monkeypatch.delattr("httpx.get")
        with pytest.raises(Exception):
            api_info.download(directory)

    # The 'download' method raises an exception if the 'servers:' section is not found in the YAML file
    def test_download_method_raises_exception_if_servers_section_not_found(
        self, tmp_path
    ):
        api_info = APIInformation(
            id=1,
            gameId="game1",
            categoryName="category1",
            filePath="/path/to/file",
            fileName="file.yaml",
            fileUrl=YAML_FILE_URL,
            ordering=1,
            createEmpNo=123,
            createEmpName="John%20Doe",
            updateEmpNo=456,
            updateEmpName="Jane%20Smith",
            createDate=datetime.now(),
            updateDate=datetime.now(),
            isVisible=True,
        )
        directory = tmp_path / "downloads"
        directory.mkdir()
        filepath = directory / "file.yaml"
        filepath.touch()
        with pytest.raises(ValueError):
            api_info.download(directory)


class TestRetrieveApiResult:
    # Returns a dictionary when API call is successful.
    def test_returns_dictionary_when_api_call_is_successful(self):
        result = retrieve_api_result()
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    # Handles HTTP errors and raises an exception.
    def test_handles_http_errors_and_raises_exception(self):
        # Mock API_VERSION_URL
        API_VERSION_URL = "https://example.com/api"

        # Mock HTTP error response
        response = httpx.Response(404)

        # Mock httpx.get() method
        def mock_get(url):
            return response

        httpx.get = mock_get

        # Act and Assert
        with pytest.raises(Exception):
            retrieve_api_result()

    # Raises an exception when API call fails.
    def test_raises_exception_when_api_call_fails(self):
        # Mock API_VERSION_URL
        API_VERSION_URL = "https://example.com/api"

        # Mock connection error
        def mock_get(url):
            raise httpx.ConnectError()

        httpx.get = mock_get

        # Act and Assert
        with pytest.raises(Exception):
            retrieve_api_result()

    # Raises an exception when API result is not in the expected format.
    def test_raises_exception_when_api_result_not_in_expected_format(self):
        # Mock API_VERSION_URL
        API_VERSION_URL = "https://example.com/api"

        # Mock API response with invalid format
        response = httpx.Response(200, json={"invalid": "format"})

        # Mock httpx.get() method
        def mock_get(url):
            return response

        httpx.get = mock_get

        # Act and Assert
        with pytest.raises(Exception):
            retrieve_api_result()

    # Handles unexpected HTTP status codes and raises an exception.
    def test_handles_unexpected_http_status_codes_and_raises_exception(self):
        # Mock API_VERSION_URL
        API_VERSION_URL = "https://example.com/api"

        # Mock unexpected HTTP status code
        response = httpx.Response(500)

        # Mock httpx.get() method
        def mock_get(url):
            return response

        httpx.get = mock_get

        # Act and Assert
        with pytest.raises(Exception):
            retrieve_api_result()


class TestMain:
    # Fetches and prints local and web API information
    def test_fetch_and_print_api_information(self, capsys):
        main()

        captured = capsys.readouterr()
        assert "Local API Information" in captured.out
        assert "Web API Information" in captured.out
        assert "Local API Version == Web API Version: " in captured.out
        if "Local API Version == Web API Version: False" in captured.out:
            assert "Update Required" not in captured.out
            assert "Downloading updated yaml files..." not in captured.out
            assert "Updated files:" not in captured.out
            assert Path("updated_files.txt").is_file()

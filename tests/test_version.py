from importlib.metadata import PackageNotFoundError
from unittest.mock import MagicMock, patch

from pyvider._version import get_version


@patch("pyvider._version._find_project_root")
def test_get_version_from_file(mock_find_root):
    # Mock the return of _find_project_root to be a path-like object
    # with an existing VERSION file
    mock_path = MagicMock()
    mock_version_file = MagicMock()
    mock_version_file.exists.return_value = True
    mock_version_file.read_text.return_value = " 1.2.3 "
    mock_path.__truediv__.return_value = mock_version_file
    mock_find_root.return_value = mock_path

    assert get_version() == "1.2.3"
    mock_find_root.assert_called_once()
    mock_version_file.read_text.assert_called_once()


@patch("pyvider._version._find_project_root", return_value=None)
@patch("importlib.metadata.version", return_value="2.3.4")
def test_get_version_from_metadata(mock_version, mock_find_root):
    assert get_version() == "2.3.4"
    mock_find_root.assert_called_once()
    mock_version.assert_called_once_with("pyvider")


@patch("pyvider._version._find_project_root", return_value=None)
@patch("importlib.metadata.version", side_effect=PackageNotFoundError)
def test_get_version_fallback(mock_version, mock_find_root):
    assert get_version() == "0.0.0-dev"
    mock_find_root.assert_called_once()
    mock_version.assert_called_once_with("pyvider")

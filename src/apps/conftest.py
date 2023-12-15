import pytest


@pytest.fixture()
def mock_image_save(monkeypatch):
    """
    A pytest fixture that mocks the 'save' method of
    Django's FileSystemStorage. Used in tests to avoid actual
    image file creation.
    """

    def mock_save(_, name, *args, **kwargs):
        return f"path/to/{name}"

    monkeypatch.setattr(
        "django.core.files.storage.FileSystemStorage.save", mock_save
    )

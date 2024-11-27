import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock


@pytest.fixture
def mock_db():
    """Crea un objeto de sesión de base de datos simulado."""
    return MagicMock(spec=Session)
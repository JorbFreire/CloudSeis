import pytest
import unittest
from server.app.repositories.SeismicFileRepository import SeismicFileRepository

class TestSeismicFileRepository(unittest.TestCase):
  def test_if_is_class(self):
    assert callable(SeismicFileRepository.__init__)

  def test_happy_path(self):
    assert True

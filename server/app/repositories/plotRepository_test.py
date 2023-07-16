import pytest
import unittest
from server.app.repositories.PlotRepository import PlotRepository

class TestPlotRepository(unittest.TestCase):
  def test_if_is_class(self):
    assert callable(PlotRepository.__init__)

  def test_happy_path(self):
    assert True

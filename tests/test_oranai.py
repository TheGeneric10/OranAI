import unittest

from OranAI.core import OranAI, OranAIConfig


class TestOranAI(unittest.TestCase):
  def test_responds_with_prompt(self):
    ai = OranAI()
    response = ai.chat("Hello there")
    self.assertIn("OranAI", response)

  def test_sets_model(self):
    ai = OranAI(OranAIConfig(model="oran-0.7"))
    response = ai.chat("Give me a plan")
    self.assertIn("oran-0.7", response.lower())


if __name__ == "__main__":
  unittest.main()

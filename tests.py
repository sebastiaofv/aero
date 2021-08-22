from bs import Black_Scholes
import unittest

class TestBlackScholes(unittest.TestCase):

  def setUp(self):
    # Call
    self.bsc = Black_Scholes('c', 300, 250, 1, 0.03, 0.01, 0.15)
  
    # Put
    self.bsp = Black_Scholes('p', 300, 250, 1, 0.03, 0.01, 0.15)

  def test_d1(self):
    d1 = round(self.bsc.d1(), 3)
    self.assertEqual(d1, 1.424)
  
  def test_d2(self):
    d2 = round(self.bsc.d2(), 3)
    self.assertEqual(d2, 1.274)
 
  def test_put_price(self):
    price = round(self.bsp.option_price(), 3)
    self.assertEqual(price, 1.648)

  def test_call_price(self):
    price = round(self.bsc.option_price(), 3)
    self.assertEqual(price, 56.051)

  def test_delta_call(self):
    pass

  def test_delta_put(self):
    pass

  def test_gamma(self):
    pass

  def test_theta_call(self):
    pass

  def test_theta_put(self):
    pass

  def test_vega(self):
    pass

  def test_rho_call(self):
    pass

  def test_rho_put(self):
    pass

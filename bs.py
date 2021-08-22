from math import log, sqrt, exp, pi
from scipy.stats import norm

# http://www.anthony-vba.kefra.com/vba/vba13.htm

class Black_Scholes():
  
  def __init__(self, CallPutFlag, S, K, T, r, d=None, V=None):
    
    if CallPutFlag not in ['c', 'p']:
      raise ValueError('CallPutFlag is set wrongly. Must be "c" or "p".')
    
    self.CallPutFlag = CallPutFlag # Flag to identify if call or put
    self.S = S # Current value of underlying asset
    self.K = K # Strike Price
    self.T = T # Option life as percentage of year
    self.r = r # Risk free rate
    self.d = d # Dividend yield
    self.V = V # Sigma - Standard deviation of growth reate on the underlying

  # Cumulative probability distribution function of standard normal distribution
  def n(self, d):
    return norm.cdf(d)
  
  # First order derivative of n(d)
  def dn(self, d):
    return norm.pdf(d)

  def d1(self):
    return (log(self.S / self.K) + (self.r - self.d + self.V** 2 * 0.5) * self.T) / (self.V * sqrt(self.T))

  def d2(self):
    return self.d1() - (self.V * sqrt(self.T))

  def call(self):
    return (self.S * exp(-self.d*self.T)  * self.n(self.d1())) - (self.K * exp(-self.r * self.T) * self.n(self.d2()))

  def put(self):
    return (self.K * exp(-self.r * self.T) * self.n(-self.d2())) - (self.S * exp(-self.d * self.T)  * self.n(-self.d1()))

  def delta(self):
    if self.CallPutFlag == 'c':
      return self.n(self.d1()) 
    elif self.CallPutFlag == 'p':
      return (-self.n(-self.d1()))
  
  def gamma(self):
    return self.dn(self.d1()) / (self.S * self.V * sqrt(self.T))

  def vega(self):
    return 0.01 * (self.S * self.dn(self.d1()) * sqrt(self.T))

  def theta(self):
    if self.CallPutFlag == 'c':
      return ((-self.S * self.dn(self.d1()) * self.V) / (2 * sqrt(self.T)) - self.r * self.K * exp(-self.r * self.T) * self.n(self.d2())) / 365
    elif self.CallPutFlag == 'p':
      return ((-self.S * self.dn(self.d1()) * self.V) / (2 * sqrt(self.T)) + self.r * self.K * exp(-self.r * self.T) * self.n(-self.d2())) / 365
  
  def rho(self):
    if self.CallPutFlag == 'c':
      return 0.01 * (self.K * self.T * exp(-self.r * self.T) * self.n(self.d2()))
    elif self.CallPutFlag == 'p':
      return 0.01 * (-self.K * self.T * exp(-self.r * self.T) * self.n(-self.d2()))


  def implied_vol(self, MKT_PRICE):
    
    if self.V != None:
      raise ValueError("Volatility is already passed as a parameter.")

    PRECISION = 1.0e-5
    MAX_ITERATIONS = 200
    self.V = 0.5

    for i in range(MAX_ITERATIONS):
      diff = self.option_price() - MKT_PRICE

      print(i, self.V, diff)

      if (abs(diff) < PRECISION):
        break
      
      self.V = self.V - diff/(self.vega()*100)

    return self.V


  def option_price(self):
    if self.CallPutFlag == 'c':
      return self.call()
    elif self.CallPutFlag == 'p':
      return self.put()
  
  def option_greeks(self):
    return self.delta(), self.gamma(), self.vega(), self.theta(), self.rho()

if __name__ == '__main__':
  bs = Black_Scholes('c', 300, 250, 1, 0.03, 0.15)

  print(bs.option_price())
  print(bs.option_greeks())

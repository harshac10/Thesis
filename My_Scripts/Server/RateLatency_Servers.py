""" General Server process"""

from Server.Server_Process import ServerDistribution


class RateLatencyServer(ServerDistribution):

    def __init__(self, rate: float, latency: float):
        self.rate = rate
        self.latency = latency

    def sigma(self, theta: float) -> float:
        return self.latency

    def rho(self, theta: float) -> float:
        return self.rate

    def avg_rate(self) -> float:
        return self.rate

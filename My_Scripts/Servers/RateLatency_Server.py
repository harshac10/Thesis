""" General class for servers with Rate and latency """

from Servers.Server_Distribution import ServerDistribution


class RateLatencyServers(ServerDistribution):

    def __init__(self, rate: float, latency: float):
        self.rate = rate
        self.latency = latency

    def sigma(self, theta: float) -> float:
        return self.latency

    def rho(self, theta: float) -> float:
        return self.rate

    def avg_rate(self, theta: float) -> float:
        return self.rate

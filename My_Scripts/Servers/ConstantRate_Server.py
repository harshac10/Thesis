from Servers.RateLatency_Server import RateLatencyServers


class ConstantRateServer(RateLatencyServers):

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        return self.rate

    def avg_rate(self, theta: float) -> float:
        return self.rate

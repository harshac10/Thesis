from Servers.RateLatency_Server import RateLatencyServers


class ConstantRateServer(RateLatencyServers):

    def __init__(self, rate: float):
        super().__init__(rate=rate, latency=0.0)

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        return self.rate

    def avg_rate(self, theta: float) -> float:
        return self.rate

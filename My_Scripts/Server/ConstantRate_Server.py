""" Constant Rate server with zero Latencies"""

from Server.RateLatency_Servers import RateLatencyServer


class ConstantRateServer(RateLatencyServer):

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        return self.rate

    def avg_rate(self) -> float:
        return self.rate

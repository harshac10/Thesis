from abc import abstractmethod, ABC


class Server(ABC):

    @abstractmethod
    def sigma(self, theta: float) -> float:
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        pass

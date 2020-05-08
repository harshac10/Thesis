from abc import abstractmethod, ABC


class Arrival(ABC):

    @abstractmethod
    def sigma(self, theta: float) -> float:
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        pass

    @abstractmethod
    def discrete(self) -> bool:
        pass

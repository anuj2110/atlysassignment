from abc import ABC,abstractmethod
class StorageInterface(ABC):

    @abstractmethod
    def save(self,data):
        pass

    @abstractmethod
    def get_data(self):
        pass
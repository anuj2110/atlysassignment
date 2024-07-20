from abc import abstractmethod,ABC


class MessagingInteface(ABC):
    
    @abstractmethod
    def send_message(self,message):
        pass
    
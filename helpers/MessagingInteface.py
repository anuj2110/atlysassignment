from abc import abstractmethod,ABC


class MessagingInteface(ABC):
    
    @abstractmethod
    async def send_message(self,message):
        pass
    
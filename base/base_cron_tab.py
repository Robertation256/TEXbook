import abc

class BaseCronTab():

    @abc.abstractmethod
    def job(self,**kwargs):
        pass

    @abc.abstractmethod
    def schedule(self,**kwargs):
        pass
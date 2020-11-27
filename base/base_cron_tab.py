import abc

class BaseCronTab():

    @abc.abstractmethod
    def job(self):
        pass

    @abc.abstractmethod
    def schedule(self,**kwargs):
        pass
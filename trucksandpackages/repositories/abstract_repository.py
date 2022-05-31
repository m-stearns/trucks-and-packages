import abc

# Note: the Repository pattern is inspired by the
# following reference, written by Harry Percival and Bob Gregory:
# https://www.cosmicpython.com/book/chapter_02_repository.html

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, entity):
        raise NotImplementedError
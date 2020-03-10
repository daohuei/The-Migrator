#!/usr/bin/python3

from abc import ABC, abstractmethod


class Controller(ABC):
    @abstractmethod
    def __init__(self):
        pass
                      
    @abstractmethod
    def get_host_list(self):
        pass

    @abstractmethod
    def get_server_list(self):
        pass

    @abstractmethod
    def map_to_instance(self):
        pass

    @abstractmethod
    def migrate(self, instance, target):
       pass                   

"""
singletone decorator
Author: Akshaya Revaskar
Date: 23-04-2020
"""


# singletone decorator
def singleton(myClass):
    instances = {}

    def get_instance(*args, **kwargs):
        if myClass not in instances:
            instances[myClass] = myClass(*args, **kwargs)
        return instances[myClass]

    return get_instance
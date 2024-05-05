from design_patterns.singleton import SingletonMeta


class SingletonTestClass(metaclass=SingletonMeta):
    pass


def test_singleton_initializing_only_one_class_instance():
    first_instance = SingletonTestClass()
    second_instance = SingletonTestClass()

    assert first_instance == second_instance

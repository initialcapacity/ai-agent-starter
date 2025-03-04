import os


def slow(test_function):
    def wrapper(self, *args, **kwargs):
        if os.environ.get("RUN_SLOW_TESTS") == "true":
            test_function(self, *args, **kwargs)
        else:
            self.skipTest("skipping slow test")

    return wrapper

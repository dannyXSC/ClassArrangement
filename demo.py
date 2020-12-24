class demo():
    def fun(self, message):
        print(type(message) == type({}))


handle = demo()
target = "{'123': 1}"
handle.fun(target)
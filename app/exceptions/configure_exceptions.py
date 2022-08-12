class ItemDoesNotExist(Exception):
    def __init__(self, item_name: str, item_id: int):
        self.item_name = item_name
        self.item_id = item_id

    def __str__(self):
        return f"{self.item_name} with id: {self.item_id} does not exist"


class InvalidPassword(Exception):
    def __str__(self):
        return "Invalid Password"


class CustomerNotFound(Exception):
    def __str__(self):
        return "Email Not Found"


class WrongCredentialsException(Exception):
    def __str__(self):
        return "Wrong Password"


class ServerErrorException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

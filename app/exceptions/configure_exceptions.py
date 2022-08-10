class ItemDoesNotExist(Exception):
    def __init__(self, item_name: str, item_id: int):
        self.item_name = item_name
        self.item_id = item_id
    
    def __str__(self):
        return f"{self.item_name} with id: {self.item_id} does not exist"

class Room:

    def __init__(self, id, capacity):
        
        # room id and max capacity
        self._id = id
        self._capacity = capacity
    
    # return room id
    def get_id(self):
        return self._id

    # return room capacity
    def get_capacity(self):
        return self._capacity

    def __str__(self):
        return f"{self._id} | {self._capacity}"

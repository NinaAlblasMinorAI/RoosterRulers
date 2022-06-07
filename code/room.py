class Room:

    def __init__(self, id, capacity):
        
        # room id and max capacity
        self._id = id
        self._capacity = capacity
    
    # Return room id
    def get_id(self):
        return self._id

    # Return room capacity
    def get_capacity(self):
        return self._capacity

class Room:

    def __init__(self, id, capacity):
        """
        Room object to put into schedule.
        """

        # room id and max capacity
        
        self._id = id
        self._capacity = capacity
<<<<<<< HEAD
        self._location = None
    
    # return room id
    def get_id(self):
=======

    def has_id(self):
        """
        Return id of the room.
        """

>>>>>>> 44141beecdc8f48558ccf1837c8e9cbdccf12f9b
        return self._id

    def has_capacity(self):
        """
        Return max capacity of the room.
        """

        return self._capacity

    def __str__(self):
        """
        Representation of the object as a string.
        """
        
        return f"{self._id} | {self._capacity}"

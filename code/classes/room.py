class Room:

    def __init__(self, id, capacity):
        """
        Room object to put into schedule.
        """

        # room id and max capacity
        
        self._id = id
        self._capacity = capacity

    def get_id(self):
        """
        Return id of the room.
        """

        return self._id

    def get_capacity(self):
        """
        Return max capacity of the room.
        """

        return self._capacity

    def __str__(self):
        # return f"{self._id} | {self._capacity}"
        return f"{self._id}"

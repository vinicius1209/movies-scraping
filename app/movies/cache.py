from datetime import timedelta, datetime

class CacheItem(object):

    def __init__(self, key, movie):
        self.key = key
        self.movie = movie
        self.timestamp = datetime.now()


class Cache(object):

    # Initiate the movie cache with size and minutes to expire
    def __init__(self, length, delta=None):
        self.length = length
        self.delta = delta
        self.hash = {}
        self.item_list = []

    # Insert the movie item
    def insert(self, item):

        if item.key in self.hash:
            # Move the existing movie item to the head of item_list.
            item_index = self.item_list.index(item)
            self.item_list[:] = self.item_list[:item_index] + self.item_list[item_index+1:]
            self.item_list.insert(0, item)
        else:
            # Remove the last movie item if the length of cache exceeds the upper bound.
            if len(self.item_list) > self.length:
                self.removeItem(self.item_list[-1])

            # If this is a new movie item, just append it to the front of item_list.
            self.hash[item.key] = item
            self.item_list.insert(0, item)

    # Remove the outdated movie item
    def remove(self, item):

        del self.hash[item.key]
        del self.item_list[self.item_list.index(item)]

    # Get the movie item by key name and if found it, validate
    def get_item(self, movie):

        for item in self.item_list:
            if item.key == movie:
                # IF the movie item timestamp (creation date) is outdated, so return None
                if (item.timestamp + timedelta(minutes=self.delta)) < datetime.now():
                    self.remove(item)
                    return None
                else:
                    return item
        return None


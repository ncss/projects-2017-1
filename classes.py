class List:
    def __init__(self, title, *args):
        self.title = title
        self.items = [a for a in args]
        self.i = -1

    def __iter__(self):
        return iter(self.items)

    def add(self, user):
        '''
        Add a bucket list to the given user,
        Throws an error if user doesn't exist
        or bucket object invalid
        '''
        pass

    def update(self, user, **kwargs):
        '''
        Edit the bucket of a given user,
        changes are passed in through a
        dictionary.
        //TODO fix how data is passed in
        '''
        pass

    @staticmethod
    def get(user):
        '''
        Get the bucket data of a given user
        '''
        cur.execute()##Insert SQL Here
        cer.fetchone()
        for row in cur:
            title, *args = row
            return List(title, args)
        raise BucketNotFoundError("Bucket List of {} not found".format(user.name))


class Item:
    def __init__(self, vals):
        self.completed = False
        self.text = ''
        self.image = ''
        for a in vals:
            if isinstance(a, int):
                self.completed = bool(a)
            elif a.startswith('static/'):
                self.image = a.strip()
            else:
                self.text = a.strip()

    def __str__(self):
        return "{} : {}".format(self.text, "Yes" if self.completed else "No")

    def set_completed(self):
        self.completed = not self.completed

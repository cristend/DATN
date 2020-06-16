class User():
    def __init__(self, id):
        self.id = id
        self.key = None
        self.status = True


class Users():
    def __init__(self):
        self.users = None

    def create_user(self, users):
        user_list = list()
        for user in range(users):
            new_user = User(id=str((user+1)*10))
            user_list.append(new_user)
        self.users = user_list
        return user_list

    def print(self):
        for user in self.users:
            print(f'user_id: {user.id}')

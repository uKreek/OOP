from authorization_class import AuthService, User, UserRepository

repo = UserRepository('users.pkl')
auth = AuthService(repo)

user1 = User(1, 'Naruto', 'Hokage', '12345678', address='Konoha')
user2 = User(2, 'Steve', 'steve01', '0000')


repo.add(user1)
repo.add(user2)

print(repo.get_all())

# 2. edit user's property
user2.login = 'herobrin'
repo.update(user1)
print(f'User {user2.data_id} edited login to: {user2.login}')

print(repo.get_by_login('herobrin'))
print('---------------------------')

# 3. auth user
login_input = "herobrin"
pass_input = "0000"

user_found = repo.get_by_login(login_input)

if user_found and user_found.password == pass_input:
    auth.sign_in(user_found)
else:
    print('Incorrect login or password')

# 4. change user
print(auth.current_user.login)

print(auth.current_user)

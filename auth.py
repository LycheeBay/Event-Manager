import sqlite3
import secrets


class Authenticator:
  counter = 0
  entries = ["password", "privilege"]
  active_tokens = []
  database = 0

  def __init__(self):
    self.counter = 0
    self.database = sqlite3.connect("auth_database.db",
                                    check_same_thread=False)
    self.database.execute(
      "CREATE TABLE IF NOT EXISTS Password_DB (email STRING PRIMARY KEY, password STRING, priv INTEGER);"
    )
    #self.purge_users()

  def add_user(self, email, pwd, priv):
    if not self.has_user(email):
      print("adding")
      self.database.execute(
        r"INSERT INTO Password_DB (email,password,priv) VALUES ('" + email +
        "','" + pwd + "'," + str(priv) + ")")
      self.database.commit()
      return True
    else:
      return False

  def has_user(self, email):
    return bool(
      self.database.execute("SELECT * FROM Password_DB WHERE email = '" +
                            email + "'").fetchall())

  def change_password(self, email, pwd):
    if self.has_user(email):
      self.database.execute("UPDATE Password_DB SET password = '" + pwd +
                            "' WHERE email = '" + email + "'")
      self.database.commit()
      return True
    else:
      return False

  def get_all_users(self):
    cursur_object = self.database.execute("SELECT * FROM Password_DB")
    return cursur_object.fetchall()

  def purge_users(self):
    self.database.execute("DELETE FROM Password_DB")

  def get_token(self, email, password):
    user_info = self.database.execute(
      "SELECT * FROM Password_DB WHERE email = '" + email + "'").fetchall()
    if str(user_info[0][1]) == password:
      tk = secrets.token_urlsafe(20)
      self.active_tokens.append([tk, user_info[0][2]])
      return tk
    else:
      return "NULL"

  def token_active(self, token):
    for token_pair in self.active_tokens:
      if token_pair[0] == token:
        return True
    return False

  def get_privilege(self, token):
    for token_pair in self.active_tokens:
      if token_pair[0] == token:
        return token_pair[1]
    return False

  def log_out(self, token):
    for token_pair in self.active_tokens:
      if token_pair[0] == token:
        self.active_tokens.remove(token_pair)
        return True
    return False


"""
auth = Authenticator()
auth.purge_users()
print(auth.has_user("sandy@gmail.com"))
auth.add_user(r"sandy@gmail.com", "123456", 1)
auth.add_user(r"sandycreek@gmail.com", "123456", 1)
print(auth.has_user("sandy@gmail.com"))
auth.add_user(r"sandy@gmail.com", "123457", 1)
auth.change_password("sandy@gmail.com", "114511")
print(auth.get_all_users())
temp = auth.get_token("sandy@gmail.com", "114511")
print(temp)
print(auth.get_privilege(temp))
print(auth.log_out(temp))
print(auth.log_out(temp))
"""

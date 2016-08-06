import hello
import os
hello.db.drop_all()
hello.db.create_all()
print("db cleared")
os.system("pause")
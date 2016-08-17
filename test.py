from hello import *
p = Post("None", "4_20_2016", "Oh look, the library. Nice new and renovated the teen zone is inovative!", "testUser41: neat!", "Joe41")
db.session.add(p)
db.session.commit()
import hello
LogIn = hello.Badge("Log In", 'Default_Badge.png', '#654321','gray', "You created a digital skypy account!")
hello.db.session.add(LogIn)
hello.db.session.commit()
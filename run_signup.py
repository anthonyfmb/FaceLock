import signup as signup

box = signup.SignupToolBox(500)
box.collect_valid_user_data()

return box.create_password(20)
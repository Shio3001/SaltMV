import os
# print(os.environ.get("USER"))

user = str(os.environ.get("USER"))
# /System/Library/Fonts
# /Library/Fonts
# /Users/maruyama/Library/Fonts
font_path = os.path.join("Users", user, "Library/Fonts")

print(font_path)

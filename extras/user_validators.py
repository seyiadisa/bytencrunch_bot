import re

def check_matno(matno):
    pattern = r"\d{2}[a-zA-z]{2}\d{6}"
    return bool(re.fullmatch(pattern, matno))

def check_room(room):
    pattern = r"[a-hA-H][0-4][0-1]\d"
    return bool(re.fullmatch(pattern, room))

def check_email(email):
    pattern = r"\w+\.\w+\@stu\.cu\.edu\.ng"
    return bool(re.fullmatch(pattern, email))
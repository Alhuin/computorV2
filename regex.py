import re

get = re.compile("^(.*)\s*\=\s*\?\s*$", flags=re.IGNORECASE)

func = re.compile("(fun[a-z])\((\d+|[a-z]+)\)", flags=re.IGNORECASE)

checkFunc = re.compile("fun[A-Z]\(([a-z])\)\s*\=\s*.*", flags=re.IGNORECASE)

checkAssign = re.compile("[A-Z]+\s*\=\s*.*", flags=re.IGNORECASE)

checkLetter = re.compile("[A-Z]", flags=re.IGNORECASE)

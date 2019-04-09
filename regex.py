import re

get = re.compile("^(.*)\s*\=\s*\?\s*$", flags=re.IGNORECASE)
fnIntParam = re.compile("fun[a-z]\((\d+)\)", flags=re.IGNORECASE)
fnVarParam = re.compile("fun[a-z]\(([A-Z]+)\)", flags=re.IGNORECASE)
checkFunc = re.compile("fun[A-Z]\(([a-z])\)\s*\=\s*.*", flags=re.IGNORECASE)
checkVariable = re.compile("var[A-Z]\s*\=\s*.*", flags=re.IGNORECASE)
checkAssign = re.compile("[A-Z]+\s*\=\s*.*", flags=re.IGNORECASE)
checkLetter = re.compile("[A-Z]", flags=re.IGNORECASE)
computeFn = re.compile("^\s*fun[A-Z]\(\d+\)\s*\=\s*?\s*$", flags=re.IGNORECASE)
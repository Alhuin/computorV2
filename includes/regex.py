import re

get = re.compile(r"^(.*)\s*=\s*\?\s*$", flags=re.IGNORECASE)

put = re.compile(r"^\s*([A-Z]+|fun[A-Z]\([A-Z]\))\s*=(.*)", flags=re.IGNORECASE)

reset = re.compile(r"^\s*reset\s*(.*)\s*$", flags=re.IGNORECASE)

complex = re.compile(r"(?:(\d+)\s*)?([+\-]?\s*\d+)\s*\*?\s*i", flags=re.IGNORECASE)

func = re.compile(r"(fun[a-z])\((\d+|[a-z]+)\)", flags=re.IGNORECASE)

evalFunc = re.compile(r"(fun[a-z])\(((?:[a-z]|[\d\s+\-*/%])+)\)", flags=re.IGNORECASE)

draw = re.compile(r"^\s*draw\s*(fun[A-Z])\s*", flags=re.IGNORECASE)

checkMatrice = re.compile(r"(\[\[\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)*\](?:;\[\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)*\])*\])",
                          flags=re.IGNORECASE)

parseMatrice = re.compile(r"\[(\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)*)\]", flags=re.IGNORECASE)

checkLetter = re.compile(r"([A-HJ-Z])", flags=re.IGNORECASE)

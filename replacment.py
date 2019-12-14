import re

## uppercase every character after a -/_
## remove -/_
def cleanCamelCase(value, matchPattern="-_"):
    value = re.sub(r'(?:['+matchPattern+'])([a-z])', lambda pat: pat.group(1).upper(), value) # Inline
    print(value)
    return value

cleanCamelCase('bob-bo-hob-nob_bob-glob')

## uppercase every character after a -/_
## remove -/_
def camelCaseToDash(value,replacePattern="-"):
    value = re.sub(r'([A-Z])', lambda pat: replacePattern+pat.group(0).lower(), value) # Inline
    print(value)
    return value

camelCaseToDash('bobBoHobNobBobGlob')

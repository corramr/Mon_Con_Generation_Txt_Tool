#Misc functions

#Filters out blank spaces at beginning and end and enables Pascal case 
def clean_string(text):
    result = text.replace("/", "_").replace("-", "_")
    result = '_'.join(result.capitalize() for result in result.split('_')).strip()
    print(result)
    return result
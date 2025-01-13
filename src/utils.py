#Misc functions

#Filters out blank spaces at beginning and end and enables Pascal case 
def clean_string(text):
    result = '_'.join(result.capitalize() for result in text.split('_')).strip()
    return result
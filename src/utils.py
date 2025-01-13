#Misc functions

#Filters out blank spaces at beginning and end and enables Pascal case 
def clean_string(text):
    result = text.replace("/", "_").replace("-", "_")
    result = '_'.join(result.capitalize() for result in result.split('_')).strip()
    return result

def write_fields_to_file(object,file_name):
    
    for field, value in vars(object).items():        
        if value:
            for item in value:
                file_name.write(item)                
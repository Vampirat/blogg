

def get_hashtag(object:str) -> list:

    '''Выделяет из текста хештеги,
    если они есть и возвращает их кортежем'''
   
    obj_list = object.split()
    tags_list = [word for word in obj_list if word.startswith('#')]
    tags_list = list(dict.fromkeys(tags_list))
    return tags_list


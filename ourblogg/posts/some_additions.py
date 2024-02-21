

def get_hashtag(object:str) -> list:

    '''Выделяет из текста хештеги,
    если они есть и возвращает их списком'''
    obj_list = object.split()
    tags_list = []
    for word in obj_list:
        if word.startswith('#'):
            tag = word.split('#')
            for t in tag:
                if t == '':
                    tag.remove(t)
            tags_list += tag
            tags_list = list(dict.fromkeys(tags_list))
    print(tags_list)
    return tags_list

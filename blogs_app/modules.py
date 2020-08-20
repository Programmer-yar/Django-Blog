import re

def Search_Function(search_string, data):
    
    search = search_string

    if re.search('[a-zA-Z]', search):
        titles_list = []
        for post in data:
            titles_list.append(post.title)

        split_search = search.lower().split()
        split_search_original = split_search[:]

        if len(split_search) > 1:
            first_two_words = split_search[0]+' '+split_search[1]
        else:
            first_two_words = split_search[0]

        useless_words = ['the', 'a', 'to', 'i']

        for word in split_search:
            if word in useless_words:
                split_search.remove(word)

        counter = 0
        found_posts = []

        for title in titles_list:
            
            title=title.lower()
            
            if search.lower() == title:
                found_posts.append(title)
                break

            elif title.startswith(first_two_words):
                found_posts.append(title)

            else:
                for each_word in split_search:
                    if each_word in title:
                        counter += 1
                        if counter > 2:
                            found_posts.append(title)
                            break


        filtered_posts = []
        for post in data:
            if post.title.lower() in found_posts:
                filtered_posts.append(post)

        return filtered_posts

    else:

        return ["Nothing Found"]
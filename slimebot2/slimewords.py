import json
import time


def get_slime_list():
    with open('slimelist.json') as slime_list_file_descriptor:
        slime_word_dict = json.load(slime_list_file_descriptor)
        return slime_word_dict

def get_black_list():
    with open('blacklist.json') as black_list_file_descriptor:
        black_list_dict = json.load(black_list_file_descriptor)
        return black_list_dict

def remove_word(word):
    slime_word_dict = get_slime_list()
    black_list_dict = get_black_list()
    print(slime_word_dict)
    slime_word_dict.__delitem__(word)
    black_list_dict[word] = time.time()
    write_slime_dict_to_file(slime_word_dict)
    write_blacklist_dict_to_file(black_list_dict)

def write_words(words,adder):
    slime_word_dict = get_slime_list()
    black_list_dict = get_black_list()

    for word in words:
        if word not in slime_word_dict and word not in black_list_dict:
            submission_info = {"id": adder, "time": time.time()}
            slime_word_dict[word] = submission_info
    write_slime_dict_to_file(slime_word_dict)

def blacklist_words(words,blacklister):
    slime_word_dict = get_slime_list()
    black_list_dict = get_black_list()

    for word in words:
        if word not in black_list_dict:
            submission_info = {"id": blacklister, "time": time.time()}
            black_list_dict[word] = submission_info
            if word in slime_word_dict:
                slime_word_dict.__delitem__(word)
    write_blacklist_dict_to_file(black_list_dict)



def write_slime_dict_to_file(updated_list):
    with open('slimelist.json', 'w') as slime_list_file_descriptor:
        json.dump(updated_list, slime_list_file_descriptor)


def write_blacklist_dict_to_file(updated_list):
    with open('blacklist.json', 'w') as black_list_file_descriptor:
        json.dump(updated_list, black_list_file_descriptor)
import http.client
import json
import os
import nltk
# http://stackoverflow.com/questions/24406201/how-do-i-remove-verbs-prepositions-conjunctions-etc-from-my-text
# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

def toWordDict(songObject, output):
    """
    Adds a song object to an

    Keyword arguments:
    songObject -- A dict-like json object with song meta
    output -- A dictionary containing every lyric from a particular song stored
    with a list of song titles in which that lyrics appears
    """

    lyrics = songObject["lyrics"]
    my_buffer = []

    for char in lyrics:
        if char.isalpha():
            my_buffer.append(char.lower())
        elif char.isspace():
            word = "".join(my_buffer)
            titles = output.setdefault(word, [])
            if songObject["title"] not in titles:
                titles.append(songObject["title"])
            my_buffer.clear()


if __name__ == "__main__":
    conn = http.client.HTTPConnection("www.kanyerest.xyz")
    conn.request("GET", "/api/all")

    # This is a json file containing an object for each Kanye song with keys
    # album, title, lyrics
    r1 = conn.getresponse()
    r1_as_string = r1.read().decode()

    decoder = json.JSONDecoder()
    songs = decoder.decode(r1_as_string)
    lyric_to_title = {}

    for song in songs:
        toWordDict(song, lyric_to_title)

    with open("lyric_to_title.json", "w") as f:
        json.dump(lyric_to_title, f, indent=2, sort_keys=True)

    conn.close()

    print("\n" + "Lyric dictionary created at lyric_to_title.json" + "\n")

import http.client
import json    

# Pre: a dict-like json object
# Post: The output dict now contains every lyric from a particular song
# stored with a list of song titles that lyric appears in
def toWordDict(songObject, output):
    lyrics = songObject["lyrics"]
    my_buffer = []

    for char in lyrics:
        if char.isalpha():
            my_buffer.append(char.lower())
        elif char.isspace():
            word = "".join(my_buffer)
            titles = output.setdefault(word, [])
            if songObject["album"] not in titles:
                titles.append(songObject["album"])
            my_buffer.clear()

if __name__ == "__main__":
    conn = http.client.HTTPConnection("www.kanyerest.xyz")
    conn.request("GET", "/api/all")

    # This is a json file containing an object for each Kanye song with keys album, title, lyrics
    r1 = conn.getresponse()
    r1_as_string = r1.read().decode()
    
    decoder = json.JSONDecoder()
    songs = decoder.decode(r1_as_string)
    lyric_to_title = {}

    for song in songs:
        toWordDict(song, lyric_to_title)

    with open("lyric_to_title.json", "w") as f:
        json.dump(lyric_to_title, f)
    
    conn.close()

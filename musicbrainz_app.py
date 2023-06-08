import musicbrainzngs


def get_new_artists_from_usa(limit):
    musicbrainzngs.set_useragent("My Music App", "0.1", "")
    musicbrainzngs.set_rate_limit(limit_or_interval=True)  # Enable rate limiting

    new_artists = []

    offset = 0
    while True:
        result = musicbrainzngs.search_artists(query="", tag="new", limit=limit, offset=offset, area="489ce91b-6658-3307-9877-795b68554c98")

        if "artist-list" in result and result["artist-list"]:
            artists = result["artist-list"]
            new_artists.extend([artist["name"] for artist in artists])
            break
        offset += limit

        if len(artists) < limit:
            break

    return new_artists

# Example usage
limit = 100  # Adjust the limit per request as desired
artists = get_new_artists_from_usa(limit)
for artist in artists:
    print(artist)

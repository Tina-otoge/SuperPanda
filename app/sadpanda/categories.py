FILTER_BASE = 1023

FILTERS = {
    'misc': 1,
    'doujin': 2,
    'manga': 4,
    'artist_cg': 8,
    'game_cg': 16,
    'image_set': 32,
    'cosplay': 64,
    'asian_porn': 128,
    'non_h': 256,
    'western': 512,
}

def to_filter(l):
        return FILTER_BASE - sum([FILTERS.get(x, 0) for x in l])

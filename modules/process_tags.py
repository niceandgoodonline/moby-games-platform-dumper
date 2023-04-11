import f_util

def cull_tags(data: dict, cull: list) -> dict:
        new_data = {}
        for k,v in data.items():
                game_data = v.copy()
                game_data['tags'] = []
                for tag in v['tags']:
                        if tag in cull:
                                continue
                        else:
                                game_data['tags'].append(tag)
                new_data[k] = game_data
        return new_data


def replace_tags(data: dict, replace: dict) -> dict:
        new_data = {}
        for k,v in data.items():
                game_data = v.copy()
                for kk,vv in replace.items():
                        if kk in game_data['tags']:
                                game_data['tags'].remove(kk)
                                game_data['tags'].append(vv)
                new_data[k] = game_data
        return new_data

def cull_naive_genres(data: list, cull: list) -> dict:
        for genre in cull:
                if genre in data:
                        data.remove(genre)
        return data     


def replace_naive_genres(data: list, replace: dict) -> dict:
        new_list = set({})
        keys     = replace.keys()
        for genre in data:
                if genre in keys:
                        new_list.add(replace[genre])
                else:
                        new_list.add(genre)
        return sorted(list(new_list))


def flatten_genres_to_tags(data: dict) -> dict:
        new_data = {}
        for k,v in data.items():
                tags = set({})
                for item in v['genres']:
                        tags.add(item['genre_name'])
                        print(item)
                print(tags)
                new_data[k] = v
                new_data[k].pop('genres')
                new_data[k]['tags'] = list(tags)
        return new_data


def dump_platform_tags(data: dict, path: str) -> list:
        tags = set({})
        for k,v in data.items():
                tags.update([tag for tag in v['tags']])
        if not f_util.check_file_exists(f"{path}"):
                f_util.write_respose_to_file(f"{path}", {"tags": list(tags)})
        return list(tags)


def dump_tags_to_list(data: dict, genre: list):
        for genre in genres:
                json = {}
                json = {"slug": []}
                for k,v in data.items():
                        if genre in v['tags']:
                                json["slug"].append(k)
                f_util.write_respose_to_file(f"json/{platform}/genres/{genre}.json", json)
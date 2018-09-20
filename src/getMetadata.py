from __future__ import print_function
import flickrapi
import json
import csv
import configparser

if __name__ == "__main__":

    user_id = "154092236@N05"

    inifile = configparser.ConfigParser()
    inifile.read('./config.ini', 'UTF-8')

    api_key = inifile.get('settings', 'key')
    api_secret = inifile.get('settings', 'secret')

    api = flickrapi.FlickrAPI(api_key, api_secret)

    collections = ["72157692332884624", "72157666053544958", "72157666708394758", "72157693000400064",
                   "72157664080018847", "72157664666627177", "72157690828771862", "72157692097711501",
                   "72157693841087965"]

    f = open('data/metadata.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    fields = []
    fields.append("uparl:identifier")
    list = []

    for collection_id in collections:
        print("collection\t" + str(collection_id))
        res = api.collections.getTree(
            collection_id=collection_id,
            user_id=user_id,
            format='json')
        collection_dict = json.loads(res.decode('utf-8'))
        set = collection_dict["collections"]["collection"][0]["set"]

        for photoset in set:
            print("photoset\t" + photoset["id"])
            res = api.photosets.getPhotos(
                photoset_id=photoset["id"],
                user_id=user_id,
                format='json')

            photoset_dict = json.loads(res.decode('utf-8'))

            for photo in photoset_dict["photoset"]["photo"]:
                photo_id = photo["id"]
                title = photo["title"]
                print("title\t" + title)

                res = api.photos.getInfo(
                    photo_id=photo_id,
                    format='json')
                photo_dict = json.loads(res.decode('utf-8'))
                description = photo_dict["photo"]["description"]["_content"]

                metadata = description.split("\n")

                item = {}
                list.append(item)
                item["uparl:identifier"] = title

                for i in range(7, len(metadata) - 4):
                    element = metadata[i].split("：")
                    field = element[0].split(" ")[0]
                    if len(element) == 1:
                        value = ""
                    else:
                        value = element[1]

                    if field not in fields:
                        fields.append(field)
                    item[field] = value

                break

    writer.writerow(fields)

    for item in list:
        row = []
        for field in fields:
            if field in item:
                row.append(item[field])
            else:
                row.append("")
        writer.writerow(row)

    f.close()

from __future__ import print_function
import flickrapi
import json
import configparser


def update_description(photo_id):
    res = api.photos.getInfo(
        photo_id=photo_id,
        format='json')
    info = json.loads(res.decode('utf-8'))

    description = info["photo"]["description"]["_content"]

    for key in replace_map:
        description = description.replace(key, replace_map[key])

    api.photos.setMeta(
        photo_id=photo_id,
        description=description)


def update_license(photo_id):
    api.photos.licenses.setLicense(
        photo_id=photo_id,
        license_id=4)


if __name__ == "__main__":

    user_id = "154092236@N05"

    replace_map = {}
    replace_map["クリエイティブ・コモンズ 表示-非営利-継承 4.0 国際ライセンス（CC BY-NC-SA）"] = "クリエイティブ・コモンズ 表示 4.0 国際ライセンス（CC BY）";
    replace_map[
        "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ja"] = "https://creativecommons.org/licenses/by/4.0/deed.ja";
    replace_map[
        "the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)"] = "the Creative Commons Attribution 4.0 International (CC BY 4.0)";
    replace_map[
        '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en" rel="nofollow">creativecommons.org/licenses/by-nc-sa/4.0/deed.en</a>'] = '<a href="https://creativecommons.org/licenses/by/4.0/deed.en" rel="nofollow">creativecommons.org/licenses/by/4.0/deed.en</a>';

    inifile = configparser.ConfigParser()
    inifile.read('./config.ini', 'UTF-8')

    api_key = inifile.get('settings', 'key')
    api_secret = inifile.get('settings', 'secret')

    api = flickrapi.FlickrAPI(api_key, api_secret)

    # api.token_cache.forget()

    if not api.token_valid():
        # OOB: out of band
        api.get_request_token(oauth_callback="oob")

        verifier = str(input("Get verifier code from {} and enter it here.\n: ".format(
            api.auth_url(perms="write"))))

        # Get access token and store it as ${HOME}/.flickr/oauth-tokens.sqlite.
        # If you want to remove the cache, call api.token_cache.forget().
        api.get_access_token(verifier)

    flg = True
    page = 1

    while flg:
        res = api.people.getPhotos(
            user_id=user_id,
            page=page,
            format='json')
        photos = json.loads(res.decode('utf-8'))

        photo_list = photos["photos"]["photo"]

        pages = photos["photos"]["pages"]

        page_status = str(page) + "/" + str(pages)

        print(page_status)

        page += 1

        if len(photo_list) > 0:

            for i in range(len(photo_list)):
                photo = photo_list[i]

                photo_id = photo["id"]

                photo_status = str(i + 1) + "/" + str(len(photo_list))

                print(photo_status + "\t" + photo_id + "\t" + photo["title"])

                update_description(photo_id)
                update_license(photo_id)

        else:
            flg = False

import datetime
import os
import json


def find_recent_in(days):
    main_dir = os.getcwd()
    # noinspection PyBroadException
    try:
        main_dir = os.getcwd()
        os.chdir("cvelistV5-main")
        os.chdir("cves")

        file = "recent_activities.json"
        with open(file, 'r', encoding='utf-8') as f:
            text = json.load(f)

        needed_date = datetime.datetime.today() - datetime.timedelta(days=int(days+1))
        needed_date = datetime.date(needed_date.year, needed_date.month, needed_date.day)

        i = 0
        result = "Вот, что я нашел за указанный период:\n\n"
        while i != len(text):
            if str(needed_date) in text[i]["startTime"]:
                break
            # noinspection PyBroadException
            try:
                result += text[i]["delta"]["new"][0]["cveId"]
                result += '\n'
            except Exception:
                pass
            i += 1
    except Exception:
        result = "У меня возникла ошибка..."

    os.chdir(main_dir)
    return result

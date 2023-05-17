import json
import os


def find_recent_cve():
    # noinspection PyBroadException
    try:
        main_dir = os.getcwd()
        os.chdir("cvelistV5-main")
        os.chdir("cves")

        file = "recent_activities.json"

        with open(file, 'r', encoding='utf-8') as f:
            text = json.load(f)

        recent_cve = text[0]["delta"]["new"][0]["cveId"]
        recent_cve_date = text[0]["stopTime"]
        result = f"Вот ID последней CVE, которую мне удалось найти: {recent_cve}.\nПоследнее добавление было {recent_cve_date}"
    except Exception as ex:
        print(ex)
        result = "Мне не удалось найти последнюю CVE"

    os.chdir(main_dir)
    return result

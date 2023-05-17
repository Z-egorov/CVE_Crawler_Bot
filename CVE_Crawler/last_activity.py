import json
import os


def find_last_activity():
    main_dir = os.getcwd()
    # noinspection PyBroadException
    try:
        main_dir = os.getcwd()
        os.chdir("cvelistV5-main")
        os.chdir("cves")

        with open("recent_activities.json", 'r', encoding='utf-8') as f:
            text = json.load(f)

        a = text[0]["steps"][0]["summary"]["cveIds"]

        result = "За последнее время были зафиксированы следущие активности:\n\n"

        for i in a:
            result += str(i)
            result += '\n'

    except Exception:
        result = "У меня возникла ошибка с этим"

    os.chdir(main_dir)
    return result

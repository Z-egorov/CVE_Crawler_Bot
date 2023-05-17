import json
import os


def finder(year, cve_id):
    # noinspection PyBroadException
    try:
        main_dir = os.getcwd()
        os.chdir("cvelistV5-main")
        os.chdir("cves")
        os.chdir(year)

        series = cve_id[:-3]
        series += "xxx"
        os.chdir(series)

        file = "CVE-" + year + "-" + str(cve_id) + ".json"

        with open(file, 'r', encoding='utf-8') as f:
            text = json.load(f)

        cve_num = text["cveMetadata"]["cveId"]
        cve_description = text["containers"]["cna"]["descriptions"][0]["value"]
        cve_publish_date = text["cveMetadata"]["datePublished"]
        cve_create_date = text["cveMetadata"]["dateReserved"]
        cve_reference = text["containers"]["cna"]["references"][0]["url"]
        cve_product = text["containers"]["cna"]["affected"][0]["product"]
        cve_product_versions = text["containers"]["cna"]["affected"][0]["versions"][0]["version"]
        cve_status = text["containers"]["cna"]["affected"][0]["versions"][0]["status"]

        result = f"Итак, вот, что я нашел:\nId: {cve_num}\nОписание: {cve_description}\nCVE была опубликована {cve_publish_date}, а разработана {cve_create_date}\nCVE сделана для {cve_product} версии {cve_product_versions}\nСтатус CVE: {cve_status}\nВот ссылка, которую вы можете изучить:\n{cve_reference}"
    except Exception:
        result = "Я не нашёл такой CVE.\nМожет, Вы ошиблись?"
    os.chdir(main_dir)
    return result

from ..ciim.utils import find, find_all, format_description_markup, pluck


def transform_record_result(result):
    """Fetch data from an Elasticsearch response to pass to Record.__init__"""

    data = {}

    source = result["_source"]
    identifier = source.get("identifier")
    summary = source.get("summary")

    data["iaid"] = source["@admin"]["id"]
    data["reference_number"] = pluck(
        identifier, accessor=lambda i: i.get("reference_number")
    )
    data["title"] = summary.get("title")

    if access := source.get("access"):
        data["closure_status"] = access.get("conditions")

    if origination := source.get("origination"):
        data["created_by"] = pluck(
            origination, accessor=lambda i: i["creator"][0]["name"][0]["value"]
        )

    if description := source.get("description"):
        data["description"] = format_description_markup(description[0]["value"])

    if arrangement := source.get("arrangement"):
        data["arrangement"] = format_description_markup(arrangement["value"])

    if legal := source.get("legal"):
        data["legal_status"] = legal["status"]

    if repository := source.get("repository"):
        data["repo_summary_title"] = repository.get("summary", {}).get("title", "")
        if repo_identifier := repository.get("identifier", ""):
            archon_dict = find(
                repo_identifier, predicate=lambda i: i["type"] == "Archon number"
            )
            data["repo_archon_value"] = archon_dict.get("value", "")

    data["is_digitised"] = source.get("digitised", False)

    if parent := source.get("parent"):
        data["parent"] = {
            "iaid": pluck(parent, accessor=lambda i: i["@admin"]["id"]),
            "reference_number": pluck(
                parent,
                accessor=lambda i: i["identifier"][0]["reference_number"],
            ),
            "title": pluck(parent, accessor=lambda i: i["summary"]["title"]),
        }

    if hierarchy := source.get("@hierarchy"):
        data["hierarchy"] = [
            {
                "reference_number": i["identifier"][0]["reference_number"],
                "title": i["summary"]["title"],
            }
            for i in hierarchy[0]
            if "identifier" in i
        ]
        try:
            # non mandatory data
            if hierarchy3 := hierarchy[0][2]:
                data["hierarchy3_reference_number"] = hierarchy3.get("identifier")[0][
                    "reference_number"
                ]
                data["hierarchy3_summary_title"] = hierarchy3.get("summary").get(
                    "title"
                )
                print(data["hierarchy3_reference_number"], data["hierarchy3_summary_title"])
        except Exception:
            pass

    if availability := source.get("availability"):
        if delivery := availability.get("delivery"):
            data["availability_delivery_surrogates"] = delivery.get("surrogate")

    if topics := source.get("topic"):
        data["topics"] = [
            {
                "title": i["summary"]["title"],
            }
            for i in topics
        ]

    if related := source.get("related"):
        related_records = find_all(
            related,
            predicate=lambda i: i["@link"]["relationship"]["value"] == "related",
        )
        data["related_records"] = [
            {
                "title": i["summary"]["title"],
                "iaid": i["@admin"]["id"],
            }
            for i in related_records
        ]

        related_articles = find_all(
            related, predicate=lambda i: i["@admin"]["source"] == "wagtail-es"
        )
        data["related_articles"] = [
            {
                "title": i.get("summary", {}).get("title", ""),
                "url": i.get("source", {}).get("location", ""),
            }
            for i in related_articles
            if "summary" in i
        ]

    data["media_reference_id"] = pluck(
        source.get("multimedia"), accessor=lambda i: i["@admin"]["id"]
    )

    if next_record := source.get("@next"):
        data["next_record"] = {"iaid": next_record["@admin"]["id"]}

    if previous_record := source.get("@previous"):
        data["previous_record"] = {"iaid": previous_record["@admin"]["id"]}

    if catalogue_source := source.get("source"):
        data["catalogue_source"] = catalogue_source["value"]

    if level := source.get("level"):
        data["level_code"] = str(level["code"])

    if template := source.get("@template"):
        data["held_by"] = template.get("details", {}).get("heldBy", "")
        data["origination_date"] = template.get("details", {}).get("dateCreated", "")
        data["level"] = template.get("details", {}).get("level", "")
        data["availability_delivery_condition"] = template.get("details", {}).get(
            "deliveryOption", ""
        )
        data["template_reference_number"] = template.get("details", {}).get(
            "referenceNumber", ""
        )
        data["template_summary_title"] = template.get("details", {}).get(
            "summaryTitle", ""
        )

    return data


def transform_image_result(result):
    """Fetch data from an Elasticsearch response to pass to Image.__init__"""

    data = {}

    data["thumbnail_location"] = pluck(
        result["_source"], accessor=lambda i: i["processed"]["preview"]["location"]
    )
    data["location"] = result["_source"]["processed"]["original"]["location"]
    data["sort"] = result["_source"]["sort"]

    return data

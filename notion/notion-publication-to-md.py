import os
from notion_client import Client
from pprint import pprint

notion = Client(auth=os.environ[""])

def get_database(database_id):
    return notion.databases.retrieve(database_id)

def query_database(database_id):
    return notion.databases.query(database_id)

def get_pages(database_id):
    pages = []
    result = query_database(database_id)
    pages.extend(result["results"])

    while "next_cursor" in result and result["next_cursor"]:
        cursor = result["next_cursor"]
        result = query_database(database_id, cursor)
        pages.extend(result["results"])

    return pages

def page_to_markdown(page):
    content = ""

    for property_name, value in page["properties"].items():
        if value["type"] == "title":
            title = value["title"][0]["text"]["content"]
            content += f"# {title}\n\n"
        elif value["type"] == "rich_text":
            text = value["rich_text"][0]["text"]["content"]
            content += f"{text}\n\n"
        elif value["type"] == "multi_select":
            tags = ", ".join([tag["name"] for tag in value["multi_select"]])
            content += f"Tags: {tags}\n\n"

    return content

def save_page_as_markdown(page, directory="markdown_files"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    markdown_content = page_to_markdown(page)
    file_name = f"{page['id']}.md"
    file_path = os.path.join(directory, file_name)

    with open(file_path, "w") as file:
        file.write(markdown_content)

def main():
    database_id = input("Введите ID базы данных Notion: ")
    database = get_database(database_id)
    pages = get_pages(database_id)

    for page in pages:
        save_page_as_markdown(page)

if name == "__main__":
    main()
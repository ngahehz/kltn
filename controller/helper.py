import json

def get_icons_color():
    with open('json-styles/dashboard_style.json', 'r') as file:
        data = json.load(file)
    return data["QSettings"][0]["ThemeSettings"][0]["CustomTheme"][0]["Icons-color"]

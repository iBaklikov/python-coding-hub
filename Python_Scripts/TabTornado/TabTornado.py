import webbrowser
with open(r'D:\Users\u124935\OneDrive - Finance of America Holdings, LLC\Documents\_My Repos\PythonOOP\Python\Python Scripts\TabTornado\links.txt') as file:
    links = file.readlines()
    for link in links: 
        webbrowser.open(link)
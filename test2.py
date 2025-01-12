from test import data
def reduc_first_line(text):
    for i in range(len(text)):
        if text[i]=='\n':
            return text[i+1:]
dt=data()
text="""
dfgdf
ggj
"""
print(reduc_first_line(text))
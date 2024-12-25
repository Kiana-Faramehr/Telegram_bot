list_t="""
👨‍🏫 Supervisor Information

• Supervisor: Dr Majid Ghaderi

🎓 Details of Open Research Position

👤 Computer Networks

🏅 Level: PhD & Masters
🌍 Country: Canada
🏛 University: University of Calgary
🔬 Branch: Department of Computer Science

📝 Overview:
Funding provider(s):  . My general research area is computer networks. Within this broader area, my focus is on design and optimization of network systems and algorithms.

🏷 Tags:
• Computer Science

🔗 Online Profiles:
• <a href='https://www.linkedin.com/in/mghaderi/'>LinkedIn</a>

• <a href='https://scholar.google.ca/citations?user=qZUQdpMAAAAJ&hl=en&oi=ao'>Google Scholar</a>

• <a href='http://www.cs.ucalgary.ca/~mghaderi'>University Profile</a>

    """
k=0
k1=0
for i in range(len(list_t)):
    if list_t[i]=='\n':
        k+=1
    if k==10 and k1==0:
        k1=i
    if k==11:
        print(len(list_t[k1+12:i]))
        break
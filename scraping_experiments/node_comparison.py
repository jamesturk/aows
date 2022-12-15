# node comparison

lx = Lxml()
lx.pre_parse()
bsoup = BSoup("html.parser")
bsoup.pre_parse()

lxml_elems = lx.count_elements("html5test") 
bsoup_elems = bsoup.count_elements("html5test")

print(len(lxml_elems), len(bsoup_elems))

for elem in lx.count_elements("html5test"):
    print(elem)
for elem in bsoup.count_elements("html5test"):
    print(elem)
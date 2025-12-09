import xml.etree.ElementTree as ET

tree = ET.parse("circuitoEsquema.xml")
root = tree.getroot()

print("Root:", root.tag)

print("\nPrimeros niveles del XML:\n")
for child in root:
    print("  ", child.tag)
    for sub in child:
        print("     ", sub.tag)
        for sub2 in sub:
            print("         ", sub2.tag)

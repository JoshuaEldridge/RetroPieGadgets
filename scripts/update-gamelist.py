#!/usr/bin/python
import lxml.etree as e
import re


auto_favorite = 0.90

#replace_paths = {"path":"", "cover":"", "image":"", "marquee":"", "video":""}
#replace_paths = {"image":["screenshots", "images"], "marquee":["marquees", "images"]}
replace_paths = {}

# The No-Intro rom names often have the country in parenthesis as part of the
# name. If you want to strip this off (which could leave duplicates if you chooses
# to keep mutiple country releases in the same folder), set this to true.
clean_name = True

remove_video_tag = True

def clean_nointro_name(old_name):
    return re.sub(r'[\s]*\([^)]*\)', '', old_name)

# This function is useful for updating the location of supporting files
# from one location to another
# Example: updated the image tag with a new directory containing screenshots
# find_replace("image", "screenshots", "images")
def find_replace(str, find, replace):
    return str.replace(find, replace, 1)

# Open original file
#tree = e.parse('/home/josh/Downloads/retropie/roms/nes/gamelist.xml')
tree = e.parse('/home/josh/Downloads/retropie/roms/snes/gamelist.xml')

if remove_video_tag is True:
    for bad in tree.xpath("//video"):
      bad.getparent().remove(bad)

root = tree.getroot()
for child in root:
    for i in child:
        if i.tag == "name":
            if clean_name is True:
                name = clean_nointro_name(i.text)
                #print i.tag, "||", i.text, "||", name
                i.text = name
        if i.tag in replace_paths and i.text is not None:
            #print replace_paths[i.tag], find_replace(i.text, replace_paths[i.tag][0], replace_paths[i.tag][1])
            i.text = find_replace(i.text, replace_paths[i.tag][0], replace_paths[i.tag][1])
        if i.tag == "rating" and i.text is not None:
            if float(i.text) >= auto_favorite:
                favorite_tag = e.Element("favorite")
                favorite_tag.text = "true"
                child.append(favorite_tag)

            #print name, i.text

print e.tostring(tree, pretty_print=True, xml_declaration=True)
tree.write('/home/josh/Downloads/retropie/roms/snes/test-gamelist.xml')

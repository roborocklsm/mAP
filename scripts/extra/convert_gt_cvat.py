import sys
import os
import glob
import xml.etree.ElementTree as ET

# make sure that the cwd() in the beginning is the location of the python script (so that every path makes sense)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# change directory to the one with the files to be changed
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
parent_path = os.path.abspath(os.path.join(parent_path, os.pardir))
GT_PATH = os.path.join(parent_path, 'input-cinderella','ground-truth')
#print(GT_PATH)
if not os.path.exists(GT_PATH):
  os.makedirs(GT_PATH)
os.chdir(GT_PATH)

# create VOC format files
XML_PATH = os.path.join(parent_path, 'input-cinderella','annotations','*','*.xml')
xml_list = glob.glob(XML_PATH)
if len(xml_list) == 0:
  print("Error: no .xml files found in {}".format(XML_PATH))
  sys.exit()
for xml_file in xml_list:
  #print(tmp_file)
  # 1. create new file (VOC format)
  tree = ET.parse(xml_file)
  root = tree.getroot()
  for info in root.findall("image"):
    boxes = info.findall("box")
    path = info.attrib["name"]
    path = '_'.join(path.split('/')[2:])
    path = path.split('.')[0] + '.txt'
    if os.path.exists(path):
      os.remove(path)
    if boxes != []:
      with open(path, "a") as new_f:
        for obj in boxes:
          obj_name = obj.attrib['label']
          left = obj.attrib['xtl']
          top = obj.attrib['ytl']
          right = obj.attrib['xbr']
          bottom = obj.attrib['ybr']
          if obj_name == "pedestrian":
            if abs(float(bottom) - float(top)) < 40 or abs(float(right) - float(left)) < 40:
              continue
          if obj_name == "vehicle":
            if abs(float(bottom) - float(top)) < 120 or abs(float(right) - float(left)) < 120:
              continue
          new_f.write("%s %s %s %s %s\n" % (obj_name, left, top, right, bottom))
print("Conversion completed!")

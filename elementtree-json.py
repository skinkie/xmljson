import types

try:
  from lxml import ET
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as ET
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as ET
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as ET
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as ET
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

def splitNameSpace(tag):
    if tag[0] == "{":
        return tag[1:].split("}")
    else:
        return None, tag

def parseAttributes(attribs):
    ns = set()
    for attrib in attribs.keys():
        if ':' in attrib:
            ns.add(attrib.split(':')[0])
    if len(ns) == 0:
        return attribs
    else:
        result = {}
        for x in ns:
            result[x] = {}
        for attrib, value in attribs.items():
            if ':' in attrib:
                thisns, tag = attrib.split(':')
                result[thisns]['@'+tag] = value
            else:
                result[attrib] = value
        return result

def parseChildren(tags):
    final = {}

    for x in tags:
        prepend = {}
        result = ''
        uri, tag = splitNameSpace(x.tag)

        if uri is not None:
            prepend['$$'] = uri

        if len(x.attrib) > 0:
            prepend = dict(prepend.items() + parseAttributes(x.attrib).items())
                
        if len(x) == 0:
            if x.text is not None:
                if len(prepend) == 0:
                    result = x.text
                else:
                    result = dict(prepend.items() + { "$": x.text }.items())
            else:
                if len(prepend) > 0:
                    result = prepend

        else:
            if len(prepend) == 0:
                result = { "$" : parseChildren(x.getchildren()) }
            else:
                result = dict(prepend.items() + { "$" : parseChildren(x.getchildren()) }.items())

        if tag in final:
            if type(final[tag]) is not types.ListType:
                final[tag] = [final[tag]]

            final[tag].append(result)
        else:
            final[tag] = result

    return final

#print parseChildren([ET.XML('<tag>txt-value</tag>')])
#print parseChildren([ET.XML('<tag><tag2>txt-value</tag2></tag>')])
#print parseChildren([ET.XML('<tag><tag2>txt-value1</tag2><tag2>txt-value2</tag2></tag>')])
#print parseChildren([ET.XML('<tag ns="ns-value" />')])
#print parseChildren([ET.XML('<tag xmlns:ns="ns-value" />')])
#print parseChildren([ET.XML('<tag xmlns="root-value" xmlns:ns="ns-value" />')])
#print parseChildren([ET.XML('<ns:tag attr="attr-value" />')])
#print parseChildren([ET.XML('<tag attr="attr-value">txt-value</tag>')])
#print parseChildren([ET.XML('<ns:tag attr="attr-value">txt-value</tag>')])
import sys

x = ET.parse(sys.argv[1]).getroot()
print parseChildren([x])
print ET.tostring(x)



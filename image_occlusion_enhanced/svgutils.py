# -*- coding: utf-8 -*-
####################################################
##                                                ##
##           Image Occlusion Enhanced             ##
##                                                ##
##        Copyright (c) Glutanimate 2016          ##
##       (https://github.com/Glutanimate)         ##
##                                                ##
##     Original Image Occlusion 2.0 add-on is     ##
##         Copyright (c) 2012-2015 tmbb           ##
##           (https://github.com/tmbb)            ##
##                                                ##
####################################################

import os
import base64
import urllib


from Imaging.PIL import Image 
import etree.ElementTree as etree

labels_layer_index = 0
shapes_layer_index = 1

# Make sure to use correct namespace
svg_ns = "http://www.w3.org/2000/svg"
etree.register_namespace("",svg_ns)
svg_ns = '{' + svg_ns + '}'

def strip_attributes(root, attrs, match=None):
    title = None
    if not match:
        for elt in root.iter():
            for attr in attrs:
                elt.attrib.pop(attr, None)
        return
    for elt in root.iter():
        # only remove in matched groups
        try:
            title = elt.find(svg_ns + 'title').text
        except:
            pass
        if title in match:
            for attr in attrs:
                elt.attrib.pop(attr, None)


def imageProp(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return width, height

def svgToBase64(svg_path):
    doc = etree.parse(svg_path)
    svg = doc.getroot()
    svg_content = etree.tostring(svg)
    svg_b64 = "data:image/svg+xml;base64," + base64.b64encode(svg_content)
    return svg_b64

def parseStyle(s):
    """Create a dictionary from the value of an inline style attribute"""
    if s is None:
        return {}
    else:
        return dict([i.split(":") for i in s.split(";") if len(i)])

def formatStyle(a):
    """Format an inline style attribute from a dictionary"""
    return ";".join([att + ":" + str(val) for att, val in a.iteritems()])


def nr_of_shapes(svg, curr_shapes_index):
    return len(svg[curr_shapes_index]) - 1  # subtract one because of <title>

# Find shapes layer index
def get_shapes_layer_idx(svg):
    for idx,svg_ele in enumerate(svg):
        try:
            title = svg_ele.find(svg_ns + 'title').text
        except:
            title = None
        if title == "Masks" or title == "Shapes":
            return idx
            break

def set_color(elt, color):
    elt.attrib["fill"] = "#" + color

def set_id(elt, elmid):
    elt.attrib["id"] = elmid

def set_color_recursive(elt, color):
    for e in elt.iter():
        set_color(e, color)


##### Functions to generate filenames: ###################################
### ext is the file extension (e.g. 'svg', 'png')
def gen_fnames(q_or_a, dir, nr_of_cards, ext):

    def basename(i):
        return "{q_or_a} {i}.{ext}".format(q_or_a=q_or_a,
                                           i=str(i),
                                           ext=ext)

    return [os.path.join(dir, basename(i)) for i in xrange(nr_of_cards)]


# Question side of the cards:
def gen_fnames_q(dir, nr_of_cards, ext):
    return gen_fnames('Q', dir, nr_of_cards, ext)


# Answer side of the cards:
def gen_fnames_a(dir, nr_of_cards, ext):
    return gen_fnames('A', dir, nr_of_cards, ext)
###########################################################################
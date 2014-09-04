# -*- coding: utf-8 -*-

import requests
from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import json

app = Flask(__name__)


def get_namespace(root):
    try:
        index = root.tag.index('}')
        return root.tag[0:index + 1]
    except ValueError:
        return ''


def flatten_layers(layers, parent=None):
    flattened = []
    for layer in layers:

        if layer.get('name', None):
            flattened.append(layer)

        if layer.get('children', None):
            children = flatten_layers(layer['children'], layer)
            flattened += children
            del layer['children']
    return flattened


def parse_layer(layer, namespace):
    try:
        name = layer.find('%sName' % namespace).text
    except AttributeError:
        name = None

    times = None
    try:
        dimensions = layer.findall('%sExtent' % namespace)
        for dimension in dimensions:
            #print dimension.attrib.get('name', None)
            if dimension.attrib.get('name', None) == 'TIME':
                times = dimension.text.split(',')
                break
    except AttributeError:
        times = None

    return {'name': name, 'times': times}


def find_layers(element, namespace):
    layers = []
    if element is not None:
        for layer in element.findall('%sLayer' % namespace):
            layer_dict = parse_layer(layer, namespace)
            layer_dict['children'] = find_layers(layer, namespace)
            layers.append(layer_dict)
    layers = flatten_layers(layers)
    return [layer for layer in layers if layer.get('times', None) is not None]


def get_layer_list():
    url = 'http://bw-wms.met.no/barentswatch/default.map?&service=wms&version=1.1.1&request=getCapabilities'
    data = requests.get(url, headers={'Accept': 'application/xml'}).content
    root = ET.fromstring(data)
    namespace = get_namespace(root)

    capability = root.find('.//%sCapability' % namespace)
    return find_layers(capability, namespace)


def get_times(layer_name):
    layers = get_layer_list()
    for layer in layers:
        if layer['name'] == layer_name:
            return layer


@app.route('/')
def map():
    layer = request.args.get('layer', None)

    if not layer:
        return render_template(
            'list.html',
            layers=get_layer_list()
        )

    layer = get_times(layer)
    if layer:
        return render_template(
            'index.html',
            layer_name=layer['name'],
            times=json.dumps(layer['times'])
        )

if __name__ == '__main__':
    app.run(debug=True)

#!usr/bin/env python
import macos_tags

def apply_tag(tag_name, path):
    tag = tag_name
    macos_tags.add(tag, file=path)

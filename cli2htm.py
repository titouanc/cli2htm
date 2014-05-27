#!/usr/bin/env python

class Converter(object):
    class TagError(Exception):
        pass

    def __init__(self, inline_style=True):
        self.inline_style = inline_style
        self.tag_stack = []

    def mkColor(self, console_color):
        color = int(console_color)
        r, g, b = color&0x1, (color&0x2)>>1, (color&0x4)>>2
        return '#%x%x%x'%tuple(c*0xf for c in (r, g, b))

    def tag2html(self, tag, closing):
        html = ''
        if tag == '1':
            html = 'b'
        elif tag[0] in '34':
            html = 'span' 
            if not closing:
                if self.inline_style:
                    html += ' style="'
                    if tag[0] == '4':
                        html += 'background-'
                    html += 'color:%s;"'%(self.mkColor(tag[1]))
                else:
                    html += ' class="cli%s"'%(tag)
        if closing:
            return '</%s>'%(html)
        return '<%s>'%(html)

    def convert_tag(self, string):
        m = string.find("m", self.end)
        if m < self.end:
            raise TagError()
        attributes = string[self.end+2:m]
        res = []
        for tag in attributes.split(';'):
            if tag == '0':
                res.append(self.close_all_tags())

            elif tag[-1] == '0':
                res.append(self.close_last_tag())

            elif not self.is_same_tag(tag):
                if self.is_same_tag_type(tag):
                    res.append(self.close_last_tag())
                self.tag_stack.append(tag)
                res.append(self.tag2html(tag, closing=False))
        self.begin = m+1
        return ''.join(res)

    def is_same_tag_type(self, tag):
        if self.tag_stack:
            last = self.tag_stack[-1]
            return last[0] == tag[0]
        return False

    def is_same_tag(self, tag):
        if self.tag_stack:
            return self.tag_stack[-1] == tag
        return False

    def close_last_tag(self):
        return self.tag2html(self.tag_stack.pop(), closing=True)

    def close_all_tags(self):
        return ''.join(self.close_last_tag() for i in range(len(self.tag_stack)))

    def convert_string(self, string):
        self.begin, self.end = 0, 0
        res = []
        found = string.find("\033[")
        while found >= 0:
            # First: copy the unmodified part
            self.end = found
            res.append(string[self.begin:self.end].replace('\n', '<br/>'))
            res.append(self.convert_tag(string))
            found = string.find("\033[", self.begin)
        res.append(string[self.begin:].replace('\n', '<br/>'))
        res += self.close_all_tags()
        return ''.join(res)

def convert(string, *args, **kwargs):
    return Converter(*args, **kwargs).convert_string(string)

if __name__ == "__main__":
    from sys import stdin, stdout
    import argparse
        
    optparser = argparse.ArgumentParser(
        description="Convert ANSI terminal output to HTML"
    )
    optparser.add_argument(
        '-c', '--context',
        action='store_true', dest='context', default=False,
        help="Print contextual HTML around converted text (html mandatory tags and a bit of css)"
    )
    optparser.add_argument(
        '-o', '--output', type=str,
        action='store', dest='output', default=None,
        help="Output file (defaults to stdout)"
    )
    optparser.add_argument(
        '-i', '--input', type=str,
        action='store', dest='input', default=None,
        help="Input file (defaults to stdin)"
    )
    optparser.add_argument(
        '-s', '--style', type=str,
        action='store', dest='css', default=None,
        help="Fill style section with the content of this file (when -c is activated)"
    )
    optparser.add_argument(
        '-I', '--inline',
        action='store_true', dest='inline', default=False,
        help="Use HTML inline style instead of classes (<span style='color:#f00;'> instead of <span class='cli30'>)"
    )
    OPTIONS = optparser.parse_args()

    input, output = stdin, stdout
    if OPTIONS.input:
        input = open(OPTIONS.input)
    if OPTIONS.output:
        output = open(OPTIONS.output, 'w')

    converter = Converter(inline_style=OPTIONS.inline)
    if not OPTIONS.inline:
        if OPTIONS.css:
            STYLE = open(OPTIONS.css).read()
        else:
            STYLE = ".cli{color:#fff;background-color:#000;font-family:courier;}"
            for i in range(1, 8):
                STYLE += ".cli3%d{color:%s;}"%(i, converter.mkColor(str(i)))
            for i in range(1, 8):
                STYLE += ".cli4%d{background-color:%s;}"%(i, converter.mkColor(str(i)))

    if OPTIONS.context:
        output.write('<!DOCTYPE html>')
        output.write('<html><head>')
        if not OPTIONS.inline:
            output.write('<style type="text/css">'+STYLE+'</style>')
        output.write('</head><body><div class="cli">')
    output.write(convert(stdin.read(), OPTIONS.inline))
    if OPTIONS.context:
        output.write('</div></body></html>')
    output.write('\n')
    
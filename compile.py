import re
import codecs
import pdb

SRE_MATCH_TYPE = type(re.match("", ""))

def expand(match, value):
  if isinstance(value, str) or isinstance(value, unicode):
    return match.expand(value)
  if isinstance(value, Compilation):
    results = {}
    for k, v in value.objects.items():
      expanded = expand(match, v)
      if expanded is not None:
        results[k] = expanded
    return compile_all(value.template, results)
  if isinstance(value, tuple):
    return value[1](match.expand(value[0]))
  return value

def indentize(content, indentation):
  indent = u' ' * indentation
  result = []
  for i, line in enumerate(content.split(u'\n')):
    if i == 0:
      result += [line]
    else:
      result += [indent + line]
  return u'\n'.join(result)

def compile_all(fn, vars):
  def get_template(obj):
    # get out of regexp
    indents = 0
    if type(obj) is SRE_MATCH_TYPE:
      i = obj.start(0) - 1
      indents = 0
      while obj.string[i] == ' ':
        indents += 1
        i -= 1
      obj = obj.group(1)
    if obj.endswith('.html') or obj.endswith('.css'):
      with codecs.open(obj, 'r', 'utf-8') as f:
        return f.read() if indents == 0 else indentize(f.read(), indents)
    if vars.has_key(obj):
      return str(vars[obj])
    for key, value in vars.items():
      match = re.match(key, obj)
      if match:
        return expand(match, value)
    return '{' + obj + '}'

  def conditional(match):
    conditions = [condition.strip() for condition in match.group(1).split(',')]
    results = []
    for condition in conditions:
      param, output = [c.strip() for c in condition.split(':')]
      if param in vars.keys():
        results += [re.sub(u'{{ *(.*) *}}', compile, output)]
    return ' '.join(results)

  def compile(obj):
    contents = get_template(obj)
    contents = re.sub(u'{% *(.*?) *%}', conditional, contents)
    return re.sub(u'{{ *(.*?) *}}', compile, contents)

  return compile(fn)

class Compilation(object):
  def __init__(self, template, objects):
    self.template = template
    self.objects = objects
  def compile(self):
    return compile_all(self.template, self.objects)

def compile_to_file(fn, vars, output_fn):
  with codecs.open(output_fn, 'w', 'utf-8') as f:
    f.write(compile_all(fn, vars))
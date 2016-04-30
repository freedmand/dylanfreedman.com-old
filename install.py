import subprocess
import os, codecs, sys
from compile import compile_to_file, Compilation
import SimpleHTTPServer
import SocketServer
import datetime

INPUT_SVG_DIR = 'svg'
SVG_EXTENSION = '.svg'

OUTPUT_PNG_DIR = 'output/png'
PORT = 8080

def svg_convert():
  for svg_fn in get_svg_files():
    subprocess.call(["convert", "-density", "1200", svg_fn[0], os.path.join(OUTPUT_PNG_DIR, "%s.png" % svg_fn[1])])

def get_svg_files():
  for dirpath, dirnames, filenames in os.walk(INPUT_SVG_DIR):
    for fn in filenames:
      if fn.endswith(SVG_EXTENSION):
        yield (os.path.join(dirpath, fn), fn[:-len(SVG_EXTENSION)])

svg_heights = {
  'background': 800
}

svg_widths = {
  'bullet': 30,
  'bullet-music': 33,
  'bullet-design': 33,
  'bullet-projects': 33,
  'bullet-hobbies': 39,
  'footer-email': 30,
  'footer-github': 32,
}

colors = {
  'gray': '#6D6E71',
  'light-gray': '#A09F9F',
  'dark-gray': '#414042',
  'dark-dark-gray': '#333132',

  # 'faded-orange': '#FFF4DD', # writing
  # 'faded-blue': '#DDF2FF', # programming
  # 'faded-purple': '#E0DDFF', # projects
  # 'faded-green': '#DDFFE0', # graphic design
  # 'faded-pink': '#FFDDE7', # music
  # 'faded-sky': '#DDFEFF', # hobbies
  # 'faded-gold': '#FFF8DD', # experience

  'faded-orange': '#FBDA4F', # writing
  'faded-blue': '#ABCFFF', # programming
  'faded-purple': '#D0CCFF', # projects
  'faded-green': '#7DECAC', # graphic design
  'faded-pink': '#FFBFBF', # music
  'faded-sky': '#A5E8FF', # hobbies
  'faded-gold': '#FFE1B8', # experience

  # 'blue': '#6905FB', # programming
  # 'pink': '#CE0303', # music
  # 'orange': '#FD902B', # writing
  # 'green': '#20D06A', # graphic design
  # 'purple': '#2788E2', # projects
  # 'gold': '#EBAE20', # experience
  # 'sky': '#A5E8FF', # hobbies

  'coding': '#0D579B', # programming
  'music': '#984120', # music
  'writing': '#FBA919', # writing
  'design': '#00646E', # graphic design
  'projects': '#834C9E', # projects
  'experience': '#FF7700', # experience
  'hobbies': '#ED1C24', # hobbies

  'accent': '#EF7A22', # characteristic orange
}

year = datetime.datetime.now().year

def get_param(params, s):
  if params.has_key(s):
    return params[s]
  if '-' in s:
    s = '-'.join(s.split('-')[:-1])
    return get_param(params, s)
  return None

# compile the HTML page
compile_to_file('template.html',
  {'(.*)(\.svg)':
    Compilation('image.html',
      {'src': r'svg/\1\2',
       'height': (r'\1', lambda x: get_param(svg_heights, x)),
       'width': (r'\1', lambda x: get_param(svg_widths, x))
      }
    ),
    'year': year
  },
  'output/index.html'
)

compile_to_file('main.css',
  {
    'color-(.*)': (r'\1', lambda x: colors.get(x))
  },
  'output/main.css'
)

compile_to_file('resume.html',
  {},
  'output/resume.html'
)

print 'file://' + os.path.abspath('output/index.html')

if '-s' in sys.argv:
  # start the http server
  os.chdir('output')
  Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
  httpd = SocketServer.TCPServer(("", 8080), Handler)

  print "serving at port", PORT
  httpd.serve_forever()

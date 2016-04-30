import re
import os

output = 'icons'

def output_svg(lines):
  contents = """<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
  viewBox="-659.4 300.85 520.4 520.3" style="enable-background:new -659.4 300.85 520.4 520.3;" xml:space="preserve">
  <style type="text/css">
    .st0{fill:#A09F9F;}
    .st1{fill:#6D6E71;}
  </style>

  """

  contents += '<g>\n' + '\n'.join(lines) + '\t</g>'
  contents += """

</svg>"""
  return contents

with open('footers.svg', 'r') as f:
  contents = f.read()

  for className, lines in re.findall('<g class="(.*?)">(.*?)</g>', contents, re.DOTALL):
    lines = lines.split('\n')
    st0 = [l for l in lines if 'class="st0"' in l]
    st1 = [l for l in lines if 'class="st1"' in l]

    fn = os.path.join(output, className)
    with open(fn + '-0.svg', 'w') as f2:
      f2.write(output_svg(st0))
    with open(fn + '-1.svg', 'w') as f2:
      f2.write(output_svg(st1))

print 'Done'
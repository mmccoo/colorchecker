

import re
import pdb
import sys


# width is 3x2 + 2x5 + 20x6 = 6+10+120 = 136
# height is 3x2 + 2x3 + 20x4 = 6+6+80 = 92

xoffset = 13
yoffset = 13
width = xoffset*2 + 2*5 + 20*6
height = yoffset*2 + 2*3 + 20*4

def svg_header(fp):
    fp.write("""
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="{}mm"
   height="{}mm"
   version="1.1"
>

    <rect
       style="fill:#dfdfdf;fill-opacity:1;"
       width="{}mm"
       height="{}mm"
       x="0mm"
       y="0mm" />
""".format(width, height, width, height))

def svg_footer(fp):
    fp.write("""

</svg>
""")



# dark skin
# 113 82 67

filename = "../colornerd/csv/ral.csv"
with open(filename) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

macbeth_colors = {
    #                  Munsell             CIE xyY             srgb D50 values
    "Dark skin"     : ("3 YR 3.7/3.2"    , 0.400, 0.350, 10.1, 0x735244),
    "Light skin"    : ("2.2 YR 6.47/4.1" , 0.377, 0.345, 35.8, 0xc29682),
    "Blue sky"      : ("4.3 PB 4.95/5.5" , 0.247, 0.251, 19.3, 0x627a9d),
    "Foliage"       : ("6.7 GY 4.2/4.1"  , 0.337, 0.422, 13.3, 0x576c43),
    "Blue flower"   : ("9.7 PB 5.47/6.7" , 0.265, 0.240, 24.3, 0x8580b1),
    "Bluish green"  : ("2.5 BG 7/6"      , 0.261, 0.343, 43.1, 0x67bdaa),
    "Orange"        : ("5 YR 6/11"       , 0.506, 0.407, 30.1, 0xd67e2c),
    "Purplish blue" : ("7.5 PB 4/10.7"   , 0.211, 0.175, 12.0, 0x505ba6),
    "Moderate red"  : ("2.5 R 5/10"      , 0.453, 0.306, 19.8, 0xc15a63),
    "Purple"        : ("5 P 3/7"         , 0.285, 0.202, 6.6 , 0x5e3c6c),
    "Yellow green"  : ("5 GY 7.1/9.1"    , 0.380, 0.489, 44.3, 0x9dbc40),
    "Orange yellow" : ("10 YR 7/10.5"    , 0.473, 0.438, 43.1, 0xe0a32e),
    "Blue"          : ("7.5 PB 2.9/12.7" , 0.187, 0.129, 6.1 , 0x383d96),
    "Green"         : ("0.25 G 5.4/9.6"  , 0.305, 0.478, 23.4, 0x469449),
    "Red"           : ("5 R 4/12"        , 0.539, 0.313, 12.0, 0xaf363c),
    "Yellow"        : ("5 Y 8/11.1"      , 0.448, 0.470, 59.1, 0xe7c71f),
    "Magenta"       : ("2.5 RP 5/12"     , 0.364, 0.233, 19.8, 0xbb5695),
    "Cyan"          : ("5 B 5/8"         , 0.196, 0.252, 19.8, 0x0885a1),
    "White"         : ("N 9.5/"          , 0.310, 0.316, 90.0, 0xf3f3f2),
    "Neutral 8"     : ("N 8/"            , 0.310, 0.316, 59.1, 0xc8c8c8),
    "Neutral 6.5"   : ("N 6.5/"          , 0.310, 0.316, 36.2, 0xa0a0a0),
    "Neutral 5"     : ("N 5/"            , 0.310, 0.316, 19.8, 0x7a7a7a),
    "Neutral 3.5"   : ("N 3.5/"          , 0.310, 0.316, 9.0 , 0x555555),
    "Black"         : ("N 2/"            , 0.310, 0.316, 3.1 , 0x343434)
}

RAL_colors = {}
for line in content:
    # "Green Beige","1000","#bebd7f"
    #print(line)

    m = re.match(r'"(.*)","(.*)","(.*)"', line)
    name =  m.group(1)
    num  =  m.group(2)
    color = m.group(3)

    r = int(color[1:3],16)
    g = int(color[3:5],16)
    b = int(color[5:7],16)

    RAL_colors[num] = (name, r, g, b)
    #print("{} {} {} {} {} {} \n".format(m.group(1), m.group(2), m.group(3), r, g, b))


row = 0
col = 0

fp = open('mygenerated.svg', 'w')
svg_header(fp)

for m_color_name, m_color in macbeth_colors.items():

    mr = int((m_color[4] & 0xFF0000) >> 16)
    mg = int((m_color[4] & 0xFF00)   >>  8)
    mb = int((m_color[4] & 0xFF)          )

    print("mac color {} {} {} {}".format(m_color_name, mr, mg, mb))

    min_dist = -1
    best = None

    for r_id in RAL_colors:
        r_color = RAL_colors[r_id]

        name, rr, rg, rb = r_color;
        #print("ral color {} {} {} {}".format(name, rr, rg, rb))

        dist = max(abs(mr-rr), abs(mg-rg), abs(mb-rb));

        if (min_dist==-1 or dist<min_dist):
            min_dist = dist
            best = r_id


    print("   Best is {} {} with dist {}".format(best, RAL_colors[best], min_dist))
    fp.write('    <rect style="fill:#{:02X}{:02X}{:02X};fill-opacity:1;stroke:none" width="20mm" height="20mm" x="{}mm" y="{}mm" />\n'
             .format(int(RAL_colors[best][1]), int(RAL_colors[best][2]), int(RAL_colors[best][3]),
                     xoffset+col*22, yoffset+row*22))

    fp.write('    <text xml:space="preserve"\n')
    fp.write('          style="font-style:normal;font-weight:normal;font-size:8px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"\n')
    fp.write('          x="{}mm" y="{}mm">\n'.format(-5+xoffset+col*22, yoffset+row*22))
    fp.write('     {} {} \n'.format(best, RAL_colors[best][0]))
    fp.write('    </text>\n')
    col = col + 1
    if (col>=6):
        col = 0
        row = row + 1

svg_footer(fp)
fp.close()

def comp_grey(a):
    color = RAL_colors[a]
    greynessa = max(int(color[1]), int(color[2]), int(color[3])) - min(int(color[1]), int(color[2]), int(color[3]))
    return greynessa



greys = sorted(RAL_colors, key=comp_grey)

for grey in greys[0:10]:
    color = RAL_colors[grey]
    print("grey {} {} ".format(grey, color))

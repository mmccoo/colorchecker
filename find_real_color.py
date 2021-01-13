
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re

import colormath

import pdb

def read_color_vals(filename):

    with open(filename) as f:
        content = f.readlines()

    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    colors = {}

    indata = False
    for line in content:
        if (line == "BEGIN_DATA"):
            indata = True
            continue

        if (line == "END_DATA"):
            break

        if (not indata):
            continue

        vals = line.split()
        label = re.sub(r'^([a-zA-Z]+)0*([0-9]+)', r'\1\2', vals[0])

        colors[label] = np.array([float(n) for n in vals[1:]])

    return colors

def show_colors(sp, colors):
    r = np.array([c[0] for c in colors.values()])
    g = np.array([c[1] for c in colors.values()])
    b = np.array([c[2] for c in colors.values()])

    sp.scatter(r,g,b)


basename = "IMG_1956"
basename = "2021-01-01-0001_"
it8_scanned_colors     = read_color_vals(basename + "it8.val")
mygen_scanned_colors   = read_color_vals(basename + "mygenerated.val")

mygen_reference_colors = read_color_vals("../common_files/mygenerated.val")
it8_reference = read_color_vals("../common_files/R170830.txt")


# this section translates the LAB/XYZ colors in the reference file to RGB values.
it8_reference_colors = {}
for rcolor in it8_reference:
    lab = it8_reference[rcolor][3:6]

    xyz = colormath.LAB_XYZ(*list(lab))
    rgb = colormath.XYZ_RGB(*xyz)

    it8_reference_colors[rcolor] = np.array(rgb)
    if 0:
        print("{} should be at {} but is really at {} with dist {}".format(rcolor,
                                                                           it8_reference_colors[rcolor],
                                                                           it8_scanned_colors[rcolor],
                                                                           distance.euclidean(it8_reference_colors[rcolor],
                                                                                              it8_scanned_colors[rcolor])
                                                                           ))

# Here I normalize the it8 scanned colors so the extremes of the white scale match.
# I compute the needed offset and scaling

white_scanned = it8_scanned_colors['GS0']
white_ref = it8_reference_colors['GS0']
black_scanned = it8_scanned_colors['GS23']
black_ref = it8_reference_colors['GS23']
print("white is scanned at {} but should be {}".format(white_scanned,
                                                       white_ref))
print("black is scanned at {} but should be {}".format(black_scanned,
                                                       black_ref))
print("scanned dist {} ref dist{}".format(abs(white_scanned-black_scanned), abs(white_ref-black_ref)))
print("scanned ave {} ref ave {}".format(np.average(abs(white_scanned-black_scanned)),
                                         np.average(abs(white_ref-black_ref))))

scale_factor = np.average(abs(white_ref-black_ref))/np.average(abs(white_scanned-black_scanned))
offset = np.average(black_ref-black_scanned)

print("scale factor {} offset {}".format(scale_factor, offset))

print("black scanned {}\nblack adjusted {}\nblack ref{}".format(black_scanned,
                                                                (black_scanned+offset)*scale_factor,
                                                                black_ref))
print("white scanned {}\nwhite adjusted {}\nwhite ref{}".format(white_scanned,
                                                                (white_scanned+offset)*scale_factor,
                                                                white_ref))

for mcolor in mygen_scanned_colors:
    mygen_scanned_colors[mcolor] = (mygen_scanned_colors[mcolor]+offset)*scale_factor;

for it8 in it8_scanned_colors:
    it8_scanned_colors[it8] = (it8_scanned_colors[it8]+offset)*scale_factor;


for mcolor in mygen_scanned_colors:

    mvals = mygen_scanned_colors[mcolor]

    def dist_fn(color):
        dist = max(abs(mvals-it8_scanned_colors[color]))
        return dist

    closest = sorted(it8_scanned_colors.keys(), key=dist_fn)

    print("closest to {}:{}".format(mcolor, mygen_scanned_colors[mcolor]))

    c1 = closest[0]
    it8_1 = it8_scanned_colors[c1]
    print("       is  {}:{} dist:{}".format(c1, it8_1, dist_fn(c1)))

    for c2 in closest[1:]:
        it8_2 = it8_scanned_colors[c2]
        #if ((it8_1<=mvals) == (mvals <= it8_2)).all():
        print("       and {}:{} dist:{}".format(c2, it8_2, dist_fn(c2)))

        # if x*c1 + (1-x)*c2 = mvals
        # x(c1-c2) + c2      = mvals
        # x = mvals-c2
        #     --------
        #     (c1-c2)
        coeff = (mvals-it8_2)/(it8_1-it8_2)

        print("    coeff {} {}".format(coeff,coeff*it8_1+(1-coeff)*it8_2))

        interpolated_real = coeff*it8_reference_colors[c1] + (1-coeff)*it8_reference_colors[c2];

        print("    {} ref is {}\n    {} ref is {}.\n    applying to ref values, mine is {}".format(c1,it8_reference_colors[c1],
                                                                                            c2,it8_reference_colors[c2],
                                                                                            interpolated_real))
        print("    real should be {} with dist {}".format(mygen_reference_colors[mcolor],
                                                          max(abs(mygen_reference_colors[mcolor]-mygen_scanned_colors[mcolor]))))

        break


exit(0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
show_colors(ax, mygen_scanned_colors)
#ax = fig.add_subplot(121, projection='3d')
show_colors(ax, it8_scanned_colors)


plt.show()


print("done")



# darktable chart uses D65. Faust it8 uses D50
ref  = "D50"


if (ref == "D65"):
    # http://www.easyrgb.com/en/math.php#text8
    #         2degree                      10degree
    #         X        Y         Z
    # D65     95.047   100.000   108.883   94.811  100.000  107.304  Daylight, sRGB, Adobe-RGB
    Reference_X = 95.047
    Reference_Y = 100.000
    Reference_Z = 108.883

if (ref == "D50"):
    # D50     96.422   100.000   82.521    96.720   100.000  81.427  ICC profile PCS
    Reference_X =  96.422
    Reference_Y = 100.000
    Reference_Z =  82.521

def XYZ_RGB(X, Y, Z):
    # X, Y and Z input refer to a D65/2° standard illuminant.
    # sR, sG and sB (standard RGB) output range = 0 ÷ 255

    var_X = X / 100
    var_Y = Y / 100
    var_Z = Z / 100

    var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
    var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570

    if ( var_R > 0.0031308 ):
        var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_R = 12.92 * var_R

    if ( var_G > 0.0031308 ):
        var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_G = 12.92 * var_G

    if ( var_B > 0.0031308 ):
        var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_B = 12.92 * var_B

    sR = var_R * 255.0
    sG = var_G * 255.0
    sB = var_B * 255.0

    return (sR, sG, sB)


def RGB_XYZ(sR, sG, sB):
    # sR, sG and sB (Standard RGB) input range = 0 ÷ 255
    # X, Y and Z output refer to a D65/2° standard illuminant.

    var_R = ( sR / 255.0 )
    var_G = ( sG / 255.0 )
    var_B = ( sB / 255.0 )

    if ( var_R > 0.04045 ):
        var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_R = var_R / 12.92

    if ( var_G > 0.04045 ):
        var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_G = var_G / 12.92

    if ( var_B > 0.04045 ):
        var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100.0
    var_G = var_G * 100.0
    var_B = var_B * 100.0

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    return (X, Y, Z)


def LAB_XYZ(CIE_L, CIE_A, CIE_B):
    # Reference-X, Y and Z refer to specific illuminants and observers.
    # Common reference values are available below in this same page.

    var_Y = ( CIE_L + 16 ) / 116.0
    var_X = CIE_A / 500.0 + var_Y
    var_Z = var_Y - CIE_B / 200.0

    if ( var_Y**3.0  > 0.008856 ):
        var_Y = var_Y**3
    else:
        var_Y = ( var_Y - 16 / 116.0 ) / 7.787

    if ( var_X**3  > 0.008856 ):
        var_X = var_X**3
    else:
        var_X = ( var_X - 16 / 116.0 ) / 7.787

    if ( var_Z**3  > 0.008856 ):
        var_Z = var_Z**3
    else:
        var_Z = ( var_Z - 16 / 116.0 ) / 7.787

    X = var_X * Reference_X
    Y = var_Y * Reference_Y
    Z = var_Z * Reference_Z

    return (X, Y, Z)


def XYZ_LAB(X, Y, Z):
    # Reference-X, Y and Z refer to specific illuminants and observers.
    # Common reference values are available below in this same page.

    var_X = X / Reference_X
    var_Y = Y / Reference_Y
    var_Z = Z / Reference_Z

    if ( var_X > 0.008856 ):
        var_X = var_X ** ( 1/3.0 )
    else:
        var_X = ( 7.787 * var_X ) + ( 16 / 116.0 )

    if ( var_Y > 0.008856 ):
        var_Y = var_Y ** ( 1/3.0 )
    else:
        var_Y = ( 7.787 * var_Y ) + ( 16 / 116.0 )

    if ( var_Z > 0.008856 ):
        var_Z = var_Z ** ( 1/3.0 )
    else:
        var_Z = ( 7.787 * var_Z ) + ( 16 / 116.0 )

    CIE_L = ( 116 * var_Y ) - 16
    CIE_a = 500 * ( var_X - var_Y )
    CIE_b = 200 * ( var_Y - var_Z )

    return (CIE_L, CIE_a, CIE_b)

if __name__ == "__main__":
    cie_lab = (22.03, 10.35, 2.08)
    #cie_lab = (19.29, 10.86, 3.40)
    print("LAB {}\nXYZ {}\nRGB {}\n\n".format(cie_lab, LAB_XYZ(*cie_lab), XYZ_RGB(*LAB_XYZ(*cie_lab))))

    rgb = XYZ_RGB(*LAB_XYZ(*cie_lab))
    print("RGB {}\nXYZ {}\nRGB {}".format(rgb, RGB_XYZ(*rgb), XYZ_RGB(*RGB_XYZ(*rgb))))

    print("LAB {}\nXYZ {}\nLAB {}\n\n".format(cie_lab, LAB_XYZ(*cie_lab), XYZ_LAB(*LAB_XYZ(*cie_lab))))

    xyz = (3.340000, 2.810000, 1.950000)
    print("\nXYZ {}\nRGB {}".format(xyz, XYZ_RGB(*xyz)))

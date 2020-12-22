#  16-image tracing tool
#  convert the binary edge image to svg
import os
import sys
import cairosvg


def bin2svg(i, o):
    platform = sys.platform
    auto_trace = r'autotrace'
    if platform == 'win32':
        auto_trace = r'autotrace.exe'
    config = [
        '--background-color 000000',
        '--centerline',
        '--output-file',
        o,
        '--output-format svg',
        i
    ]
    line = ' '.join([auto_trace] + config)
    os.system(line)


def svg2img(svg, img):
    cairosvg.svg2png(url=svg, write_to=img)

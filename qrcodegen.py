from argparse import ArgumentParser
from argparse import Namespace

import PIL
import qrcode.constants
from PIL import Image
from qrcode import QRCode

def parse_args() -> Namespace:
  parser = ArgumentParser(description='A simple script to generate Qr Codes')
  parser.add_argument('-l', '--logo',
                      dest='logo',
                      required=False,
                      default=None,
                      help='An optional logo to insert in the middle of the generated qr code'
                      )
  parser.add_argument('-o', '--output-file',
                      dest='out_file',
                      required=False,
                      default=None,
                      help='An output file'
                      )
  parser.add_argument('-e', '--error-correction',
                      dest='error_correction',
                      required=False,
                      default='M',
                      choices=['L', 'M', 'Q', 'H'],
                      help='An output file'
                      )
  parser.add_argument('-d', '--data',
                      dest='data',
                      required=True,
                      type=str,
                      help='The data used to generate the qr code'
                      )

  return parser.parse_args()

def show_qrcode(qr: QRCode):
  from io import StringIO

  f = StringIO()
  qr.print_ascii(out=f)
  f.seek(0)
  print(f.read())

def export_qrcode(qr_img: PIL.Image, output_file: str):
  qr_img.save(output_file)

def add_logo_to_qrcode(logo: PIL.Image.Image, qr: QRCode):
  basewidth = 50
  wpercent = (basewidth / float(logo.size[0]))
  hsize = int((float(logo.size[1]) * float(wpercent)))
  logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

  qr_img = qr.make_image().convert('RGB')
  pos = ((qr_img.size[0] - logo.size[0]), (qr_img.size[1] - logo.size[1]))
  qr_img.paste(logo, pos)
  return qr_img

def main() -> None:
  args = parse_args()

  correction_level = {
    'L': qrcode.constants.ERROR_CORRECT_L,
    'M': qrcode.constants.ERROR_CORRECT_M,
    'Q': qrcode.constants.ERROR_CORRECT_Q,
    'H': qrcode.constants.ERROR_CORRECT_H
  }[args.error_correction]

  qr = QRCode(error_correction=correction_level)

  qr.add_data(args.data)

  qr_img = qr.make_image(fill_color='black', back_color='white')

  try:
    if args.logo is not None:
      logo = Image.open(args.logo, mode='r')
      qr_img = add_logo_to_qrcode(logo, qr)
  except FileNotFoundError:
    print("\x1b[31m[!] Error\x1b[0m: The logo file can not be found!")
  except PIL.UnidentifiedImageError:
    print("\x1b[31m[!] Error\x1b[0m: The logo file can not be open!")

  if args.out_file is None:
    show_qrcode(qr)
  else:
    export_qrcode(qr_img, args.out_file)

if __name__ == '__main__':
  main()

from PIL import Image
import requests
import io
from math import sqrt

def color_distance(rgb1, rgb2):
  """
    Function used to get the distance between two colors
  """
  rmean = int((rgb1[0] + rgb2[0]) / 2);
  r = rgb1[0] - rgb1[0]
  g = rgb1[1] - rgb2[1]
  b = rgb1[2] - rgb2[2]
  return sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

# The colors i will use
ASCII_COLORS = [
  [255, "█"],
  [192, "▓"],
  [128, "▒"],
  [ 64, "░"],
  [  0, " "],
]
# The size of the output
SIZE = (90, 45)

# The url of the image
url = input("url : ")

# Get the data of the image
try:
  response = requests.get(url)
except requests.exceptions.MissingSchema:
  print("Erreur lors de la lecture de l'url !")
  quit()

# Open it, convert it to the good size whitout deforming it, and make it B&W
image = Image.open(io.BytesIO(response.content))
image.thumbnail(SIZE)
image = image.convert("L")

# Get the real size
im_size = image.size

for y in range(int(im_size[1] / 3)):
  for x in range(im_size[0]):
    # For each pixel
    px = image.getpixel((x, y * 3))

    closer = 10e10
    shade = " "
    
    # For each availaible color, search for the closest
    for color in ASCII_COLORS:
      rgb = color[0]
      clositude = color_distance([rgb, rgb, rgb], [px, px, px])
      if clositude < closer:
        closer = clositude
        shade = color[1]

    # Print it whitout '\n'
    print(shade, end="")
  # Print a '\n'
  print("")

# Save it because why not
image.save("./your-image.png")
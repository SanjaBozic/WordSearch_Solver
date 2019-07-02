
import cv2
import time
import numpy as np

from PIL import Image
import pytesseract


DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
CANNY = 250

_width  = 600.0
_height = 420.0
_margin = 0.0

if USE_CAM: video_capture = cv2.VideoCapture(0)

corners = np.array(
	[
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
)

pts_dst = np.array( corners, np.float32 ) #pretvaranje u float array 

while True :

	if USE_CAM :
		ret, rgb = video_capture.read()

	if ( ret ):

		gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY ) #slika se pretvori u sivu

		gray = cv2.bilateralFilter( gray, 1, 10, 120 ) #za smanjenje sumova

		edges  = cv2.Canny( gray, 10, CANNY ) #pretvaranje slike u crno-bijelu, od slova se vide rubovi

		kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )

		closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel ) #morfoloski transformira sliku da su slova puna

		contours, h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE ) #funkcija preuzima konture iz binarne slike koristeći algoritam

		for cont in contours:

			if cv2.contourArea( cont ) > 5000 :

				arc_len = cv2.arcLength( cont, True ) #racunanje duljine konture

				approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True ) #aproksimacija krivulje ili poligona sa krivuljom ili poligonom koja ima manje vrhova

				if ( len( approx ) == 4 ):
					IS_FOUND = 1

					pts_src = np.array( approx, np.float32 ) #pretvaranje aproksimacije u np array

					h, status = cv2.findHomography( pts_src, pts_dst ) #ako nade 4 tocke trazi homografiju (trazi 4 odgovarajuce tocke u 2 ili vise frame-ova)

					out = cv2.warpPerspective( rgb, h, ( int( _width + _margin * 2 ), int( _height + _margin * 2 ) ) ) #kad je homografija pronadena moze se primijeniti transformacija na sve piksele jedne slike tako da bi se mapirala na drugoj slici

					cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 ) #crta obrise kontura, thickness 2 

				else : pass

		#cv2.imshow( 'closed', closed )
		#cv2.imshow( 'gray', gray )
		cv2.namedWindow( 'edges')
		cv2.imshow( 'edges', edges )

		cv2.namedWindow( 'rgb')
		cv2.imshow( 'rgb', rgb )

		if IS_FOUND :
			cv2.namedWindow( 'out' )
			cv2.imshow( 'out', out )

		if cv2.waitKey(1) & 0xFF == ord('q') :
			break

		if cv2.waitKey(99) & 0xFF == ord('c') :
			cv2.imwrite( 'out.png', out )
			cv2.imwrite( 'edges.png', edges )
			cv2.imwrite( 'gray.png', gray )
			cv2.imwrite( 'org.png', rgb )
			print ("Slike spremljene")

		time.sleep( DELAY )

	else :
		print ("Stopirano")
		break

if USE_CAM : video_capture.release()
cv2.destroyAllWindows()


im=Image.open("out.png")
text=pytesseract.image_to_string(im, config="-c tessedit_char_whitelist=QWERTZUIOPASDFGHJKLYXCVBNM --psm 6 --oem 0")
print(text)
#print(type(text))

positions=pytesseract.image_to_boxes(im, config="-c tessedit_char_whitelist=QWERTZUIOPASDFGHJKLYXCVBNM --psm 6 --oem 0")

for position in positions.splitlines():
    position = position.split(' ')
    #print(position)

text = text.replace(' ','')
length=text.index('\n')
#print(text)

search = list(map(str, input('Enter words: ').strip().split(',')))

print(search)

letters = [(letter, divmod(index, length))
            for  index, letter in enumerate (text)]
#Promijeni redoslijed popisa kako bi predstavljao svaki smjer čitanja
#i sve se dodaju u rijecnik
lines = {}

offsets = {'down':0, 'right down':-1, 'left down':1}

for direction, offset in offsets.items():

    lines[direction] = []

    for i in range(length):

        for j in range(i, len(letters), length + offset):

            lines[direction].append(letters[j])

        lines[direction].append('\n')


lines['left']  = letters

lines['right'] = [i for i in reversed(letters)]

lines['up'] = [i for i in reversed(lines['down'])]

lines['left up'] = [i for i in reversed(lines['right down'])]

lines['right up'] = [i for i in reversed(lines['left down'])]

#Stvaranje stringova od slova i pronalazi se rijec u njima 

for direction, tup in lines.items():

    string = ''.join([i[0] for i in tup])

    for word in search:

        if word in string:

            location = tup[string.index(word)][1]
			
            print (word, 'row', location[0]+1, 'column', location[1]+1, direction)

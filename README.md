# Synesthetic-Dream

This program explores alternative forms of data visualization. It loads the text from Lewis Carroll’s Alice In Wonderland from NLTK’s Gutenberg dataset, and represents the entire corpus in five stages. It simulates grapheme-color synesthesia – a neurological condition in which the perception of alphanumeric characters is associated with color. 

Viewing the rendered animation:
https://youtu.be/KjNj6jAP5lg

Running the code:
animation.py outputs images into the "frames" folder. Frames can be compiled into a video using "ffmpeg -r 60 -start_number 7030000 -s 4096x2160 -i %d.png -vcodec libx264 -crf 5 -pix_fmt yuv420p final.mp4". 
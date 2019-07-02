# Word Search Solver
Word Search solver which sees the word search on a paper with a web camera and solves it, made in Python.
Used Tesseract OCR with pytesseract wrapper and library OpenCV.

For now the word search works if the words you search are written down in a console.
TODO: words that need to be searched will be recognized together with the word search itself

It works only if the word search on paper does not have a inner grid, only an outer grid. (it will recognize the whole wordsearch but Tesseract wont recognize the characters that are in it)
TODO: recognize the characters that are in the word search if the word search has an inner grid

Reference and snippets of code used for this project:
- https://docs.opencv.org/
- https://github.com/robbiebarrat/word-search/blob/master/wordsearch.py
- https://mehmethanoglu.com.tr/blog/6-opencv-ile-dikdortgen-algilama-python.html

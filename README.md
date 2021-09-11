# TOW.PY

TOW.PY *(text only window)* is a simple, toy python library that allows for text-based graphical
applications to be prototyped and developed. It has been built on top of
*pygame* but developed as to abstract its methods away.

## Setup
TOW.PY can easily be installed with pip.
`pip install towpy`

## Code Example
```
import towpy

tow = towpy.TextOnlyWindow()

txt_obj = towpy.TextObject(["Hello", "World"], (10, 10))
tow.add_object(txt_obj)

tow.run()
```

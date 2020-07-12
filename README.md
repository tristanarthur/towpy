# TOW.PY

TOW.PY *(text only window)* is a simple, toy python library that allows for text-based graphical
applications to be prototyped and developed. It has been built on top of
*pygame* but developed as to abstract its methods away.

*SIDE NOTE*: This is not to say that pygame is complicated or necessary to
abstract away to create a useable framework.

## Philosophy
Why develop a program that is so restricted when libraries such as *pygame*
already exist? Aside from being a toy library to play around with and develop
quirky text programs in, I have always taken after the way of thinking that
minimilism enhances creativity.

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

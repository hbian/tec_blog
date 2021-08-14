a Unicode string is a sequence of code points, which are numbers from 0 to 0x10ffff. This sequence needs to be represented as a set of bytes (meaning, values from 0–255) in memory. The rules for translating a Unicode string into a sequence of bytes are called an encoding.
The first encoding you might think of is an array of 32-bit integers. In this representation, the string “Python” would look like this:

```
   P           y           t           h           o           n
0x50 00 00 00 79 00 00 00 74 00 00 00 68 00 00 00 6f 00 00 00 6e 00 00 00
   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
```

Encodings don’t have to handle every possible Unicode character, and most encodings don’t. For example, Python’s default encoding is the ‘ascii’ encoding. The rules for converting a Unicode string into the ASCII encoding are simple; for each code point:
* If the code point is < 128, each byte is the same as the value of the code point.
* If the code point is 128 or greater, the Unicode string can’t be represented in this encoding. (Python raises a UnicodeEncodeError exception in this case.)

UTF-8 is one of the most commonly used encodings. UTF stands for “Unicode Transformation Format”, and the ‘8’ means that 8-bit numbers are used in the encoding. (There’s also a UTF-16 encoding, but it’s less frequently used than UTF-8.) UTF-8 uses the following rules:
* If the code point is <128, it’s represented by the corresponding byte value.
* If the code point is between 128 and 0x7ff, it’s turned into two byte values between 128 and 255.

Code points >0x7ff are turned into three- or four-byte sequences, where each byte of the sequence is between 128 and 255.


### Python unicode 
Unicode strings are expressed as instances of the unicode type, one of Python’s repertoire of built-in types. Python represents Unicode strings as either 16- or 32-bit integers, depending on how the Python interpreter was compiled.
The unicode() constructor has the signature unicode(string, [encoding, errors]). All of its arguments should be 8-bit strings.All of its arguments should be 8-bit strings. The first argument is converted to Unicode using the specified encoding; if you leave off the encoding argument, the ASCII encoding is used for the conversion, so characters greater than 127 will be treated as errors

Another important method is .encode([encoding], [errors='strict']), which returns an 8-bit string version of the Unicode string, encoded in the requested encoding. 
```
>>> u = unichr(40960) + u'abcd' + unichr(1972)
>>> u.encode('utf-8')
'\xea\x80\x80abcd\xde\xb4'
>>> u.encode('ascii')                       
Traceback (most recent call last
```
Python’s 8-bit strings have a .decode([encoding], [errors]) method that interprets the string using the given encoding:
```
>>> u = unichr(40960) + u'abcd' + unichr(1972)   # Assemble a string
>>> utf8_version = u.encode('utf-8')             # Encode as UTF-8
>>> type(utf8_version), utf8_version
(<type 'str'>, '\xea\x80\x80abcd\xde\xb4')
```

Python supports writing Unicode literals in any encoding, but you have to declare the encoding being used. This is done by including a special comment as either the first or second line of the source file:
```
#!/usr/bin/env python
# -*- coding: latin-1 -*-

u = u'abcdé'
print ord(u[-1])
```
If you don’t include such a comment, the default encoding used will be ASCII.

**The most important tip is: Software should only work with Unicode strings internally, converting to a particular encoding on output.**



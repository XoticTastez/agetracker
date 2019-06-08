# AgeTracker
AgeTracker is a console application that allows you to keep track of ages, in the following format: `1y 2m 3w 4d`

For example, on June 7th, 2019, my rat Chief, born on April 16th, 2019, was displayed by AgeTracker as being `1m 3w 1d` old.
If any of the timespan specifications equal zero, they will not be shown.

To add a new entry, enter `+` followed by the name.
To remove an existing entry, enter `-` followed by the name.
Names are case-sensitive, and year of birth's millennium/century should not be omitted (`19` equates to the year 19, not 2019).

### Credits
Icon by Smashicons at [Flaticon](https://www.flaticon.com/free-icon/hourglass_148855)

Compiled with [PyInstaller](https://github.com/pyinstaller/pyinstaller)

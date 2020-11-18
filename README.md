## tmpmail

Create and view temporary mailbox using 1secmail [API](https://www.1secmail.com/api/).


## Requirements
* _python >= 3.6_
* _requests_
* _html2text_
* _rich_
* _appdirs_

## Installation
3. Install using `pip install git+https://github.com/meashishsaini/tmpmail-python`

## Usage
```
tmpmail [-h] [-g [USERNAME]] [-r] [-t] [-b [BROWSER]] [id]

positional arguments:
  id                    id of the email received

optional arguments:
  -h, --help            show this help message and exit
  -g [USERNAME], --generate [USERNAME]
                        generate new username or use given.
  -r, --recent          view most recent email.
  -t, --text            view email as pure text.
  -b [BROWSER], --browser [BROWSER]
                        open email in given browser.
```

## Credits
The python version inspired by Siddharth Dushantha's [tmpmail](https://github.com/sdushantha/tmpmail) script.
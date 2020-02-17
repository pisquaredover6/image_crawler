Given a plaintext file containing URLs, one per line, e.g.:

http://mywebserver.com/images/271947.jpg  
http://mywebserver.com/images/24174.jpg  
http://somewebsrv.com/img/992147.jpg

The script takes this plaintext file as an argument and downloads all images, storing them on the local hard disk

To store all images in a local folder "output", call the script like: ` python image_crawler path/to/urllist.txt`
To save images in other directory, call script like: ` python image_crawler path/to/urllist.txt path/to/outpt_directory` 
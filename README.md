# gmail_create_label

This is a simple application to create labels in gmail.

As I am currently looking for a new job, I have to send a lot of e-mails to different requirement services. My post box very quickly became a mess, and I decided to organise it in a better way using Gmail labels. I also found it inconvenient for me to set the labels within the browser version of Gmail. This application aims to make label creation a more simple way.It is build on Gmail API library.

## Example of usage
To create a new label with name "label_title/label_subtitle". The parameter `-st` is optional: if not defined, the resulting label name is "label_title". The parameter `-status` will defind the color of the label as follows: "fail": red, "pending":grey, "succes": green.
``` bash
python main.py -t label_titile -st label_subtitle -status fail
```
If the label already exsists, the code will try to update it.

To delete a label, define its name and raise a flag `-d`
``` bash
python main.py -t label_titile -st label_subtitle -d
```

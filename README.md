#Sajax

Sajax is a Flask/jQuery extension for building ajax web applications.

There are a ton of tools/libraries/frameworks out there that make AJAX really easy though, right? Turns out,
there aren't really any that ease the transition between python and javascript specifically. Even jQuery's
added functionality isn't really all that helpful, even when you narrow your focus down to just the javascript
side of things.

A lot of how this was built was inspired from personal experience with an old PHP ajax framework, XAjax.

##Dependencies
* <a href="http://jquery.com/">jQuery</a>
    * v1.11.1 or greater, this is a jQuery/Python library and as such isn't compatible with straight javascript.
    Further, in my original experience with the XAjax library from PHP, I found that the javascript side of things was
    much messier and had several defects entrenched in it. I don't expect this to ever be large enough to suffer any
    significant drawbacks by taking the "easy" route of jQuery.
* <a href="https://github.com/danheberden/jquery-serializeForm">jQuery-serializeForm</a>
    * So its not really a dependency, as sajax.getFormValues will fall back to jQuery's serialize method. 
    jQuery-serializeForm will, however, construct an object representing the serialization of a form, compared to
    jQuery's serialize() producing a url-encoded string.

##Installation

##Usage

###Python:

###Javascript:

##Examples

function sajax() {
    this.loads_pending = 0;
}

/**
 * Process sajax response (data)
 *
 * sajax.call binds this as the success processing method. data is a json array of
 * commands (denoted sometimes by an abbreviation) to take action on and any corresponding
 * data (such as JS that needs evaluating, or some HTML to be assigned).
 *
 * @param data
 */
sajax.prototype.parseResponse = function(data) {
    // Limit to 20 iterations (10 seconds)
    var i = data.i === undefined ? 0 : data.i;
    // Store delayed data to be called via timeout
    var delayed_data = []

    if (i > 20)
        throw 'Exceeded parseResponse processing limit';

    $.each(data.r, function() {
        // If we have a load queued and we haven't already waited 10 seconds, continue to wait
        if (delayed_data.length > 0 || (sajax.loads_pending > 0 && this.action != 'load')) {
            delayed_data.push(this);
        } else {
            // Process the action for this iteration of data.r
            switch(this.action) {
                case 'as':
                    $(this.selector).html(this.data);
                    break;
                case 'ap':
                    $(this.selector).append(this.data);
                    break;
                case 'ap_t':
                    // append to selector only if the id of the template is not on the page
                    if ($(this.id).length == 0)
                        $(this.selector).append(this.data);
                    break;
                case 'js':
                    eval(this.data);
                    break;
                case 'alert':
                    alert(this.data);
                    break;
                case 'load':
                    sajax.load(this.data);
                    break;
                default:
                    break;
            }
        }
    });

    // If there was one or more delayed_data, set a timeout to re-process
    if (delayed_data.length > 0)
        setTimeout(function() { sajax.parseResponse({'r': delayed_data, 'i':++i}) }, 500);
};

/**
 * load a static file onto the DOM via ajax
 *
 * @param file
 */
sajax.prototype.load = function(file) {
    if (file == undefined)
        return false;

    this.loads_pending++;

    try {
        switch(file.split('.').pop()) {
            case 'css':
                link = $('<link rel="stylesheet" type="text/css" href="'+file+'">');
                $('head').append(link);
                // css files effectively load automatically
                this.loads_pending--;
                break;
            case 'js':
                $.getScript(file, function() { sajax.loads_pending--; });
                break;
        }
    } catch(e) {
        this.loads_pending--;
        throw e;
    }
}

/**
 * Shortcut to initialize a jquery AJAX request via post
 *
 * @param path
 * @param parameters
 * @returns {boolean}
 */
sajax.prototype.call = function(path, parameters) {
    if (parameters === undefined) parameters = {};
    if (path.slice(0, 1) !== '/') path = '/' + path;

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: path,
        data: JSON.stringify(parameters),
        datatype: 'json',
        success: this.parseResponse
    });

    return false;
};

/**
 * Build array from arguments, retrun
 *
 * @returns {array}
 */
sajax.prototype.buildData = function() {
    // extend string holds the js that will be eval'd into the returned object
    var e_s = '';
    var data = {};

    for (var i = 0; i < arguments.length; i++) {
        if (typeof(arguments[i]) == 'object')
            e_s += 'arguments['+i+'],';
        else if (typeof(arguments[i]) == 'string')
            e_s += "$('"+arguments[i].replace("'", "\\'")+"').serializeForm(),";
    }

    if (e_s.length > 1)
        eval('$.extend(true, data, '+e_s.substring(0, e_s.length-1)+');');

    return data;
}

/**
 * Return serialized data for easy form consumption
 *
 * @param selector
 * @returns {json}
 */
sajax.prototype.getFormValues = function(selector) {
    if ($(selector).serializeForm)
        return $(selector).serializeForm();
    else
        return $(selector).serialize();
}
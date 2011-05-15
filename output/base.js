$(function () {
    // TO CREATE AN INSTANCE
    // select the tree container using jQuery
    $("#demo1")
        // call `.jstree` with the options object
        .jstree({
            // the `plugins` array allows you to configure the active plugins on this instance
            "plugins" : ["html_data","ui","crrm"],
            // each plugin you have included can have its own config object
            "core" : { "initially_open" : [ "phtml" ] }
            // it makes sense to configure a plugin only if overriding the defaults
        })
        // EVENTS
        // each instance triggers its own events - to process those listen on the container
        // all events are in the `.jstree` namespace
        // so listen for `function_name`.`jstree` - you can function names from the docs
        .bind("loaded.jstree", function (event, data) {
            // you get two params - event & data - check the core docs for a detailed description
        });

});

window.onload = function() {
  document.onselectstart = function() {return false;} // ie
  document.onmousedown = function() {return false;} // mozilla
}
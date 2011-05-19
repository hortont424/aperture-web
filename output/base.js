$(function () {
    // TO CREATE AN INSTANCE
    // select the tree container using jQuery
    $("#demo1")
        // call `.jstree` with the options object
        .jstree({
            // the `plugins` array allows you to configure the active plugins on this instance
            "plugins" : ["html_data","ui"],
            // each plugin you have included can have its own config object
            "core" : { "initially_open" : [ ] }
            // it makes sense to configure a plugin only if overriding the defaults
        })
        // EVENTS
        // each instance triggers its own events - to process those listen on the container
        // all events are in the `.jstree` namespace
        // so listen for `function_name`.`jstree` - you can function names from the docs
        .bind("loaded.jstree", function (event, data) {
            // you get two params - event & data - check the core docs for a detailed description
        })
        .bind("select_node.jstree", function (event, data) { 
            // `data.rslt.obj` is the jquery extended node that was clicked
            $("#title").text(data.rslt.obj.attr("id"));
            
            $("#sidebar").children().remove();
            
            $.getJSON(data.rslt.obj.attr("id") + ".js")
            .success(function(data) {
                for(var i in data)
                {
                    style = "vertical-align: middle; max-height: 100px; overflow:hidden; float: left;";
                    $("#sidebar").append("<a href='" + data[i][1] + "'><img style='"+style+"' src='" + data[i][1] + "'/></a>");
                }
            })
            .error(function() { alert("error"); });
        });
});

window.onload = function() {
  document.onselectstart = function() {return false;} // ie
  document.onmousedown = function() {return false;} // mozilla
}
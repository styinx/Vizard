function allowDrop(event)
{
    event.preventDefault();
}

function drag(event, callback)
{
    event.dataTransfer.setData("id", event.target.id);
    callback(event);
}

function drop(event, callback)
{
    event.preventDefault();
    let dropped_element = event.target;
    let id = event.dataTransfer.getData("id");

    callback();
}
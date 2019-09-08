var { Query, User } = AV;
AV.init({
    appId: "GQYoAfWH0A2DanzVcWc62zKt-MdYXbMMI",
    appKey: "Mp24E60jxscWbErP5wYBCjgA",
});
$(function(){
    var query = new AV.Query('setting');
    query.select(['title','description','instagram','address']);
    query.first().then(function (todo) {
    var title = todo.get('title'); 
    var description = todo.get('description'); 
    var instagram = todo.get('instagram'); 
    var address = todo.get('address'); 
    $("title").text(title);
    $("#logo").text(title);
    $("#address").text(address);
    $("meta[name='description']").attr('content',description);
    $(".instagram_url").attr("href","https://www.instagram.com/blackholexgirl/");
    });
})
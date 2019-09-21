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
    //$("title").text(title);
    $("#logo").text(title);
    $("#address").text(address);
    //$("meta[name='description']").attr('content',description);
    $(".instagram_url").attr("href","https://www.instagram.com/blackholexgirl/");
    });
})

//utc时间
function toUtc(date){
    var y =  date.getUTCFullYear();   
    var m = date.getUTCMonth() ;
    var d = date.getUTCDate();
    var h= date.getUTCHours();
    var M = date.getUTCMinutes();
    var s = date.getUTCSeconds();
    var utc = new Date(y,m,d,h,M,s);
    return utc;
}

//utc日期
function toUtcDate(date){
    var y =  date.getUTCFullYear();   
    var m = date.getUTCMonth() ;
    var d = date.getUTCDate();
    var h= date.getUTCHours();
    var M = date.getUTCMinutes();
    var s = date.getUTCSeconds();
    var utcDate = new Date(y,m,d);
    return utcDate;
}
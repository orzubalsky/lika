var galleries = function()
{   
    var galleries = $('.gallery');
    
    for (var i=0; i<galleries.size(); i++)
    {
        var gallery = $(galleries).eq(i);
        
        $('.item', gallery).eq(0).show();
    }
    
    $('.next').click(function(e)
    {
        e.preventDefault();
        
        var gallery = $(this).parent().parent();
        var count = $('.item', gallery).size();
        
        var index = $('.item:visible', gallery).index();
        index = (index < count-1) ? index+1 : 0;
        $('.item', gallery).hide();
        $('.item', gallery).eq(index).show();
    });
    $('.back').click(function(e)
    {
        e.preventDefault();
        
        var gallery = $(this).parent().parent();
        var count = $('.item', gallery).size();
        
        var index = $('.item:visible', gallery).index();
        index = (index > 0) ? index-1 : count-1;
        $('.item', gallery).hide();
        $('.item', gallery).eq(index).show();
    });        
};

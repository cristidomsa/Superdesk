define('providers/twitter/adaptor', [
    'providers',
    'utils/str',
    'jquery',
    'gizmo',
    'jquery/rest',
    'jquery/utils',
    'providers/twitter/tab',
    'tmpl!livedesk>providers/twitter/post'
], function(providers,str, $, Gizmo)
{
    var AnnotateView = Gizmo.View.extend
    ({
        tagName: 'li',
        init: function(data)
        {
            var self = this;
            $(self.el).on('click', '.btn.publish', function()
            {
                self.data.Content = $('.twitter-full-content .result-text', self.el).html();
                self.data.Meta.annotation = [$('.twitter-full-content .annotation:eq(0)', self.el).html(), 
                    $('.twitter-full-content .annotation:eq(1)', self.el).html()];
                self.data.Meta = JSON.stringify(self.data.Meta);
                self.parent.insert(self.data);
                //$('.actions', self.el).remove();
            });
            $(self.el).on('click', '.btn.cancel', function()
            {
                self.parent = null;
                self.el.remove();
            });
        },
        render: function()
        {
            this.el.tmpl('livedesk>providers/twitter/post', this.data);
            this.el.addClass('with-avatar twitter clearfix');
        }
    });
    
    $.extend(providers.twitter, 
    {
        adaptor: 
        {
            author: 1,
            init: function() 
            {
                var self = this;
                new $.rest('Superdesk/Collaborator/')
                    .xfilter('Id')
                    .request({data: { name: 'twitter'}})
                    .done(function(collabs)
                    {
                        if( $.isDefined(collabs[0]) ) 
                            self.author = collabs[0].Id;
                    });
            },
            universal: function(obj) 
            {
                var meta =  jQuery.extend(true, {}, obj);
                delete meta.text
                
                return new AnnotateView
                ({
                    data: 
                    {
                        Content: obj.text,
                        Type: 'normal',
                        Author: this.author,
                        Meta: meta
                    }
                });
            }
        }
    });
	return providers;
});



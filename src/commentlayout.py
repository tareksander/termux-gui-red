from __future__ import annotations


import praw.models
import termuxgui.oo as tgo
import termuxgui as tg


class CommentLayout(tgo.NestedScrollView):
    
    def on_back(self):
        self.a.active_layout(self.a.post)
    
    def set_parent(self, parent):
        self.reddit_parent = parent
        if isinstance(self.reddit_parent, praw.models.Submission):
            self.title.settext(parent.title)
            self.title.setvisibility(tgo.View.VISIBLE)
            self.content.settext(self.reddit_parent.selftext)
        else:
            self.title.setvisibility(tgo.View.GONE)
            self.content.settext(parent.body)
    
    def on_post(self, e: tg.Event, v: tgo.textview):
        if self.reply.gettext() != "":
            self.reddit_parent.reply(self.reply.gettext())
            self.reply.settext("")
            self.a.active_layout(self.a.post)
    
    def __init__(self, activity: Activity):
        tgo.NestedScrollView.__init__(self, activity, activity.frame, visibility=tgo.View.GONE)
        self.a = activity
        
        self.reddit_parent: praw.models.Submission | praw.models.Comment | None = None
        
        self.layout = tgo.LinearLayout(self.a, self)
        
        self.title = tgo.TextView(self.a, "", self.layout)
        self.title.setheight(tgo.View.WRAP_CONTENT)
        self.title.setlinearlayoutparams(0)
        self.title.settextsize(20)

        self.content = tgo.TextView(self.a, "", self.layout)
        self.content.setheight(tgo.View.WRAP_CONTENT)
        self.content.setlinearlayoutparams(0)
        self.content.setmargin(20, "bottom")

        self.reply = tgo.EditText(self.a, "", self.layout)
        self.reply.setheight(tgo.View.WRAP_CONTENT)
        self.reply.setlinearlayoutparams(0)
        
        self.post = tgo.Button(self.a, "Post", self.layout)
        self.post.setheight(tgo.View.WRAP_CONTENT)
        self.post.setlinearlayoutparams(0)
        self.post.on_click = self.on_post
        
        pass


from activity import Activity

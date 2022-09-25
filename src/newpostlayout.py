from __future__ import annotations

import praw.models
import termuxgui.oo as tgo
import termuxgui as tg


class NewPostLayout(tgo.NestedScrollView):
    
    def on_back(self):
        self.a.active_layout(self.a.sub)
    
    def set_sub(self, sub: praw.models.Subreddit):
        self.sub = sub
        self.sublabel.settext("r/"+sub.display_name)
    
    def on_post(self, e: tg.Event, v: tgo.textview):
        if self.title.gettext() != "":
            self.sub.submit(self.title.gettext(), selftext=self.content.gettext())
            self.title.settext("")
            self.content.settext("")
            self.a.active_layout(self.a.sub)
            self.a.sub.update_sorting()
    
    def __init__(self, activity: Activity):
        tgo.NestedScrollView.__init__(self, activity, activity.frame, visibility=tgo.View.GONE)
        self.a = activity
        
        self.sub: praw.models.Subreddit | None = None
        
        self.layout = tgo.LinearLayout(self.a, self)
        
        self.sublabel = tgo.TextView(self.a, "", self.layout)
        self.sublabel.setheight(tgo.View.WRAP_CONTENT)
        self.sublabel.setlinearlayoutparams(0)
        self.sublabel.setmargin(20, "bottom")
        self.sublabel.settextsize(18)
        
        self.title = tgo.EditText(self.a, "", self.layout, singleline=True)
        self.title.setheight(tgo.View.WRAP_CONTENT)
        self.title.setlinearlayoutparams(0)
        self.title.settextsize(20)
        
        self.content = tgo.EditText(self.a, "", self.layout, singleline=False, inputtype="textMultiLine")
        self.content.setheight(tgo.View.WRAP_CONTENT)
        self.content.setlinearlayoutparams(0)

        self.post = tgo.Button(self.a, "Post", self.layout)
        self.post.setheight(tgo.View.WRAP_CONTENT)
        self.post.setlinearlayoutparams(0)
        self.post.on_click = self.on_post


from activity import Activity

from __future__ import annotations

import sys

import praw.models
import termuxgui.oo as tgo
import termuxgui as tg
from functools import partial

import app


class SearchLayout(tgo.LinearLayout):

    def on_back(self):
        sys.exit(0)
    
    def on_subreddit(self, e: tg.Event, v: tgo.Button, sub: praw.models.Subreddit):
        self.a.hidesoftkeyboard()
        self.a.sub.set_sub(sub)
        self.a.active_layout(self.a.sub)
    
    def on_search(self, e: tg.Event, v: tgo.View):
        self.results.clearchildren()
        for sub in app.reddit.subreddits.search_by_name(self.edit.gettext()):
            b = tgo.Button(self.a, sub.display_name, self.results)
            b.on_click = partial(self.on_subreddit, sub=sub)
    
    def __init__(self, activity: Activity):
        tgo.LinearLayout.__init__(self, activity, activity.frame, visibility=tgo.View.GONE)
        self.a = activity
        self.content = tgo.TextView(self.a, "Search subreddits", self)
        self.edit = tgo.EditText(self.a, "", self)
        self.search = tgo.Button(self.a, "Search", self)
        self.search.on_click = self.on_search
        
        self.search.setmargin(10, "bottom")
        
        self.results_scroll = tgo.NestedScrollView(self.a, self)
        self.results = tgo.LinearLayout(self.a, self.results_scroll)
        
        self.content.setheight(tgo.View.WRAP_CONTENT)
        self.edit.setheight(tgo.View.WRAP_CONTENT)
        self.search.setheight(tgo.View.WRAP_CONTENT)
        
        self.content.setlinearlayoutparams(0)
        self.edit.setlinearlayoutparams(0)
        self.search.setlinearlayoutparams(0)


from activity import Activity

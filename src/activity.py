from __future__ import annotations

from typing import Optional

import termuxgui.oo as tgo
import termuxgui as tg
import app
import res
import base64


class Activity(tgo.Activity):
    
    def intercept_back(self) -> bool:
        return True
    
    def on_back(self):
        if hasattr(self.active, "on_back"):
            self.active.on_back()
    
    def active_layout(self, l: tgo.ViewGroup):
        self.active.setvisibility(tgo.View.GONE)
        self.active = l
        self.active.setvisibility(tgo.View.VISIBLE)
        if self.active == self.search:
            self.search.edit.focus(True)
    
    def __init__(self, c: tg.Connection, t: Optional[tg.Task]):
        tgo.Activity.__init__(self, c, t)
        self.frame = tgo.FrameLayout(self)
        
        self.auth = AuthLayout(self)
        self.search = SearchLayout(self)
        self.sub = SubredditLayout(self)
        self.post = PostLayout(self)
        self.newpost = NewPostLayout(self)
        self.comment = CommentLayout(self)
        
        self.active = self.search
        
        if not app.reddit.read_only:
            self.active_layout(self.search)
        else:
            self.active_layout(self.auth)
        
        self.settaskdescription("", str(base64.standard_b64encode(res.get_icon()), "ascii"))


from authlayout import AuthLayout
from searchlayout import SearchLayout
from subredditlayout import SubredditLayout
from postlayout import PostLayout
from newpostlayout import NewPostLayout
from commentlayout import CommentLayout

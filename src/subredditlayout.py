from __future__ import annotations

from math import ceil
from typing import List
from functools import partial

import praw.models
import termuxgui.oo as tgo
import termuxgui as tg
from imagethread import image_thread, ImageTask


page_size = 10


def on_upvote(e: tg.Event, v: tgo.textview, submission, downvote):
    if submission.likes:
        submission.clear_vote()
        submission.likes = None
        v.settextcolor(0xffffffff)
    else:
        submission.upvote()
        submission.likes = True
        v.settextcolor(0xffff0000)
        downvote.settextcolor(0xffffffff)
    pass


def on_downvote(e: tg.Event, v: tgo.textview, submission, upvote):
    if submission.likes is not None and not submission.likes:
        submission.clear_vote()
        submission.likes = None
        v.settextcolor(0xffffffff)
    else:
        submission.downvote()
        submission.likes = False
        v.settextcolor(0xffff0000)
        upvote.settextcolor(0xffffffff)
    pass


class SubredditLayout(tgo.LinearLayout):

    def loaded_image(self, data: bytes, task: ImageTask, v: tgo.ImageView):
        v.setimage(data)
        self.image_tasks.remove(task)
    
    def on_back(self):
        self.a.active_layout(self.a.search)
        for t in self.image_tasks:
            t.aborted()
    
    def set_sub(self, sub: praw.models.Subreddit):
        self.content.clearchildren()
        self.sub = sub
        self.sub_name.settext("r/"+sub.display_name)
        if self.sortby_value == "hot":
            self.update_sorting()
        else:
            self.sortby_value = "hot"
            self.sortby.selectitem(0)

    def on_post(self, e: tg.Event, v: tgo.textview, submission, upvote, downvote):
        self.a.post.set_submission(submission, upvote, downvote)
        self.a.active_layout(self.a.post)
    
    def set_page(self, page: int):
        if self.page == 0 and page != 0:
            self.prev.setvisibility(tgo.View.VISIBLE)
        if page == 0 and self.page != 0:
            self.prev.setvisibility(tgo.View.GONE)
        if self.page == self.lastpage and page != self.lastpage:
            self.next.setvisibility(tgo.View.VISIBLE)
        if page == self.lastpage and self.page != self.lastpage:
            self.next.setvisibility(tgo.View.GONE)
        self.page = page
        for t in self.image_tasks:
            t.aborted()
        self.content.clearchildren()
        for submission in self.post_list[page_size*self.page:page_size*(self.page+1)]:
            #pprint(vars(submission))
            post = tgo.LinearLayout(self.a, self.content)
            post.setmargin(5, "top")
            post.setmargin(5, "bottom")
            post.setheight(tgo.View.WRAP_CONTENT)
            post.setlinearlayoutparams(0)
            user = tgo.TextView(self.a, "u/" + (submission.author.name if submission.author is not None else "deleted"), post)
            title = tgo.TextView(self.a, submission.title, post)
            title.settextsize(20)
            if submission.selftext == "" and hasattr(submission, "url") and submission.url is not None and submission.url.endswith((".jpg", ".bmp", ".webp", ".png")):
                v = tgo.ImageView(self.a, post)
                t = ImageTask(submission.url, partial(self.loaded_image, v=v))
                self.image_tasks.append(t)
                image_thread.tasks.put(t)
            
            bar = tgo.LinearLayout(self.a, post, vertical=False)
            upvote = tgo.TextView(self.a, "↑", bar)
            upvote.settextsize(20)
            upvote.setwidth(tgo.View.WRAP_CONTENT)
            upvote.setlinearlayoutparams(0)
            upvote.setmargin(10, "right")
            upvote.sendclickevent(True)
            score = tgo.TextView(self.a, str(submission.score), bar)
            score.setmargin(10, "right")
            score.setwidth(tgo.View.WRAP_CONTENT)
            score.setlinearlayoutparams(0)
            downvote = tgo.TextView(self.a, "↓", bar)
            downvote.settextsize(20)
            downvote.setwidth(tgo.View.WRAP_CONTENT)
            downvote.setlinearlayoutparams(0)
            downvote.setmargin(10, "right")
            downvote.sendclickevent(True)
            if submission.likes is not None:
                if submission.likes:
                    upvote.settextcolor(0xffff0000)
                if not submission.likes:
                    downvote.settextcolor(0xffff0000)
            comments = tgo.TextView(self.a, "💬 "+str(submission.num_comments), bar)
            comments.setwidth(tgo.View.WRAP_CONTENT)
            comments.setlinearlayoutparams(0)
            
            upvote.on_click = partial(on_upvote, submission=submission, downvote=downvote)
            downvote.on_click = partial(on_downvote, submission=submission, upvote=upvote)
            
            title.sendclickevent(True)
            title.on_click = partial(self.on_post, submission=submission, upvote=upvote, downvote=downvote)
    
    def on_sub_long(self, e: tg.Event, v: tgo.View):
        self.a.newpost.set_sub(self.sub)
        self.a.active_layout(self.a.newpost)
    
    def update_sorting(self):
        self.content.clearchildren()
        if self.sortby_value == "hot":
            self.post_list = list(self.sub.hot())
        if self.sortby_value == "new":
            self.post_list = list(self.sub.new())
        if self.sortby_value == "top":
            self.post_list = list(self.sub.top())
        self.lastpage = ceil(len(self.post_list) / page_size)-1
        self.set_page(0)
        
    def on_sort(self, e: tg.Event, v: tgo.Button):
        self.sortby_value = e.value["selected"]
        self.update_sorting()

    def on_prev(self, e: tg.Event, v: tgo.Button):
        if self.page > 0:
            self.set_page(self.page - 1)

    def on_next(self, e: tg.Event, v: tgo.Button):
        if self.page < self.lastpage:
            self.set_page(self.page + 1)
    
    def __init__(self, activity: Activity):
        tgo.LinearLayout.__init__(self, activity, activity.frame, visibility=tgo.View.GONE)
        self.a = activity
        
        self.sub: praw.models.Subreddit | None = None
        self.post_list: List[praw.models.Submission] | None = None
        self.page = 0
        self.lastpage = 0
        
        self.image_tasks: List[ImageTask] = []
        
        self.bar = tgo.LinearLayout(self.a, self, vertical=False)
        self.bar.setheight(tgo.View.WRAP_CONTENT)
        self.bar.setlinearlayoutparams(0)
        
        self.sub_name = tgo.TextView(self.a, "", self.bar)
        self.sub_name.settextsize(20)
        self.sub_name.sendlongclickevent(True)
        self.sub_name.on_longClick = self.on_sub_long
        
        self.sortby_value = "hot"
        self.sortby = tgo.Spinner(self.a, self.bar)
        self.sortby.setlist(["hot", "new", "top"])
        self.sortby.on_itemselected = self.on_sort
        
        self.prev = tgo.Button(self.a, "Previous", self, visibility=tgo.View.GONE)
        self.prev.setheight(tgo.View.WRAP_CONTENT)
        self.prev.setlinearlayoutparams(0)
        
        self.content_scroll = tgo.NestedScrollView(self.a, self)
        self.content = tgo.LinearLayout(self.a, self.content_scroll)
        
        self.next = tgo.Button(self.a, "Next", self)
        self.next.setheight(tgo.View.WRAP_CONTENT)
        self.next.setlinearlayoutparams(0)
        
        self.prev.on_click = self.on_prev
        self.next.on_click = self.on_next


from activity import Activity

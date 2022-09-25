from __future__ import annotations

import praw.models
from praw.models.comment_forest import CommentForest
import termuxgui.oo as tgo
import termuxgui as tg
from functools import partial

import subredditlayout

import app
from imagethread import ImageTask, image_thread


def on_upvote(e: tg.Event, v: tgo.textview, submission, downvote, upvote_sub, downvote_sub):
    if submission.likes:
        submission.clear_vote()
        submission.likes = None
        v.settextcolor(0xffffffff)
        upvote_sub.settextcolor(0xffffffff)
    else:
        submission.upvote()
        submission.likes = True
        v.settextcolor(0xffff0000)
        upvote_sub.settextcolor(0xffff0000)
        downvote.settextcolor(0xffffffff)
        downvote_sub.settextcolor(0xffffffff)
    pass


def on_downvote(e: tg.Event, v: tgo.textview, submission, upvote, upvote_sub, downvote_sub):
    if submission.likes is not None and not submission.likes:
        submission.clear_vote()
        submission.likes = None
        v.settextcolor(0xffffffff)
        downvote_sub.settextcolor(0xffffffff)
    else:
        submission.downvote()
        submission.likes = False
        v.settextcolor(0xffff0000)
        downvote_sub.settextcolor(0xffff0000)
        upvote.settextcolor(0xffffffff)
        upvote_sub.settextcolor(0xffffffff)
    pass


class PostLayout(tgo.SwipeRefreshLayout):

    def loaded_image(self, data: bytes, task: ImageTask):
        self.img.setimage(data)
        self.imagetask = None
    
    def on_back(self):
        self.a.active_layout(self.a.sub)
        if self.imagetask is not None:
            self.imagetask.abort()
    
    def parse_comments(self, comments: CommentForest, indentation: int):
        comment_list = list(comments)
        for c in comment_list:
            if isinstance(c, praw.models.MoreComments):
                pass
            else:
                layout = tgo.LinearLayout(self.a, self.comment_layout)
                layout.setheight(tgo.View.WRAP_CONTENT)
                layout.setlinearlayoutparams(0)
                layout.setmargin(indentation, "left")
                layout.setmargin(10, "top")

                user = tgo.TextView(self.a, "u/" + (c.author.name if c.author is not None else "deleted"), layout)
                
                content = tgo.TextView(self.a, c.body, layout)
                content.sendlongclickevent(True)
                content.on_longClick = partial(self.on_comment, comment=c)
                
                bar = tgo.LinearLayout(self.a, layout, vertical=False)
                upvote = tgo.TextView(self.a, "↑", bar)
                upvote.settextsize(20)
                upvote.setwidth(tgo.View.WRAP_CONTENT)
                upvote.setlinearlayoutparams(0)
                upvote.setmargin(10, "right")
                upvote.sendclickevent(True)
                score = tgo.TextView(self.a, str(c.score), bar)
                score.setmargin(10, "right")
                score.setwidth(tgo.View.WRAP_CONTENT)
                score.setlinearlayoutparams(0)
                downvote = tgo.TextView(self.a, "↓", bar)
                downvote.settextsize(20)
                downvote.setwidth(tgo.View.WRAP_CONTENT)
                downvote.setlinearlayoutparams(0)
                downvote.setmargin(10, "right")
                downvote.sendclickevent(True)
                if c.likes is not None:
                    if c.likes:
                        upvote.settextcolor(0xffff0000)
                    if not c.likes:
                        downvote.settextcolor(0xffff0000)
                
                upvote.on_click = partial(subredditlayout.on_upvote, submission=c, downvote=downvote)
                downvote.on_click = partial(subredditlayout.on_downvote, submission=c, upvote=upvote)
                
                self.parse_comments(c.replies, indentation + 20)
    
    def on_title(self, e: tg.Event, v: tgo.textview):
        self.a.comment.set_parent(self.submission)
        self.a.active_layout(self.a.comment)
    
    def on_comment(self, e: tg.Event, v: tgo.textview, comment):
        self.a.comment.set_parent(comment)
        self.a.active_layout(self.a.comment)
    
    def set_submission(self, submission, upvote: tgo.TextView, downvote: tgo.Textview):
        self.submission = submission
        self.upvote.on_click = partial(on_upvote, submission=self.submission, downvote=downvote, upvote_sub=upvote, downvote_sub=downvote)
        self.downvote.on_click = partial(on_downvote, submission=self.submission, upvote=upvote, upvote_sub=upvote, downvote_sub=downvote)
        
        self.user.settext(submission.author.name if submission.author is not None else "u/deleted")
        
        self.title.settext(submission.title)
        if submission.selftext != "":
            self.content.settext(submission.selftext)
            self.content.setvisibility(tgo.View.VISIBLE)
        else:
            self.content.setvisibility(tgo.View.GONE)
        
        self.score.settext(str(submission.score))
        
        if hasattr(submission, "url") and submission.url is not None and submission.url.endswith((".jpg", ".bmp", ".webp", ".png")):
            self.imagetask = ImageTask(submission.url, self.loaded_image)
            image_thread.tasks.put(self.imagetask)
            self.img.setvisibility(tgo.View.VISIBLE)
        else:
            self.img.setvisibility(tgo.View.GONE)
        self.comments.settext("💬 "+str(submission.num_comments))
        
        self.comment_layout.clearchildren()
        self.parse_comments(submission.comments, 0)
    
    def on_refresh(self, e: tg.Event, v: tgo.SwipeRefreshLayout):
        self.setrefreshing(False)
        self.set_submission(app.reddit.submission(self.submission.id), self.upvote, self.downvote)
    
    def __init__(self, activity: Activity):
        tgo.SwipeRefreshLayout.__init__(self, activity, activity.frame, visibility=tgo.View.GONE)
        self.scroll = tgo.NestedScrollView(self.a, self)
        self.a = activity
        
        self.layout = tgo.LinearLayout(self.a, self.scroll)
        
        self.submission = None
        self.imagetask = None
        self.comment_list: praw.models.Comment | praw.models.MoreComments | None = None
        
        self.user = tgo.TextView(self.a, "", self.layout)
        
        self.title = tgo.TextView(self.a, "", self.layout)
        self.title.settextsize(20)
        self.title.sendlongclickevent(True)
        self.title.on_longClick = self.on_title
        
        self.img = tgo.ImageView(self.a, self.layout, tgo.View.GONE)
        self.content = tgo.TextView(self.a, "", self.layout, tgo.View.GONE)

        self.bar = tgo.LinearLayout(self.a, self.layout, vertical=False)
        self.upvote = tgo.TextView(self.a, "↑", self.bar)
        self.upvote.settextsize(20)
        self.upvote.setwidth(tgo.View.WRAP_CONTENT)
        self.upvote.setlinearlayoutparams(0)
        self.upvote.setmargin(10, "right")
        self.upvote.sendclickevent(True)
        self.score = tgo.TextView(self.a, "", self.bar)
        self.score.setmargin(10, "right")
        self.score.setwidth(tgo.View.WRAP_CONTENT)
        self.score.setlinearlayoutparams(0)
        self.downvote = tgo.TextView(self.a, "↓", self.bar)
        self.downvote.settextsize(20)
        self.downvote.setwidth(tgo.View.WRAP_CONTENT)
        self.downvote.setlinearlayoutparams(0)
        self.downvote.setmargin(10, "right")
        self.downvote.sendclickevent(True)

        self.comments = tgo.TextView(self.a, "", self.bar)
        self.comments.setwidth(tgo.View.WRAP_CONTENT)
        self.comments.setlinearlayoutparams(0)
        
        self.comment_layout = tgo.LinearLayout(self.a, self.layout)
        self.comment_layout.setwidth(tgo.View.WRAP_CONTENT)
        self.comment_layout.setlinearlayoutparams(0)


from activity import Activity

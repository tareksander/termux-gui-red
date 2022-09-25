from __future__ import annotations

import subprocess
import sys
import urllib.parse

import termuxgui.oo as tgo
import termuxgui as tg
import app
import res

class AuthLayout(tgo.LinearLayout):
    
    
    def on_login(self, e: tg.Event, v: tgo.View):
        try:
            url = urllib.parse.urlparse(self.uri.gettext(), allow_fragments=True)
            if url.scheme != "termux-reddit-client":
                self.a.c.toast("invalid URL", True)
                return
            qp = urllib.parse.parse_qs(url.query)
            if "error" in qp or qp["state"][0] != self.state:
                self.a.c.toast("Error or outdated URL used", True)
                return
            refresh_token = app.reddit.auth.authorize(qp["code"])
            if refresh_token is not None:
                res.write_auth_data(refresh_token)
                self.a.active_layout(self.a.search)
            else:
                self.a.c.toast("Could not retrieve token", True)
        except (ValueError, KeyError) as e:
            self.a.c.toast("Python Error", True)
            print("Error: ", e)
            
    
    def on_back(self):
        sys.exit(0)
    
    
    def on_link(self, e: tg.Event, v: tgo.TextView):
        subprocess.run(["termux-open-url", v.gettext()])
    
    def __init__(self, activity: Activity):
        tgo.LinearLayout.__init__(self, activity, activity.frame, visibility=tgo.View.GONE)
        self.a = activity
        self.setmargin(10)
        
        self.state = app.gen_state()
        
        self.content = tgo.TextView(activity, "Please open the following URL in your browser and autorize this application:", self)
        self.link = tgo.TextView(activity, app.token_url(self.state), self, clickablelinks=True, selectabletext=True)
        self.link.setmargin(20, "top")
        self.content2 = tgo.TextView(activity, "After authorizing, please copy the URI you're redirected to here:", self)
        self.content2.setmargin(20, "top")
        self.uri = tgo.EditText(activity, "", self, singleline=True)
        self.uri.setmargin(20, "top")
        self.login = tgo.Button(activity, "Finish", self)
        self.login.on_click = self.on_login
        self.login.setmargin(20, "top")
        
        self.link.sendclickevent(True)
        self.link.on_click = self.on_link
        
        self.content.setheight(tgo.View.WRAP_CONTENT)
        self.link.setheight(tgo.View.WRAP_CONTENT)
        self.content2.setheight(tgo.View.WRAP_CONTENT)
        self.uri.setheight(tgo.View.WRAP_CONTENT)
        self.login.setheight(tgo.View.WRAP_CONTENT)
        
        self.content.setlinearlayoutparams(0)
        self.link.setlinearlayoutparams(0)
        self.content2.setlinearlayoutparams(0)
        self.uri.setlinearlayoutparams(0)
        self.login.setlinearlayoutparams(0)


from activity import Activity

#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
form= """ <form method="post">
                <table>
                     <tbody>
                        <tr>
                            <td>
                                <label for="username">Username</label>
                            </td>
                            <td>
                                <input name="username" type="text" value="%(user_name)s" required>
                                <span class="error">%(error_username)s</span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label for="password">Password</label>
                            </td>
                            <td>
                                <input name="password" type="password" value required>
                                <span class="error">%(error_password)s</span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label for="verify">Verify Password</label>
                            </td>
                            <td>
                                <input name="verify" type="password" value required>
                                <span class="error">%(error_verify)s</span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label for="email">Email(optional)</label>
                            </td>
                            <td>
                                <input name="email" type="email" value="%(mail)s">
                                <span class="error">%(error_email)s</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <input type="submit">
            </form>

"""


# main_content = form_user + form_password + form_verify + form_email
content = page_header + form + page_footer

class Index(webapp2.RequestHandler):
    def write_form(self, user_name="",mail="",error_username="",error_password="",error_verify="",error_email=""):
        self.response.out.write(content % {"user_name":user_name,
                                            "mail":mail,
                                            "error_username":error_username,
                                            "error_password":error_password,
                                            "error_verify":error_verify,
                                            "error_email":error_email})

    def get(self):

        self.write_form()

    def post(self):

        user_name = self.request.get("username")
        pass_word = self.request.get("password")
        verify_password = self.request.get("verify")
        mail = self.request.get("email")


        # error_message=""
        is_error = False
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        if not valid_username(user_name):
            error_username = "That's not a valid username!"
            is_error = True

        if not valid_password(pass_word):
            error_password = "That's not a valid password!"
            is_error = True

        if not (pass_word == verify_password):
            error_verify = "Passwords don't match!"
            is_error = True

        if not valid_email(mail):
            error_email = "That's not a valid Email!"
            is_error = True

        # error_message = error_username + error_password + error_verify + error_email

        # if error_message is not None:
        if is_error:    
            self.write_form(user_name,mail,error_username,error_password,error_verify,error_email)

        else:
            self.redirect('/welcome?user_name=' + user_name)

            # self.response.write("Welcome," + user_name)



class Welcome(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get("user_name")
        self.response.out.write("<h1>Welcome," + user_name + "</h1>")



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)



# self.redirect("/?error=" + error_message)
# form_user = """ <form method="post">
#                 <table>
#                      <tbody>
#                         <tr>
#                             <td>
#                                 <label for="username">Username</label>
#                             </td>
#                             <td>
#                                 <input name="username" type="text" value required>
#                                 <span class="error">{0}</span>
#                             </td>
#                         </tr>""".format(error_username)
# form_password = """
#                         <tr>
#                             <td>
#                                 <label for="password">Password</label>
#                             </td>
#                             <td>
#                                 <input name="password" type="password" value required>
#                                 <span class="error">{0}</span>
#                             </td>
#                         </tr>""".format(error_password)
#
# form_verify = """
#                         <tr>
#                             <td>
#                                 <label for="verify">Verify Password</label>
#                             </td>
#                             <td>
#                                 <input name="verify" type="password" value required>
#                                 <span class="error">{ver}</span>
#                             </td>
#                         </tr>""".format(ver=error_verify)
#                         # <input name="verify" value="{}">.format(verify)
# form_email = """
#                         <tr>
#                             <td>
#                                 <label for="email">Email(optional)</label>
#                             </td>
#                             <td>
#                                 <input name="email" type="email" value>
#                                 <span class="error">{ema}</span>
#                             </td>
#                         </tr>
#                     </tbody>
#                 </table>
#                 <input type="submit">
#             </form>
#
# """.format(ema=error_email)
#
#
# main_content = form_user + form_password + form_verify + form_email
# content_error = page_header + main_content + page_footer
#
# self.response.out.write(content_error)

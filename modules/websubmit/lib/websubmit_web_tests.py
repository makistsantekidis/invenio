# -*- coding: utf-8 -*-

## This file is part of Invenio.
## Copyright (C) 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""WebSubmit module web tests."""
import time
from invenio.config import CFG_SITE_SECURE_URL
from invenio.testutils import make_test_suite, \
                              run_test_suite, \
                              InvenioWebTestCase


class InvenioWebSubmitWebTest(InvenioWebTestCase):
    """WebSubmit web tests."""

    def test_submit_article(self):
        """websubmit - web test submit an article"""

        self.browser.get(CFG_SITE_SECURE_URL)
        # login as jekyll
        self.login(username="jekyll", password="j123ekyll")

        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Article Submission")
        self.browser.find_element_by_link_text("Demo Article Submission").click()
        self.find_element_by_id_with_timeout("comboARTICLE")
        self.browser.find_element_by_id("comboARTICLE").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()
        self.fill_textbox(textbox_name="DEMOART_REP", text="Test-Ref-001\nTest-Ref-002")
        self.fill_textbox(textbox_name="DEMOART_TITLE", text="Test article document title")
        self.fill_textbox(textbox_name="DEMOART_AU", text="Author1, Firstname1\nAuthor2, Firstname2")
        self.fill_textbox(textbox_name="DEMOART_ABS", text="This is a test abstract.\nIt has some more lines.\n\n...and some empty lines.\n\nAnd it finishes here.")
        self.fill_textbox(textbox_name="DEMOART_NUMP", text="1234")
        self.choose_selectbox_option_by_label(selectbox_name="DEMOART_LANG", label="French")
        self.fill_textbox(textbox_name="DEMOART_DATE", text="11/01/2001")
        self.fill_textbox(textbox_name="DEMOART_KW", text="test keyword1\ntest keyword2\ntest keyword3")
        self.fill_textbox(textbox_name="DEMOART_NOTE", text="I don't think I have any additional comments.\nBut maybe I'll input some quotes here: \" ' ` and the rest.")
        self.find_element_by_xpath_with_timeout("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']")
        self.browser.find_element_by_xpath("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']").click()
        self.wait_element_displayed_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.fill_textbox(textbox_id="balloonReviseFileInput", text="/opt/invenio/lib/webtest/invenio/test.pdf")
        self.find_element_by_id_with_timeout("bibdocfilemanagedocfileuploadbutton")
        self.browser.find_element_by_id("bibdocfilemanagedocfileuploadbutton").click()
        self.wait_element_hidden_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.find_elements_by_class_name_with_timeout('reviseControlFileColumn')
        self.page_source_test(expected_text=['revise', 'tree_branch.gif'])
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>DEMO-ARTICLE-'])
        self.logout()

    def test_submit_book(self):
        """websubmit - web test submit a book"""

        self.browser.get(CFG_SITE_SECURE_URL)
        # login as jekyll
        self.login( username="jekyll", password="j123ekyll")
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Book Submission (Refereed)")
        self.browser.find_element_by_link_text("Demo Book Submission (Refereed)").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()
        self.fill_textbox(textbox_name="DEMOBOO_REP", text="test-bk-ref-1\ntest-bk-ref-2")
        self.fill_textbox(textbox_name="DEMOBOO_TITLE", text="Test book title")
        self.fill_textbox(textbox_name="DEMOBOO_AU", text="Doe, John")
        self.fill_textbox(textbox_name="DEMOBOO_ABS", text="This is a test abstract of this test book record.")
        self.fill_textbox(textbox_name="DEMOBOO_NUMP", text="20")
        self.choose_selectbox_option_by_label(selectbox_name="DEMOBOO_LANG", label="English")
        self.fill_textbox(textbox_name="DEMOBOO_DATE", text="10/01/2001")
        self.fill_textbox(textbox_name="DEMOBOO_KW", text="test keyword 1\ntest keyword 2")
        self.fill_textbox(textbox_name="DEMOBOO_NOTE", text="No additional notes.")
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>DEMO-BOOK-', \
                                             'An email has been sent to the referee.'])
        self.logout()

    def test_submit_book_approval(self):
        """websubmit - web test submit a book approval"""

        import time
        year = time.localtime().tm_year
        self.browser.get(CFG_SITE_SECURE_URL)
        # login as hyde
        self.login(username="hyde", password="h123yde")
        self.browser.get(CFG_SITE_SECURE_URL + "/yourapprovals.py")
        self.page_source_test(expected_text='You are not authorized to use approval system.')
        self.browser.get(CFG_SITE_SECURE_URL + "/publiline.py?doctype=DEMOBOO")
        self.browser.find_element_by_link_text("DEMO-BOOK-%s-001" % str(year)).click()
        self.page_source_test(unexpected_text='As a referee for this document, you may click this button to approve or reject it')
        self.logout()
        # login as dorian
        self.login(username="dorian", password="d123orian")
        self.find_element_by_link_text_with_timeout("your approvals")
        self.browser.find_element_by_link_text("your approvals").click()
        self.page_source_test(expected_text='You are a general referee')
        self.find_element_by_link_text_with_timeout("You are a general referee")
        self.browser.find_element_by_link_text("You are a general referee").click()
        self.page_source_test(expected_text='DEMO-BOOK-')
        self.browser.find_element_by_link_text("DEMO-BOOK-%s-001" % str(year)).click()
        self.page_source_test(expected_text=['Approval and Refereeing Workflow', \
                                             'The record you are trying to access', \
                                             'It is currently restricted for security reasons'])
        self.logout()

    def test_submit_journal(self):
        """websubmit - web test submit a journal"""

        self.browser.get(CFG_SITE_SECURE_URL + "/submit?doctype=DEMOJRN")
        # login as jekyll
        self.login(username="jekyll", password="j123ekyll")
        self.browser.get(CFG_SITE_SECURE_URL + "/submit?doctype=DEMOJRN")
        self.page_source_test(unexpected_text='Arts')
        self.browser.get(CFG_SITE_SECURE_URL)
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.page_source_test(unexpected_text='Demo Journal Submission')
        self.logout()
        # login as romeo
        self.login(username="romeo", password="r123omeo")
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Journal Submission")
        self.browser.find_element_by_link_text("Demo Journal Submission").click()
        self.find_element_by_id_with_timeout("comboARTS")
        self.browser.find_element_by_id("comboARTS").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()
        self.choose_selectbox_option_by_label(selectbox_name="DEMOJRN_TYPE", label="Offline")
        self.fill_textbox(textbox_name="DEMOJRN_ORDER1", text="1")
        self.fill_textbox(textbox_name="DEMOJRN_ORDER2", text="1")
        self.fill_textbox(textbox_name="DEMOJRN_AU", text="Author1, Firstname1\nAuthor2, Firstname2")
        self.fill_textbox(textbox_name="DEMOJRN_TITLEE", text="This is a test title")
        self.fill_textbox(textbox_name="DEMOJRN_TITLEF", text="Ceci est un titre test")
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>BUL-ARTS-'])
        self.logout()

    def test_submit_poetry(self):
        """websubmit - web test submit a poem"""

        self.browser.get(CFG_SITE_SECURE_URL)
        # login as jekyll
        self.login(username="jekyll", password="j123ekyll")
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Poetry Submission")
        self.browser.find_element_by_link_text("Demo Poetry Submission").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()
        self.fill_textbox(textbox_name="DEMOPOE_TITLE", text="A test poem")
        self.fill_textbox(textbox_name="DEMOPOE_AU", text="Doe, John")
        self.choose_selectbox_option_by_label(selectbox_name="DEMOPOE_LANG", label="Slovak")
        self.fill_textbox(textbox_name="DEMOPOE_YEAR", text="1234")
        self.find_element_by_xpath_with_timeout("//strong/font")
        self.browser.find_element_by_xpath("//strong/font").click()
        self.fill_textbox(textbox_name="DEMOPOE_ABS", text=u"This is a test poem<br>\na test poem indeed<br>\nwith some accented characters<br>\n<br>\nΕλληνικά<br> \n日本語<br>\nEspañol")
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>DEMO-POETRY-'])
        self.logout()

    def test_submit_tar_gz(self):
        """websubmit - web test submit an article with a tar.gz file """

        self.browser.get(CFG_SITE_SECURE_URL)
        # login as jekyll
        self.login(username="jekyll", password="j123ekyll")
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Article Submission")
        self.browser.find_element_by_link_text("Demo Article Submission").click()
        self.find_element_by_id_with_timeout("comboARTICLE")
        self.browser.find_element_by_id("comboARTICLE").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()
        self.fill_textbox(textbox_name="DEMOART_REP", text="Test-Ref-001\nTest-Ref-002")
        self.fill_textbox(textbox_name="DEMOART_TITLE", text="Test article tar gz document title")
        self.fill_textbox(textbox_name="DEMOART_AU", text="Author1, Firstname1\nAuthor2, Firstname2")
        self.fill_textbox(textbox_name="DEMOART_ABS", text="This is a test abstract.\nIt has some more lines.\n\n...and some empty lines.\n\nAnd it finishes here.")
        self.fill_textbox(textbox_name="DEMOART_NUMP", text="1234")
        self.choose_selectbox_option_by_label(selectbox_name="DEMOART_LANG", label="French")
        self.fill_textbox(textbox_name="DEMOART_DATE", text="11/01/2001")
        self.fill_textbox(textbox_name="DEMOART_KW", text="test keyword1\ntest keyword2\ntest keyword3")
        self.fill_textbox(textbox_name="DEMOART_NOTE", text="I don't think I have any additional comments.\nBut maybe I'll input some quotes here: \" ' ` and the rest.")
        self.find_element_by_xpath_with_timeout("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']")
        self.browser.find_element_by_xpath("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']").click()
        self.wait_element_displayed_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.fill_textbox(textbox_id="balloonReviseFileInput", text="/opt/invenio/lib/webtest/invenio/test.pdf")
        self.find_element_by_id_with_timeout("bibdocfilemanagedocfileuploadbutton")
        self.browser.find_element_by_id("bibdocfilemanagedocfileuploadbutton").click()
        self.wait_element_hidden_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.find_elements_by_class_name_with_timeout('reviseControlFileColumn')
        self.page_source_test(expected_text=['revise', 'tree_branch.gif'])
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>DEMO-ARTICLE-'])
        self.logout()

    def test_submit_article_guest(self):
        """websubmit - web test submit an article as a guest"""
        self.browser.get(CFG_SITE_SECURE_URL)
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Article Submission")
        self.browser.find_element_by_link_text("Demo Article Submission").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()
        self.fill_textbox(textbox_name="DEMOART_REP", text="Test-Ref-001\nTest-Ref-002")
        self.fill_textbox(textbox_name="DEMOART_TITLE", text="Test article document title")
        self.fill_textbox(textbox_name="DEMOART_AU", text="Author1, Firstname1\nAuthor2, Firstname2")
        self.fill_textbox(textbox_name="DEMOART_ABS", text="This is a test abstract.\nIt has some more lines.\n\n...and some empty lines.\n\nAnd it finishes here.")
        self.fill_textbox(textbox_name="DEMOART_NUMP", text="1234")
        self.choose_selectbox_option_by_label(selectbox_name="DEMOART_LANG", label="French")
        self.fill_textbox(textbox_name="DEMOART_DATE", text="11/01/2001")
        self.fill_textbox(textbox_name="DEMOART_KW", text="test keyword1\ntest keyword2\ntest keyword3")
        self.fill_textbox(textbox_name="DEMOART_NOTE", text="I don't think I have any additional comments.\nBut maybe I'll input some quotes here: \" ' ` and the rest.")
        self.find_element_by_xpath_with_timeout("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']")
        self.browser.find_element_by_xpath("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']").click()
        self.fill_textbox(textbox_id="balloonReviseFileInput", text="/opt/invenio/lib/webtest/invenio/test.pdf")
        self.find_element_by_id_with_timeout("bibdocfilemanagedocfileuploadbutton")
        self.browser.find_element_by_id("bibdocfilemanagedocfileuploadbutton").click()
        self.find_elements_by_class_name_with_timeout('reviseControlFileColumn')
        self.page_source_test(expected_text=['revise', 'tree_branch.gif'])
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>DEMO-ARTICLE-'])

    def test_access_restricted_submission_as_guest(self):
        """websubmit - web test guest must login to access restricted submission"""
        self.browser.get(CFG_SITE_SECURE_URL + '/submit?ln=en&doctype=DEMOTHE')
        self.page_source_test(expected_text=['Password', 'Lost your password?'],
                              unexpected_text=['Submit New Record', \
                                               'Demo Thesis Submission'])
        self.login(username="jekyll", password="j123ekyll", go_to_login_page=False)
        self.page_source_test(expected_text=['Submit New Record', \
                                             'Demo Thesis Submission'])
    def test_revise_picture_admin(self):
        """websubmit - web test submit and revise picture as admin"""
        self.browser.get(CFG_SITE_SECURE_URL + '?ln=en')
        # login as admin
        self.login( username="admin", password="")
        self.find_element_by_link_text_with_timeout("Submit")
        self.browser.find_element_by_link_text("Submit").click()
        self.find_element_by_link_text_with_timeout("Demo Picture Submission")
        self.browser.find_element_by_link_text("Demo Picture Submission").click()
        self.find_element_by_id_with_timeout("comboEXP")
        self.browser.find_element_by_id("comboEXP").click()
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New File']")
        self.browser.find_element_by_xpath("//input[@value='Submit New File']").click()
        self.find_element_by_name_with_timeout("DEMOPIC_RN")
        self.browser.find_element_by_name("DEMOPIC_RN").clear()
        self.fill_textbox(textbox_name="DEMOPIC_RN", text="CERN-GE-9806033")
        self.find_element_by_name_with_timeout("endS")
        self.browser.find_element_by_name("endS").click()
        time.sleep(2)
        self.handle_popup_dialog()
        time.sleep(2)
        self.find_element_by_link_text_with_timeout("revise")
        self.browser.find_element_by_link_text("revise").click()
        self.find_element_by_id_with_timeout("balloonReviseFileInput")
        self.wait_element_displayed_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.fill_textbox(textbox_id="balloonReviseFileInput", text="/opt/invenio/lib/webtest/invenio/test.png")
        self.find_element_by_id_with_timeout("bibdocfilemanagedocfileuploadbutton")
        self.browser.find_element_by_id("bibdocfilemanagedocfileuploadbutton").click()
        time.sleep(1)
        self.wait_element_displayed_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.find_element_by_xpath_with_timeout("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']")
        self.browser.find_element_by_xpath("//div[@id='uploadFileInterface']//input[@type='button' and @value='Add new file']").click()
        self.choose_selectbox_option_by_value(selectbox_id='fileDoctype', value='Additional')
        self.fill_textbox(textbox_name="rename", text="Tiger")
        self.fill_textbox(textbox_id="balloonReviseFileInput", text="/opt/invenio/lib/webtest/invenio/test.pdf")
        self.find_element_by_id_with_timeout("bibdocfilemanagedocfileuploadbutton")
        self.browser.find_element_by_id("bibdocfilemanagedocfileuploadbutton").click()
        time.sleep(1)
        self.wait_element_hidden_with_timeout(self.browser.find_element_by_id("balloonReviseFileInput"))
        self.page_source_test(expected_text='Tiger')
        self.browser.find_element_by_xpath("//div[@id='uploadFileInterface']//tr[@class='even']//a[text()='delete']").click()
        self.handle_popup_dialog()
        time.sleep(1)
        self.find_element_by_name_with_timeout("Submit")
        self.browser.find_element_by_name("Submit").click()
        self.handle_popup_dialog()
        time.sleep(2)
        self.page_source_test(expected_text=['Submission Complete!', \
                                             'Your document has the following reference(s): <b>CERN-GE-9806033'])

    def test_autocompletion_authors(self):

        self.browser.get(CFG_SITE_SECURE_URL)
        self.login(username="admin", password="")
        self.browser.get(CFG_SITE_SECURE_URL+'/submit?ln=en&doctype=DEMOTHE')
        self.find_element_by_xpath_with_timeout("//input[@value='Submit New Record']")
        self.browser.find_element_by_xpath("//input[@value='Submit New Record']").click()


        sel = self.selenium
        sel.open("/?")
        sel.click("link=Submit")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Demo Thesis Submission")
        sel.wait_for_page_to_load("30000")
        sel.click("css=input.adminbutton")
        sel.wait_for_page_to_load("30000")
        submission_no = sel.get_text("css=td > table > tbody > tr > td.submitHeader > small")
        sel.type("name=DEMOTHE_TITLE", sel.get_eval("Math.floor(Math.random()*111111111111)"))
        title = sel.get_value("name=DEMOTHE_TITLE")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[1]")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[2]")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[3]")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[4]")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[5]")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[6]")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[7]")
        author_1 = sel.get_text("id=author_1")
        author_2 = sel.get_text("id=author_2")
        author_3 = sel.get_text("id=author_3")
        author_4 = sel.get_text("id=author_4")
        author_5 = sel.get_text("id=author_5")
        author_6 = sel.get_text("id=author_6")
        author_7 = sel.get_text("id=author_7")
        sel.type("name=DEMOTHE_ABS", sel.get_eval("Math.floor(Math.random()*111111111111)"))
        abstract = sel.get_value("name=DEMOTHE_ABS")
        sel.select("name=DEMOTHE_LANG", "label=English")
        sel.type("name=DEMOTHE_PUBL", "CERN")
        sel.type("name=DEMOTHE_PLDEF", "Geneva")
        sel.select("name=DEMOTHE_DIPL", "label=MSc")
        sel.type("name=DEMOTHE_DATE", "11/11/1991")
        sel.type("name=DEMOTHE_UNIV", "AUTH")
        sel.type("name=DEMOTHE_PLACE", "Thessaloniki")
        sel.type("name=DEMOTHE_FILE", "/home/mike/Downloads/SIPB.pdf")
        sel.send_keys("id=contribution_textfield_1", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_3", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_5", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        contribution_1 = sel.get_value("id=contribution_textfield_1")
        contribution_3 = sel.get_value("id=contribution_textfield_3")
        contribution_5 = sel.get_value("id=contribution_textfield_5")
        sel.click("name=endS")
        sel.wait_for_page_to_load("30000")
        reference = sel.get_text("//b[2]")
        sel.click("link=Submit")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Demo Thesis Submission")
        sel.wait_for_page_to_load("30000")
        sel.click("//input[@value='Modify Record']")
        sel.wait_for_page_to_load("30000")
        sel.type("name=DEMOTHE_RN", reference)
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Author(s)")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Title")
        time.sleep(4)
        sel.click("name=endS")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual(title, sel.get_value("name=DEMOTHE_TITLE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_1, sel.get_value("id=contribution_textfield_0"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_value("id=contribution_textfield_1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_3, sel.get_value("id=contribution_textfield_2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_value("id=contribution_textfield_3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_5, sel.get_value("id=contribution_textfield_4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_value("id=contribution_textfield_5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_value("id=contribution_textfield_6"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_1, sel.get_text("id=author_0"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_2, sel.get_text("id=author_1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_3, sel.get_text("id=author_2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_4, sel.get_text("id=author_3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_5, sel.get_text("id=author_4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_6, sel.get_text("id=author_5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(author_7, sel.get_text("id=author_6"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.send_keys("id=contribution_textfield_0", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_1", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_2", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_3", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_4", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("id=contribution_textfield_5", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        sel.send_keys("name=DEMOTHE_TITLE", sel.get_eval("Math.floor(Math.random()*111111111111)"))
        contribution_0 = sel.get_value("id=contribution_textfield_0")
        contribution_1 = sel.get_value("id=contribution_textfield_1")
        contribution_2 = sel.get_value("id=contribution_textfield_2")
        contribution_3 = sel.get_value("id=contribution_textfield_3")
        contribution_4 = sel.get_value("id=contribution_textfield_4")
        contribution_5 = sel.get_value("id=contribution_textfield_5")
        title = sel.get_value("name=DEMOTHE_TITLE")
        sel.send_keys("id=author_textbox", "asa")
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*asa[\s\S]*$", sel.get_text("css=p.author_autocomplete_name_field")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("xpath=(//p[contains(@class,'author_autocomplete_name_field')])[9]")
        sel.send_keys("id=contribution_textfield_6", sel.get_eval("Math.floor(Math.random()*111111111111)+\"\\\n\" + Math.floor(Math.random()*111111111111)"))
        contribution_6 = sel.get_value("id=contribution_textfield_6")
        time.sleep(0.01)
        sel.click("name=End")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Submit")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Demo Thesis Submission")
        sel.wait_for_page_to_load("30000")
        sel.click("//input[@value='Modify Record']")
        sel.wait_for_page_to_load("30000")
        sel.type("name=DEMOTHE_RN", reference)
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Other Report Numbers")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Title")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Subtitle")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Author(s)")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Supervisor(s)")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Abstract")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Number of Pages")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Language")
        time.sleep(4)
        sel.click("name=endS")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual(title, sel.get_value("name=DEMOTHE_TITLE"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_0, sel.get_value("id=contribution_textfield_0"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_1, sel.get_value("id=contribution_textfield_1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_2, sel.get_value("id=contribution_textfield_2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_3, sel.get_value("id=contribution_textfield_3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_4, sel.get_value("id=contribution_textfield_4"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_5, sel.get_value("id=contribution_textfield_5"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_6, sel.get_value("id=contribution_textfield_6"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_value("id=contribution_textfield_7"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(abstract, sel.get_value("name=DEMOTHE_ABS"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//img[@onclick='delete_author(this,2)']")
        sel.click("//img[@onclick='delete_author(this,3)']")
        sel.click("//img[@onclick='delete_author(this,4)']")
        sel.click("name=End")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Submit")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Demo Thesis Submission")
        sel.wait_for_page_to_load("30000")
        sel.click("//input[@value='Modify Record']")
        sel.wait_for_page_to_load("30000")
        sel.type("name=DEMOTHE_RN", reference)
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Author(s)")
        sel.add_selection("name=DEMOTHE_CHANGE[]", "label=Title")
        time.sleep(3)
        sel.click("name=endS")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual(contribution_0, sel.get_value("id=contribution_textfield_0"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_1, sel.get_value("id=contribution_textfield_1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_5, sel.get_value("id=contribution_textfield_2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(contribution_6, sel.get_value("id=contribution_textfield_3"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_value("id=contribution_textfield_4"))
        except AssertionError, e: self.verificationErrors.append(str(e))

TEST_SUITE = make_test_suite(InvenioWebSubmitWebTest, )

if __name__ == '__main__':
    run_test_suite(TEST_SUITE, warn_user=True)

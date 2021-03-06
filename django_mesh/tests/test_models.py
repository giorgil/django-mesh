# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Test imports
from .util import BaseTestCase

class PostTestCase(BaseTestCase):
    def test_has_auto_summary(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        self.assertEqual(self.p1.summary, self.p1.teaser)
        self.assertNotEqual(self.p1.summary, self.p1.custom_summary)

    def test_has_custom_summary(self):
        self.c1.save()
        self.p1.custom_summary = 'This is a summary.'
        self.p1.channel = self.c1
        self.p1.save()
        
        self.assertNotEqual(self.p1.summary, self.p1.teaser)
        self.assertEqual(self.p1.summary, self.p1.custom_summary)

    def test_render_stays_the_same_when_no_links(self):
        self.assertNotEqual(self.p1.text, '')
        self.assertEqual(self.p1.rendered_text, '')

        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        self.assertEqual(self.p1.rendered_text, self.p1.text)

    def test_render_adds_anchors(self):
        self.p1.text = """foo
            http://somelink
            http://anotherlink
        """

        self.assertEqual(self.p1.rendered_text, '')

        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        self.assertEqual(self.p1.rendered_text, """foo
            <a href="http://somelink">http://somelink</a>
            <a href="http://anotherlink">http://anotherlink</a>
        """)

    def test_get_absolute_url(self):
        self.c1.save()
        self.p1.channel = self.c1
        url = self.p1.get_absolute_url()

        self.assertGreater(len(url),0)

    def test_str_unicode(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()


        returned_title = str(self.p1)
        self.assertEqual(self.p1.title, returned_title)

class ChannelTestCase(BaseTestCase):
    def test_get_absolute_url(self):
        self.c1.save()
        url = self.c1.get_absolute_url()
        self.assertGreater(len(url),0)

    def test_str_unicode(self):
        self.c1.save()

        returned_title = str(self.c1)
        self.assertEqual(self.c1.title, returned_title)

class TagTestCase(BaseTestCase):

    def test_get_absolute_url(self):
        self.t1.save()
        url = self.t1.get_absolute_url()

        self.assertGreater(len(url), 0)

    def test_str_unicode(self):
        self.t1.save()
        returned_title = str(self.t1)
        self.assertEqual(self.t1.title, returned_title)

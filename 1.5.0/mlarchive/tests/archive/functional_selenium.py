'''Selenium Functional Tests'''

import urlparse
import pytest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from mlarchive.archive.models import Message


timeout = 10


class MySeleniumTests(StaticLiveServerTestCase):
    '''Selenium functional test cases'''
    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(1400, 1000)
        # cls.selenium.PhantomJS(service_log_path='tests/tmp/ghostdriver.log')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    # TEST MESSAGE VIEW NAVIGAIONS

    @pytest.mark.usefixtures("thread_messages")
    def test_message_detail_next_list(self):
        '''Test next message in list button of message detail'''
        messages = Message.objects.all().order_by('date')
        url = urlparse.urljoin(self.live_server_url, messages[0].get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_link_text('Next in List').click()
        
        # Wait until the response is received
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        
        # Get results page
        # print self.selenium.page_source
        self.selenium.get_screenshot_as_file('tests/tmp/test_message_detail_next_list.png')
        self.assertIn('Archive', self.selenium.title)
        self.assertIn(messages[1].msgid, self.selenium.page_source)
        # elements = self.selenium.find_elements_by_xpath("//*[contains(text(), '00002@example.com')]")
        # self.assertEqual(len(elements),1)

    @pytest.mark.usefixtures("thread_messages")
    def test_message_detail_previous_list(self):
        '''Test previous message in list button of message detail'''
        messages = Message.objects.all().order_by('date')
        self.assertEqual(len(messages), 4)
        url = urlparse.urljoin(self.live_server_url, messages[1].get_absolute_url())
        self.selenium.get(url)
        self.selenium.find_element_by_link_text('Previous in List').click()
        
        # Wait until the response is received
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        
        # Get results page
        # print self.selenium.page_source
        self.selenium.get_screenshot_as_file('tests/tmp/test_message_detail_previous_list.png')
        self.assertIn('Archive', self.selenium.title)
        self.assertIn(messages[0].msgid, self.selenium.page_source)

        
from webdriver_bot import SeleniumBot
from selenium.webdriver.chrome.options import Options

class CheetosBot(SeleniumBot):
    def __init__(self):
        SeleniumBot.__init__(self)
    
    def vote(self):
        self.go_to_page('https://www.cheetos.lt/index/galerii/images/librariesprovider3/osalejad/kanar%C4%97l%C4%97?itemIndex=30')
        self.solve_captcha()
    
    def solve_captcha(self):
        captcha_frame = self.get_element_by_css_selector("iframe[sandbox='allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox']")
        self.driver.switch_to_frame(captcha_frame)
        im_not_robot_button = self.get_element_by_css_selector(".rc-anchor-checkbox-holder")
        self.post_click_or_submit(im_not_robot_button)
        audio_button = self.get_element_by_css_selector("buton.rc-button.goog-inline-block.rc-button-audio")

    def switch_to_default_content(self):
        self.driver.switch_to_default_content()

try:
    bot = CheetosBot()
    bot.vote()
except Exception as e:
    print(e)
    bot.driver.quit()
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

class Recaptcha:
    def __init__(self, url, siteKey):
        self.url = url
        self.siteKey = siteKey
        self.apiKey = 'minhaKey'
    
    def resolver(self):

        solver = TwoCaptcha(self.apiKey)

        try:
            result = solver.recaptcha(
                sitekey=self.siteKey,
                url=self.url)
            return result

        except Exception as e:
            sys.exit(e)

        else:
            sys.exit('solved: ' + str(result))
            return result
        

import unittest
from main import authorize
from main import isNext
from main import isPrev
from main import isTicket
import requests

class Tester(unittest.TestCase):
    def testAuthorize(self):
        #test authorization
        self.assertEqual(authorize("david021301@gmail.com","Asmallturtle123!"),0)
        self.assertEqual(authorize("asdf", "asdf"), 1)
    def testPaging(self):
        #test paging for various numbers of tickets
        self.assertTrue(isNext(3,100), True)
        self.assertFalse(isNext(7, 3), False)
        self.assertFalse(isNext(4, 100), False)
        self.assertTrue(isNext(4, 110), True)

        self.assertTrue(isPrev(2), True)
        self.assertFalse(isPrev(1), False)
    def testFindTicket(self):
        #test trying to find an individual ticket in a page
        curr = requests.get('https://zccstudent.zendesk.com/api/v2/tickets.json?page[size]=25', auth=('david021301@gmail.com', 'Asmallturtle123!'))

        self.assertTrue(isTicket(60,500,curr.json()))
        curr = requests.get(curr.json()["links"]["next"],
                         auth=('david021301@gmail.com', 'Asmallturtle123!'))
        self.assertTrue(isTicket(80, 500, curr.json()))
        curr = requests.get(curr.json()["links"]["next"],
                         auth=('david021301@gmail.com', 'Asmallturtle123!'))
        self.assertFalse(isTicket(300, 500, curr.json()))
        curr = requests.get(curr.json()["links"]["prev"],
                            auth=('david021301@gmail.com', 'Asmallturtle123!'))
        self.assertTrue(isTicket(79, 500, curr.json()))
        self.assertFalse(isTicket(400, 500, curr.json()))
        self.assertFalse(isTicket(60, 500, curr.json()))
if __name__ == '__main__':
    unittest.main()



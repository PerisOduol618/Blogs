import unittest
from app.models import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(password = 'mango')
    
    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)
    
    def test_no_access_password(self):
        with self.assertRaises(ArithmeticError):
            self.new_user.password


    def test_password_verfication(self):
        self.assertTrue(self.new_user.verify_password('mango'))     
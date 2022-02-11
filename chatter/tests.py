from django.test import TestCase
import requests
import json

# from backend root, run: python manage.py test [-v 2] 
# run with --keepdb to creep on your test_db after tests: `test_chatter`
# 
# looks like the test_db starts out with no seed, but with correct schema
# 
# note: you'll need to have several things for this to work
#       - `requests` package, currently in dev dependecies of Pipfile
#               install this via pipenv install --dev
#       - run settings.sql to allow your app to create a test db:
#                ALTER USER chatteruser CREATEDB;
#       - have the development server running on port 8000
#       - manually generated users (user/alice/bob) described below
#               this can be worked into setUp() method down the road.
#   
# disclaimer: no idea what best practices are here

# Create your tests here.
class EnpointResponseTests(TestCase):

    def setUp(self):
        
        # specify these here in unittest convention?
        self.base_url = 'http://127.0.0.1:8000/'  # faster than localhost for me
        self.method =  'GET'
        self.headers = {'Content-Type': 'application/json'}
        self.data = None

        # TODO - do login once here, and use token for multiple tests
        self.authToken = None
        

    def make_params(self):
        pass
    
    @staticmethod
    def make_auth_header(access_token):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'JWT {access_token}'  # Bearer (?)
        }

    def make_request(
        self,
        endpoint,
        method=None,
        params=None,
        headers=None,
        data=None,
        expect_html=False,
        verbose=False,
        return_obj=False,
        ):
        
        if method is None: method = self.method
        if headers is None: headers = self.headers
        if data is None: data = self.data

        url = self.base_url + endpoint
        
        if params is not None:
            url += params

        r = requests.request(
            method,
            url=url, 
            data=json.dumps(data),
            headers=headers,
            )

        if return_obj: return r

        if not(r.ok):
            try: 
                if verbose: print(f'request failed {r.status_code}')
                if verbose: print(f'content: {r.content}')
            except: pass
            return

        if expect_html:
            try: response = r.content
            except: 
                if verbose: print(f'could not get content from expect_html response')
        
        else:
            try: response = r.json()
            except Exception as e:
                if verbose: print(f'failed to parse response json: {e}')
                if verbose: print(r.content)
                return
        
        return response

    # # # --------- TESTS --------------------------------- # # #
    # all testing function must use `test_` naming 
    # these test rely on having users: {`user`, `alice`, `bob`}
    # each with password: `password`
    # # # --------------------------------------------------# # #

    def test_login_basic(self):
        
        # login
        endpoint = 'auth/login/'
        method = 'POST'
        data = {'username': 'user', 'password': 'password'}
        token_res = self.make_request(endpoint=endpoint, method=method, data=data)
        
        # test login token
        self.assertIsNotNone(token_res)
        self.assertIsInstance(token_res.get('access', None), str)
        self.assertIsInstance(token_res.get('refresh', None), str)

        # make un-authorized request to protected route
        endpoint = 'auth/getmessages/alice_user/'
        noauth_res = self.make_request(endpoint=endpoint)

        # test that this 40X's
        self.assertIsNone(noauth_res)

        # make authorized request
        endpoint = 'auth/getmessages/alice_user/'
        headers = self.make_auth_header(token_res['access'])
        auth_res = self.make_request(endpoint=endpoint, headers=headers) 
        
        # test this succeeds
        self.assertIsNotNone(auth_res)

        # make bad authorized request
        endpoint = 'auth/getmessages/alice_user/'
        headers = self.make_auth_header('wrong_token')
        badauth_res = self.make_request(endpoint=endpoint, headers=headers) 

        # test this fails
        self.assertIsNone(badauth_res)        


    def test_user_specific_chat_auth(self):
        
        # login as user
        endpoint = 'auth/login/'
        method = 'POST'
        data = {'username': 'user', 'password': 'password'}
        token_res = self.make_request(endpoint=endpoint, method=method, data=data)
        self.assertIsNotNone(token_res)

        # make authorized request with `user` to chatroom `alice_bob`
        endpoint = 'auth/getmessages/alice_bob/'
        headers = self.make_auth_header(token_res['access'])
        spy_res = self.make_request(endpoint=endpoint, headers=headers) 

        # you should not be able to get chatroom messages as `user`
        self.assertIsNone(spy_res)  # currently this fails


    def test_bad_login_1(self):
        
        # login request with wrong password
        endpoint = 'auth/login/'
        method = 'POST'
        data = {'username': 'user', 'password': 'wrong_password'}
        token_res_obj = self.make_request(endpoint=endpoint, method=method, data=data, return_obj=True)
        
        self.assertEqual(token_res_obj.status_code, 401)

        # login request with no empty data object in body
        endpoint = 'auth/login/'
        method = 'POST'
        data = {}
        token_res_obj = self.make_request(endpoint=endpoint, method=method, data=data, return_obj=True)
        
        self.assertEqual(token_res_obj.status_code, 400)


    def test_getmessages_response_data(self):
        
        # login
        endpoint = 'auth/login/'
        method = 'POST'
        data = {'username': 'user', 'password': 'password'}
        token_res = self.make_request(endpoint=endpoint, method=method, data=data)
        self.assertIsNotNone(token_res)

        # make good request
        endpoint = 'auth/getmessages/alice_user/'
        headers = self.make_auth_header(token_res['access'])
        chat_res = self.make_request(endpoint=endpoint, headers=headers) 
        self.assertIsNotNone(chat_res)

        # match response to seed data
        # ALICE_USER_CHAT_DATA = [{"message": "no way", "sender": 2}, {"message": "blah blah", "sender": 1}]
        # This won't work untill we seed properly, leaving 
        # as template for later
        # self.assertEqual(chat_res, ALICE_USER_CHAT_DATA)
        # self.assertDictContainsSubset({}, chat_res)


    def test_getmessages_unsafe_methods(self):
        
        # login
        endpoint = 'auth/login/'
        method = 'POST'
        data = {'username': 'user', 'password': 'password'}
        token_res = self.make_request(endpoint=endpoint, method=method, data=data)
        self.assertIsNotNone(token_res)

        # make good request
        endpoint = 'auth/getmessages/alice_user/'
        method = 'POST'
        headers = self.make_auth_header(token_res['access'])
        chat_res = self.make_request(endpoint=endpoint, method=method, headers=headers) 
        
        # as a POST, this should fail
        self.assertIsNone(chat_res)

        # make good request
        endpoint = 'auth/getmessages/alice_user/'
        method = 'PUT'
        headers = self.make_auth_header(token_res['access'])
        chat_res = self.make_request(endpoint=endpoint, method=method, headers=headers) 
        
        # as a PUT, this should fail
        self.assertIsNone(chat_res)


    def test_getmessages_param_order_bad(self):
        # getmessages/alice_user vs getmessages/user_alice
        pass


if __name__ == "__main__":

    # you can use this section to run invididual tests via:
    # >python tests.py
    # you can go into the code and turn on print stuff out, 
    # and only run this one
    t_obj = EnpointResponseTests()
    t_obj.setUp()
    t_obj.test_getmessages_unsafe_methods()
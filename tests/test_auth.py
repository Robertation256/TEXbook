import requests


def test_get_token():
    response = requests.post(
        url="http://127.0.0.1:5000/auth/token",
        data={
            "email": "yz3919@nyu.edu"
        }
    )
    cookie = response.cookies
    print("token_response: ", response.content)
    print("token_cookies:", requests.utils.dict_from_cookiejar(cookie))
    return cookie
def test_email_verify(cookie: dict, token: str):
    response = requests.post(
        url="http://127.0.0.1:5000/auth/email_verify",
        data={
            "token": token
        },
        cookies=cookie
    )

    cookie = response.cookies
    print("verify_cookies:", requests.utils.dict_from_cookiejar(cookie))
    print("verify_response:", response.text)


def test_register(cookie):
    response = requests.post(
        url="http://127.0.0.1:5000/auth/register",
        data={
            "username": "robert.zhang",
            "password": "robert.zhang"
        },
        cookies=cookie
    )
    print("register_response:", response.text)


def test_login():
    response = requests.post(
        url="http://127.0.0.1:5000/auth/login",
        data={
            "email": "yz3919@nyu.edu",
            "password": "robert.zhang"
        },
    )
    cookie = response.cookies
    print("login_response:", response.text)
    print("login_cookies:", requests.utils.dict_from_cookiejar(cookie))


if __name__ == "__main__":
    # cookie = test_get_token()
    # token = input("enter token")
    # test_email_verify(cookie=cookie, token=token)
    # test_register(cookie)
    test_login()



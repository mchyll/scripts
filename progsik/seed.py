import requests
import random
import string


base_url = "https://localhost:462"

def print_req_resp(resp: requests.Response):
    req = resp.request

    # Print request
    print('\n{}\r\n{}\r\n\r\n{}'.format(
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body))

    # Print response
    print('\n{}\r\n{}\r\n\r\n{}\n'.format(
        str(resp.status_code) + ' ' + resp.reason,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in resp.headers.items()),
        resp.content.decode("utf8"))) # .decode("utf8")[-75:]


_csrf_token = None
def post(session: requests.Session, path, data):
    global _csrf_token
    if not _csrf_token:
        _csrf_token = input("CSRF token pls: ")

    resp = session.post(base_url + path,
        data=data + "&csrf_token=" + _csrf_token,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        verify=False)

    for intermediate_resp in resp.history:
        print_req_resp(intermediate_resp)

    print_req_resp(resp)


def rnd_str(k=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))


with requests.Session() as s:
    # # Make user magnus
    # print("***** Make user magnus\n")
    # post(s, "/register",
    #     data="username=magnus&full_name=j&company=j&email=m%40t.nmo&street_address=j&city=j&state=j&postal_code=1212&country=j&password=magnusconrad&Register=")

    # # Make user test
    # print("\n\n***** Make user test\n")
    # post(s, "/register",
    #     data="username=test&full_name=j&company=j&email=m%40t.nmo&street_address=j&city=j&state=j&postal_code=1212&country=j&password=magnusconrad&Register=")

    # # Log in as magnus
    # print("\n\n***** Log in as magnus\n")
    # post(s, "/login",
    #     data="username=magnus&password=password&remember=False&Log+In=")

    # # Create a new project on user magnus
    # print("\n\n***** Create a new project on user magnus\n")
    # post(s, "/new_project",
    #     data="project_title={}&project_description=fds&category_name=1&task_title_0={}&task_description_0=fds&budget_0=123123&user_name_0=&read_permission_0=True&create_project=create_project".format(rnd_str(), rnd_str()))

    print("***** Get login page")
    print_req_resp(s.get(base_url + "/register", verify=False))

    # Make user magnus
    print("\n\n***** Make user magnus")
    post(s, "/register",
        data="username=magnus&full_name=Din+dust&company=ssj&email=magnus%40hyll.no&street_address=jjj+2&city=jee&state=jaa&postal_code=1212&country=loll&password=Fuckfuckfuck123&Register=")

    # Make user test
    print("\n\n***** Make user test")
    post(s, "/register",
        data="username=test&full_name=Din+test&company=ssj&email=magnus%40testt.no&street_address=jjj+2&city=jee&state=jaa&postal_code=1212&country=loll&password=Fuckfuckfuck123&Register=")

    print("\n\n***** Validating users")
    s.get(input("Validation URL pls: "))
    s.get(input("Validation URL pls: "))

    # Log in as magnus
    print("\n\n***** Log in as magnus")
    post(s, "/login",
        data="username=magnus&password=Fuckfuckfuck123&remember=False&Log+In=")

    # Create a new project on user magnus
    print("\n\n***** Create a new project on user magnus")
    post(s, "/new_project",
        data="project_title={}&project_description=fds&category_name=1&task_title_0={}&task_description_0=fds&budget_0=123123&user_name_0=&read_permission_0=True&create_project=create_project".format(rnd_str(), rnd_str()))

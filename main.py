import asyncio

from config import initialize_driver, LOGIN_URL
from handle_submit import handle
from input import get_user_credentials
from auto_login import auto_login


async def main():

    driver = initialize_driver(LOGIN_URL)
    username, password = get_user_credentials()
    is_login = await auto_login(driver,username,password)

    while not is_login:
        print("Vui lòng nhập lại thông tin đăng nhập.")
        username, password = get_user_credentials()
        is_login = await auto_login(driver, username, password)
        

    if is_login:
        await handle(driver)
    else:
        print("Login failed, cannot submit assignment.")


if __name__ == "__main__":
    asyncio.run(main())

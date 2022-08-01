from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def launchSeleniumWebdriver():
    global driver
    option = webdriver.ChromeOptions()
    s = Service("chromedriver.exe")
    # 用户个人资料路径
    option.add_argument("--user-data-dir=" + r'D:\ChromeSelenium')
    driver = webdriver.Chrome(options=option, service=s)  # 此时将webdriver.exe 保存到python Script目录下

    return driver


def checkAlert():
    while True:
        try:
            element = driver.find_element(By.XPATH, '//span[text()="Close"]')
        except NoSuchElementException:
            print("no alert")
            break
        else:
            driver.find_element(By.XPATH, '//span[text()="Close"]').click()
            break


def checkElement(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        print(f"no element {xpath}")
        return False
    else:
        return True


def conncetMetaMask():
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    inputs = driver.find_elements(By.XPATH, '//input')
    # MetaMask密码
    inputs[0].send_keys('password')
    driver.find_element(By.XPATH, '//button[text()="解锁"]').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)


def connectPremint():
    flag = checkElement('//a[text()="Connect"]')
    if not flag:
        print("no connect button")
        return
    driver.find_element(By.XPATH, '//a[text()="Connect"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//a[@title="Twitter"]').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


def connectDiscord():
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://discord.com/channels/@me')
    time.sleep(3)
    flag = checkElement('//div[text()="登录"]')
    if not flag:
        print("no 登录 button")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return
    driver.find_element(By.XPATH, '//div[text()="登录"]').click()
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def register(num):
    # 打印打开第num个页面
    print(f'open page {num}')
    # connectPremint()
    flag = checkElement('//button[@type="submit"]')
    if not flag:
        print("no register button")
        return

    pre_element_list = driver.find_elements(By.XPATH, "//div[@class='card-body p-0']//a[@href]")
    premint_url_list = []
    # 通过a标签的href属性获取url，并存入列表
    for i in range(0, len(pre_element_list)):
        url = pre_element_list[i].get_attribute('href')
        premint_url_list.append(url)
    # 去重
    premint_url_list = list(set(premint_url_list))
    # 筛选链接的前缀
    twitter_url_list = [i for i in premint_url_list if i.startswith('https://twitter.com/')]
    dcord_url_list = [i for i in premint_url_list if i.startswith('https://discord.gg/')]
    # 进一步筛选retweet链接
    retweet_url_list = [i for i in twitter_url_list if 'user' in i]
    # 从twitter_url_list中去除retweet_url_list中的链接
    for i in retweet_url_list:
        twitter_url_list.remove(i)

    # 关注推特
    if len(twitter_url_list) > 0:
        for i in twitter_url_list:
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[2])
            driver.get(i)
            time.sleep(2)
            follow_flag = checkElement('//span[text()="关注"]')
            if follow_flag:
                driver.find_element(By.XPATH, '//span[text()="关注"]').click()
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
    # retweet&like
    if len(retweet_url_list) > 0:
        for i in retweet_url_list:
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[2])
            driver.get(i)
            time.sleep(1)
            retweet_flag = checkElement('//div[@aria-label="转推"]')
            if retweet_flag:
                driver.find_element(By.XPATH, '//div[@aria-label="转推"]').click()
                time.sleep(1)
                driver.find_element(By.XPATH, '//span[text()="转推"]').click()
                time.sleep(1)
            like_flag = checkElement('//div[@aria-label="喜欢"]')
            if like_flag:
                driver.find_element(By.XPATH, '//div[@aria-label="喜欢"]').click()
                time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
    # 关注discord
    if len(dcord_url_list) > 0:
        for i in dcord_url_list:
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[2])
            driver.get(i)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[2])
            invite_flag = checkElement("//div[text()='接受邀请']")
            if invite_flag:
                driver.find_element(By.XPATH, "//div[text()='接受邀请']").click()
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
    # 搜索页面中是否有role
    text = driver.find_element(By.XPATH, "//*[text()]")
    role = "role"
    if role in text.text:
        print("need role, close page")
        print(driver.current_url)
        fp_role = open('need_role.txt', 'a', encoding='utf-8')
        fp_role.write(driver.current_url + '\n')
        fp_role.close()
        return
    fp1 = open('can_auto.txt', 'a', encoding='utf-8')
    fp1.write(driver.current_url + '\n')
    fp1.close()
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)
    Success_flag = checkElement('//div[@class="card rounded-0 bg-success no-border"]')
    if not Success_flag:
        print(driver.current_url)
        fp_role = open('need_submit.txt', 'a', encoding='utf-8')
        fp_role.write(driver.current_url + '\n')
        fp_role.close()
        return


def getUrl():
    driver.get('https://nftbusy.xyz/#/premint/index')
    time.sleep(2)
    driver.refresh()
    checkAlert()
    time.sleep(1)
    connect_flag = checkElement('//span[text()="Connect "]')
    if connect_flag:
        driver.find_element(By.XPATH, '//span[text()="Connect "]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
        time.sleep(2)
    element_list = driver.find_elements(By.XPATH, "//div[@class='main-container']//a[@href]")
    get_url_list = []
    # 通过a标签的href属性获取url，并存入列表
    for i in range(0, len(element_list)):
        url = element_list[i].get_attribute('href')
        get_url_list.append(url)
    # 去重
    get_url_list = list(set(get_url_list))
    # 写入文件
    fp_url = open('url.txt', 'a', encoding='utf-8')
    for i in get_url_list:
        fp_url.write(i + '\n')
    fp_url.close()
    return get_url_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    driver = launchSeleniumWebdriver()
    driver.implicitly_wait(5)
    driver.get('https://www.premint.xyz/home/')
    connectDiscord()
    conncetMetaMask()
    # 读取url列表
    fp = open('url.txt', 'r', encoding='utf-8')
    url_list = fp.readlines()
    fp.close()
    # 如果url列表为空，则获取url列表
    if len(url_list) == 0:
        url_list = getUrl()

    for i in range(0, len(url_list)):
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url_list[i])
        register(i)
        driver.close()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])

    print("done")
    time.sleep(600)
    driver.quit()

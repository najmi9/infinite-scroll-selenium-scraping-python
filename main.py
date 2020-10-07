from time import sleep
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import csv
username = "username"
password = "password"
login_url = "https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.startupschool.org%2Fusers%2Fsign_in"
main_url = "https://www.startupschool.org/directory"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
chrome_options.add_argument('--enable-automation')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.headless=False

driver = webdriver.Chrome(executable_path = "../chromedriver", chrome_options=chrome_options)

driver.set_window_size(800,1000)
driver.set_window_position(0,0)

def d(n,m):
	sleep(random.randint(n,m))

def scroll(timeout):
    scroll_pause_time = timeout
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def login(driver):
	driver.get(login_url)
	d(5,7)
	driver.find_element_by_xpath('//input[@id="ycid-input"]').send_keys(username)
	driver.find_element_by_xpath('//input[@id="password-input"]').send_keys(password)
	d(1,2)
	driver.find_element_by_xpath('//button[@type="submit"]').click()
	d(8,10)
	cookies = driver.get_cookies()
	pickle.dump(cookies, open('cookies.pickle', 'wb'))

def do_job(driver):
	driver.get(main_url)
	print(driver.title)
	btn = None
	d(5,9)
	try:
		btn = driver.find_element_by_css_selector('button.MuiButtonBase-root.MuiButton-root.MuiButton-text.MuiButton-textSecondary')
	except:
		pass
	if btn:
		login(driver)
		driver.get(main_url)
		d(4,6)
	scroll(3)
	data = driver.find_elements_by_xpath('//div[@class="css-1m1qrud e1gne1cu2"]')
	
	print('data = ', len(data))
	with open('data.csv', 'w') as f:
		csv_file = csv.writer(f)
		csv_file.writerow(["name", "description", "type", "stage"])
	
	for i, post in enumerate(data):
		try:
			name = post.find_element_by_css_selector('a.css-hcep6').text
			desc = post.find_element_by_tag_name('p').text
			types = post.find_element_by_css_selector("p.css-ytno8o")
			types = types.find_element_by_tag_name('div').text
			stage = post.find_element_by_css_selector('div.css-1e0wass').text
			with open('data.csv', 'a') as f:
				csv_file = csv.writer(f)
				csv_file.writerow([name, desc, types, stage])
			print("profile n: {} ----- {}".format(i, name))
		except:
			pass
	print('done...')

	driver.quit()
	driver.close()
		

def main():
	driver.get(login_url)	
	try:
		cookies = pickle.load(open('cookies.pickle', 'rb'))
		for cookie in cookies:
			driver.add_cookie(cookie)
		d(5,8)
		print('cookies added successfly ...')
	except Exception as e:
		print("login.....")
		login(driver)

	print('do job ....')
	do_job(driver)
	
if __name__ == '__main__':
	main()

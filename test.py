from selenium.webdriver import Chrome, ChromeOptions
#options = ChromeOptions()
#options.add_argument('--headless')
driver = Chrome()
#driver.get("https://transit.yahoo.co.jp")
driver.get("https://ja.wikipedia.org/wiki/A")
v_sform = driver.find_element_by_id("sfrom")
v_sform.send_keys("南草津")
v_sto = driver.find_element_by_id("sto")
v_sform.send_keys("河原町")
v_sto.submit()
#v_f = v_browser.find_element_by_class_name("fare").text.replace("円","")
#print(v_f)
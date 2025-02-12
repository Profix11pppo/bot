#-*-coding:utf-8-*-
import telebot
from telebot import types
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#from pyvirtualdisplay import Display
import time
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

bot = telebot.TeleBot('955162419:AAHEWIgPxqd7QbRAOQZrNYlo7DYmQoR3Jlg')

x = 0
y = 0

@bot.message_handler(commands=['start'])
def start(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT id FROM users')
	ids = c.fetchall()
	k = 0
	for i in ids:
		print(i)
		if (i[0] == message.chat.id):
			k+=1
	if (k==0):
		bot.send_message(message.chat.id,"""
	Для того, чтобы начать, тебе нужно зарегистрироваться. 
	Для этого введи свой ник Инстаграм без знака @ . 
			""")
		bot.register_next_step_handler(message, registration)
	else:
		bot.send_message(message.chat.id, "Добро пожаловать!")
		main_menu(message)

def registration(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT id FROM users')
	ids = c.fetchall()
	k = 0
	for i in ids:
		print(i)
		if (i[0] == message.chat.id):
			k+=1
	if (k == 0):
		c.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)', (message.chat.id, message.from_user.first_name, message.text, 0, 0, 0, 0))
		conn.commit()
	else:
		c.close()
		conn.close()
		main_menu(message)
		print(k)
	c.close()
	conn.close()
	bot.send_message(message.chat.id,"""
		Отлично. Теперь ты можешь приступить к работе с ботом.
			""")
	main_menu(message)

@bot.message_handler(content_types=['text'])
def non_registration(message):
	if (message.text == "Личный кабинет"):
		lk(message)
	if (message.text == "FAQ"):
		FAQ(message)
	if (message.text == "Баланс"):
		balance(message)
	if (message.text == "Задания"):
		missions(message)
	if (message.text == "Выполнить задания"):
		do_missions(message)
	if (message.text == "Выложить свое задание"):
		make_self_mission(message)
	if (message.text == "Связь с администрацией"):
		admin_request(message)
	if (message.text == "Общая информация"):
		public_information(message)
	if (message.text == "Назад в меню"):
		main_menu(message)
	if (message.text == "Назад"):
		missions(message)
	if (message.text == "Готово"):
		check_mission(message)
	if (message.text == "Отмена"):
		lk(message)
	if (message.text == "Заработать баллы"):
		do_missions(message)
	if (message.text == "Выйти в главное меню"):
		main_menu(message)
	if (message.text == "Сменить аккаунт instagram"):
		akk_request(message)
	if (message.text == "Информация о профиле"):
		profile_info(message)
	if (message.text == "Пропустить задание"):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('SELECT miscount FROM users WHERE id = ?', (message.chat.id,))
		num = c.fetchone()
		c.execute('UPDATE users SET miscount = ? WHERE id = ?', (num[0] + 1, message.chat.id))
		conn.commit()
		c.close()
		conn.close()
		bot.send_message(message.chat.id, "Вы пропустили задание, вот новое")
		do_missions(message)

def main_menu(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Задания')
	markup.add('Личный кабинет', 'Связь с администрацией', 'FAQ')
	bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
	bot.register_next_step_handler(message, handler_menu)

def handler_menu(message):
	if (message.text == "Личный кабинет"):
		lk(message)
	if (message.text == "Задания"):
		missions(message)

def admin_request(message):
	markup = types.ReplyKeyboardMarkup(row_width=0.5)
	markup.add('Назад')
	bot.send_message(message.chat.id, "Для связи с администрацией напишите @RRR686", reply_markup=markup)


def lk(message):
	markup = types.ReplyKeyboardMarkup(row_width=0.5)
	markup.add('Баланс', 'Сменить аккаунт instagram', 'Информация о профиле', 'Выйти в главное меню')
	bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
	bot.register_next_step_handler(message, handler_lk)

def FAQ(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	bot.send_message(message.chat.id,"""
		Инструкция к боту:
		1. Бот написан без официального API, поэтому запросы, возможно, будут обрабатываться не так быстро
		2. Если при нажатии на определенную кнопку действие не произошло, то нажмите повторно
		3. Если есть вопросы по улучшению бота, то напишите в директ @RRR686

		""")
def handler_lk(message):
	if (message.text == "Баланс"):
		balance(message)
	if (message.text == "Сменить аккаунт instagram"):
		akk_request(message)
	if (message.text == "Информация о профиле"):
		profile_info(message)

def profile_info(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT insta_nick FROM users WHERE id = ?', (message.chat.id,))
	nick = c.fetchone()
	c.close()
	conn.close()
	mess = "---Информация о профиле---\n - ID: {0}\n - Имя: {1} \n- Привязанный аккаунт: {2}".format(str(message.chat.id), message.from_user.first_name, nick[0])
	bot.send_message(message.chat.id, mess)
def akk_request(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Отмена','Выйти в главное меню')
	bot.send_message(message.chat.id, "Отправьте новый ник инстаграм или нажмите Отмена", reply_markup=markup)
	bot.register_next_step_handler(message, change_nick)

def change_nick(message):
	if (message.text == "Отмена"):
		lk(message)
	else:
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('UPDATE users SET insta_nick = ? WHERE id = ?', (message.text, message.chat.id))
		conn.commit()
		c.close()
		conn.close()
		bot.send_message(message.chat.id, "Логин изменен")



def missions(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Получить комментарии', 'Раздать комментарии', 'Назад в меню')
	bot.send_message(message.chat.id, "Меню заданий", reply_markup=markup)
	bot.register_next_step_handler(message, handler_missions)

def handler_missions(message):
	if (message.text == "Получить комментарии"):
		make_self_mission(message)
	if (message.text == "Раздать комментарии"):
		ra_make_self_mission(message)
	# if (message.text == "Общая информация"):
	# 	public_information(message)
	if (message.text == "Назад в меню"):
		main_menu(message)

def do_missions(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Готово', 'Пропустить задание', 'Проблема с публикацией', 'Назад')
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT miscount FROM users WHERE id = ?', (message.chat.id,))
	count = c.fetchone()
	print(count[0])
	c.execute('SELECT txt FROM missions WHERE num = ?', (count[0]+1,))
	miss = c.fetchone()
	text = miss[0]
	c.close()
	conn.close()
	bot.send_message(message.chat.id, "\x20\x20---Задание для вас---\n\n" + text, disable_web_page_preview=True, reply_markup=markup)
	bot.register_next_step_handler(message, middle_do_missions)

def middle_do_missions(message):
	if (message.text == "Готово"):
		check_mission(message)
	if (message.text == "Пропустить задание"):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('SELECT miscount FROM users WHERE id = ?', (message.chat.id,))
		num = c.fetchone()
		c.execute('UPDATE users SET miscount = ? WHERE id = ?', (num[0] + 1, message.chat.id))
		conn.commit()
		c.close()
		conn.close()
		bot.send_message(message.chat.id, "Вы пропустили задание, вот новое")
		do_missions(message)
	if (message.text == "Проблема с публикацией"):
		bot.send_message(message.chat.id, "Опишите проблему и скиньте ссылку на публикацию администратору @RRR686")
	if (message.text == "Назад"):
		missions(message)

def check_mission(message):
	markup = types.ReplyKeyboardMarkup(row_width=1)
	markup.add('Следующее задание', 'Назад')
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT miscount FROM users WHERE id = ?', (message.chat.id,))
	num = c.fetchone()
	c.execute('SELECT txt FROM missions WHERE num = ?', (num[0] + 1,))
	lonk = c.fetchone()
	c.execute('SELECT insta_nick FROM users WHERE id = ?', (message.chat.id,))
	nick = c.fetchone()
	link = link_find(lonk[0])
	answer = check_comm(nick[0], link)
	if (answer == 1):
		c.execute('UPDATE users SET balance = ? WHERE id = ?', (check_balance(message) + 10, message.chat.id))
		conn.commit()
		c.execute('UPDATE users SET miscount = ? WHERE id = ?', (num[0] + 1, message.chat.id))
		conn.commit()
		c.execute('SELECT x FROM users WHERE id = ?', (message.chat.id,))
		x = c.fetchone()
		c.execute('UPDATE users SET x = ? WHERE id = ?', (x[0] + 1, message.chat.id))
		conn.commit()
		c.execute('SELECT y FROM users WHERE id = ?', (message.chat.id,))
		y = c.fetchone()
		if (x[0] == y[0]):
			if (y[0] == 7):
				five(message)
			if (y[0] == 12):
				ten(message)
			if (y[0] == 17):
				fifteen(message)
		else:
			bot.send_message(message.chat.id, "Поздравляем, вы заработали 10 баллов", reply_markup=markup)
			bot.register_next_step_handler(message, handler_mission_step)
	else:
		bot.send_message(message.chat.id,"Задание не выполнено! Выполните задание и нажмите кнопку Готово")
	c.close()
	conn.close()

def handler_mission_step(message):
	if (message.text == "Следующее задание"):
		do_missions(message)

def make_self_mission(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('5', '10', '15', 'Назад')
	bot.send_message(message.chat.id, "Сколько комментариев вы хотите получить?", reply_markup=markup)
	bot.register_next_step_handler(message, self_mission_answer)

def balls(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Заработать баллы', 'Назад в меню')
	bot.send_message(message.chat.id, "Выберите дейтсвие", reply_markup=markup)
	bot.register_next_step_handler(message, handler_no_balance)

def ra_make_self_mission(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('5', '10', '15', 'Назад')
	bot.send_message(message.chat.id, "Сколько комментариев вы хотите Раздать?", reply_markup=markup)
	bot.register_next_step_handler(message, ra_comm)

def ra_comm(message):
	if (message.text == "5"):
		do_missions(message)
	if (message.text == "10"):
		do_missions(message)
	if (message.text == "15"):
		do_missions(message)

def self_mission_answer(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	markup.add('Заработать баллы', 'Назад в меню')
	balance = check_balance(message)
	if (message.text == "Назад"):
		missions(message)
	if (message.text == "5"):
		if balance >= 50:
			conn = sqlite3.connect('data.db')
			c = conn.cursor()
			conn.commit()
			c.execute('UPDATE users SET balance = ? WHERE id = ?', (balance-50, message.chat.id))
			conn.commit()
			c.close()
			conn.close()
			bot.send_message(message.chat.id, "Введите текст задания и ссылку на пост")
			bot.register_next_step_handler(message, five)
		else:
			conn = sqlite3.connect('data.db')
			c = conn.cursor()
			conn.commit()
			c.execute('UPDATE users SET y = ? WHERE id = ?', (7, message.chat.id))
			conn.commit()
			c.close()
			conn.close()
			bot.send_message(message.chat.id, """
				Упс! Кажется у тебя не хватает баллов для получения комментариев. Тебе нужно их заработать. Просто жми кнопку «Заработать» и дерзай!
				""", reply_markup=markup)
			bot.register_next_step_handler(message, handler_no_balance)
			#make_self_mission(message)
	if (message.text == "10"):
		if balance >= 100:
			conn = sqlite3.connect('data.db')
			c = conn.cursor()
			conn.commit()
			c.execute('UPDATE users SET balance = ? WHERE id = ?', (balance-100, message.chat.id))
			conn.commit()
			c.close()
			conn.close()
			bot.send_message(message.chat.id, "Введите текст задания и ссылку на пост")
			bot.register_next_step_handler(message, ten)
		else:
			conn = sqlite3.connect('data.db')
			c = conn.cursor()
			conn.commit()
			c.execute('UPDATE users SET y = ? WHERE id = ?', (12, message.chat.id))
			conn.commit()
			c.close()
			conn.close()
			bot.send_message(message.chat.id, "Ваш баланс недостаточен для отправки своего задания", reply_markup=markup)
			bot.register_next_step_handler(message, handler_no_balance)
	if (message.text == "15"):
		if balance >= 150:
			conn = sqlite3.connect('data.db')
			c = conn.cursor()
			conn.commit()
			c.execute('UPDATE users SET balance = ? WHERE id = ?', (balance-150, message.chat.id))
			conn.commit()
			c.close()
			conn.close()
			bot.send_message(message.chat.id, "Введите текст задания и ссылку на пост")
			bot.register_next_step_handler(message, fifteen)
		else:
			conn = sqlite3.connect('data.db')
			c = conn.cursor()
			conn.commit()
			c.execute('UPDATE users SET y = ? WHERE id = ?', (17, message.chat.id))
			conn.commit()
			c.close()
			conn.close()
			bot.send_message(message.chat.id, "Ваш баланс недостаточен для отправки своего задания", reply_markup=markup)
			bot.register_next_step_handler(message, handler_no_balance)

def handler_no_balance(message):
	if (message.text == "Заработать баллы"):
		do_missions(message)
	if (message.text == "Выйти в главное меню"):
		main_menu(message)

def five(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 5):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()
	bot.send_message(message.chat.id, "Задание опубликовано")


def ten(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 10):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()
	bot.send_message(message.chat.id, "Задание опубликовано")


def fifteen(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 15):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()
	bot.send_message(message.chat.id, "Задание опубликовано")
	

def twenty(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 20):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()

def thirty(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 30):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()

def forty(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 40):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()

def fifty(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT num FROM missions WHERE ROWID IN ( SELECT max( ROWID ) FROM missions )')
	num = c.fetchone()
	c.close()
	conn.close()
	for i in range(0, 50):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		conn.commit()
		c.execute('INSERT INTO missions VALUES(?, ?)', (num[0] + 1, message.text))
		conn.commit()
		c.close()
		conn.close()
	
def balance(message):
	bot.send_message(message.chat.id, "Баланс: " + str(check_balance(message)))
	missions(message)

def check_balance(message):
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	conn.commit()
	c.execute('SELECT balance FROM users WHERE id = ?', (message.chat.id,))
	balance = c.fetchone()
	c.close()
	conn.close()
	return balance[0]

def link_find(any):
	link = ""
	haram = True
	index = -1

	for i in range(0, len(any)):
		#if ''.join(any[i]) == 'h' and ''.join(any[i+1]) == 't' and ''.join(any[i+2]) == 't':
		if any[i] == 'h' and any[i+1] == 't' and any[i+2] == 't':
			index = i
			break


	for i in range(0, len(any)):
		try:
			for j in range(0, len(any)):
				#if ''.join(any[j]) == 'i' and ''.join(any[j+1]) == 'n' and ''.join(any[j+2]) == 's' and ''.join(any[j+3]) == 't' and  ''.join(any[j+4]) == 'a':
				if any[j] == 'i' and any[j+1] == 'n' and any[j+2] == 's' and any[j+3] == 't' and  any[j+4] == 'a':
					haram = False
					break
		except:
			haram = True

	if index != -1:
		for j in range(index, len(any)):
			if any[j] != "\n":
				link += any[j]
			else:
				break
	else:
		link = "None"

	#if haram == True:
	#    link = "None"
	#print(link)


	return link

def check_comm(nick, link):
	check = 0
	answer = 0
	chrome_options = Options()
	chrome_options.add_argument("start-maximized")
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	#driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
	driver = webdriver.Chrome(executable_path='/home/pupkin/usr/local/bot/chromedriver', chrome_options=chrome_options)
	#driver.get("https://www.instagram.com/accounts/login")
#
	#inputElement = driver.find_element_by_name("username")
	#inputElement.send_keys('khalilov.tg')
#
	#inputElement = driver.find_element_by_name("password")
	#inputElement.send_keys('ddayasxk')
#
	#inputElement.send_keys(Keys.ENTER)

	#display = Display(visible=0, size=(1024, 768))
	#display.start()
	#binary = r'/usr/bin/firefox'
	#options = FirefoxOptions()
	#options.add_argument("--headless")
	#options.binary = binary
	#cap = DesiredCapabilities().FIREFOX
	#cap["marionette"] = False
	#driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path='/home/gm/zakaz/geckodriver')

	#new_link = "https://" + link

	try:
		driver.get(link)
	except:
		try:
			driver.get(link)
		except:
			try:
				driver.get(link)
			except:
				pass
	print(nick)



	# driver.find_element_by_class_name("zV_Nj").click()
	# try:
	# 	but=driver.find_element_by_class_name("dCJp8").find_element_by_tag_name("button")
	# 	but.click()
	# except Exception as e:
	# 	print(e)
	# 	pass

	inputElement = driver.find_elements_by_class_name("Mr508")

	if len(inputElement) == 0:
		try:
			driver.get(link)
			inputElement = driver.find_elements_by_class_name("Mr508")
		except:
			try:
				driver.get(link)
				inputElement = driver.find_elements_by_class_name("Mr508")
			except:
				try:
					driver.get(link)
					inputElement = driver.find_elements_by_class_name("Mr508")
				except:
					pass
	print(nick)
	while check == 0:
		for i in range(0, len(inputElement)):
			try:

				print(inputElement[i].find_element_by_class_name("_6lAjh").get_attribute("innerText"))#_6lAjh
				k = 0
				try:
					comment = inputElement[i].find_element_by_tag_name("span").get_attribute("innerText")
					print(comment)
				except Exception as e:
					print(e)
					pass
				for g in range(0, len(comment)):
					if comment[g] != ' ':
						k += 1
				if nick in inputElement[i].find_element_by_class_name("_6lAjh").get_attribute("innerText"):
					check = 1
					break
			except Exception as e:
				#print(e)
				pass
		if check == 0:
			try:
				but=driver.find_element_by_class_name("dCJp8").find_element_by_tag_name("button")
				but.click()
			except Exception as e:
				#print(str(e))
				break
			try:
				but=driver.find_element_by_class_name("dCJp8").find_element_by_tag_name("button")
				but.click()
			except:
				pass
			try:
				inputElement = driver.find_elements_by_class_name("Mr508")
			except Exception as e:
				#print(e)
				pass
	if check == 1:
		driver.close()
		try:
			driver.quit()
		except:
			pass
		answer = 1
	else:
		driver.close()
		try:
			driver.quit()
		except:
			pass
			
	try:
		subprocess.call(["killall", "Xvfb"])
	except:
		pass

	try:
		subprocess.call(["killall", "chrome"])
		#subprocess.call(["killall", "chromedriver"])
	except:
		pass 

	return answer

bot.polling()

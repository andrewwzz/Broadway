from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from wordles import wordles
from wordles import guesses
import time

STARTING_WORD = "SALET"

solutions = wordles
guesses = guesses


def get_shadow(host):
    shadow = driver.execute_script("return arguments[0].shadowRoot", host)
    return shadow


def appears_later(word, result, i):
    for x in range(i + 1, 5):
        if word[i] == word[x] and result[x] > 0:
            return True
    return False


def calculate_next_word(word, result):
    global solutions
    print(result)
    for x in range(5):
        if result[x] == 0:
            solutions = [w for w in solutions if word[x] not in w or appears_later(word, result, x)]
            # print(f"solutions0: {solutions}")
        if result[x] == 1:
            solutions = [w for w in solutions if word[x] != w[x] and word[x] in w]
            # print(f"solutions1: {solutions}")
        if result[x] == 2:
            solutions = [w for w in solutions if word[x] == w[x]]
            # print(f"solutions2: {solutions}")
    print(f"Possible words left: {solutions}")
    guess = solutions[0]
    return guess


PATH = "C:\Program Files (x86)\Chromedriver\chromedriver"
service = Service(PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.nytimes.com/games/wordle/index.html")

# remove modal
driver.find_element(by=By.TAG_NAME, value="html").click()

actions = ActionChains(driver)

"""
structure of elements
<game-app>
    #shadow-root
        <game-row>
            #shadow-root
                <div class=row>
                    <game-tile letter="s" evaluation="absent">
                    <game-tile letter="a" evaluation="present">
                    <game-tile letter="l" evaluation="absent">
                    <game-tile letter="e" evaluation="correct">
                    <game-tile letter="t" evaluation="absent">
"""
possible_results = {"absent": 0, "present": 1, "correct": 2}
result = [None] * 5
prev_word = STARTING_WORD
for i in range(6):
    # calculate and type out the next word
    word = STARTING_WORD if i == 0 else calculate_next_word(prev_word.lower(), result).lower()
    actions.send_keys(f"{word}{Keys.ENTER}").perform()

    # get results for that word
    app = driver.find_element(by=By.TAG_NAME, value="game-app")
    row = get_shadow(app).find_elements(by=By.TAG_NAME, value='game-row')[i]
    letters = get_shadow(row).find_elements(by=By.TAG_NAME, value="game-tile")
    for j, letter in enumerate(letters):
        result[j] = possible_results[letters[j].get_attribute("evaluation")]

    # if solved
    if sum(result) == 10:
        print(f"Solved the Wordle in {i + 1} guesses.")
        break

    prev_word = word
    time.sleep(2)

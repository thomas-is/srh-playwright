#!/venv/bin/python

import os
import dateparser
import sys

from datetime import datetime
from playwright.sync_api import sync_playwright

day     = sys.argv[1]
on_site = ( sys.argv[2] == "office" )

VIDEO_DIR = "/home/python/videos/"

def msg(text):
    print(f"{text}", flush=True)

def get_selector(ymd):
    return f'[id*="{ymd}"]'

def get_today_selector():
    today = datetime.now().strftime("%Y-%m-%d")
    return get_selector(today)

def login(page):

    url        = os.getenv("LOGIN_URL")
    username   = os.getenv("USERNAME")
    password   = os.getenv("PASSWORD")

    page.goto(url)

    msg(f"👨 login")
    user_field = page.locator('input#id.champConnexion')
    user_field.fill(username)
    pw_field = page.locator('input#pw.champConnexion')
    pw_field.fill(password)
    button = page.get_by_role("button", name="Connexion")
    button.click()

def working_time_open(page):
    msg(f"⌛ wait for the app to be loaded")
    selector = '[data-cy="CsMenuBar-folded-item-my_working_time"]'
    page.locator(selector).wait_for(state="attached", timeout=10000)
    msg(f"⚙️  open my_working_time")
    e = page.locator(selector)
    e.hover()
    page.wait_for_timeout(500)
    selector = '[data-cy="CsShutter-my_working_time-item-wc_gpsCollab"]'
    page.locator(selector).wait_for(state="attached", timeout=10000)
    e = page.locator(selector)
    e.click()
    msg(f"⌛ wait for the planning to be loaded")
    page.wait_for_timeout(5000)

def working_time_send(page):
    msg(f"✉️  send")
    e = page.get_by_text('Envoyer les demandes')
    e.click()
    page.wait_for_timeout(3000)


def working_time_set(page, day="today", on_site=False):

    ymd = dateparser.parse(day).strftime("%Y-%m-%d")

    status = "office" if on_site else "remote"

    msg(f'⚙️  set {ymd} as {status}')
    # this is the manager cell for a certain date
    # the cell just below is ours
    selector = get_selector(ymd)
    page.wait_for_timeout(5000)
    msg(f"  ℹ️  {selector}")
    e = page.locator(selector).bounding_box()
    x = e['x'] + e['width'] / 2    # center on manager cell
    y = e['y'] + e['height'] * 1.5 # center on manager cell and go below one row

    page.mouse.click(x, y, button='right')
    page.wait_for_timeout(1000)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowDown")
    if on_site:
        page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")

    selector='input[placeholder="Motif"]'
    msg(f"  ℹ️  {selector}")
    e = page.locator(selector)
    e.click()
    page.wait_for_timeout(1000)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)

    selector = 'button[title="Ajouter"]'
    msg(f"  ℹ️  {selector}")
    e = page.locator(selector)
    e.click()
    page.wait_for_timeout(2000)


def run(playwright, day="today", on_site=False):

    user_agent = os.getenv("USER_AGENT")
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    context = browser.new_context(
        record_video_dir=VIDEO_DIR,
        record_video_size={"width": 800, "height": 600},
        user_agent=user_agent
    )
    page = context.new_page()

    login(page)
    working_time_open(page)
    working_time_set(page, day=day, on_site=on_site)
    working_time_send(page)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    msg("🚀 launch playwright")
    run(playwright, day=day, on_site=on_site)


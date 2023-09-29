import requests
import re
import threading
import random
import json
import os
import time
import sys
from colorama import Fore, Style, init

init(convert=True)
os.system("cls")

cookies = input("\033[1;97mVui lòng nhập cookies Facebook: ")


def banner():
    banner = f"""
\033[1;97m~ \033[1;92mTool : \033[1;97mSpam CMT Đa Luồng
\033[1;97m~ \033[1;92mAuthor : \033[1;97mThiệu Trung Kiên
\033[1;97m~ \033[1;92mFacebook : \033[1;97mhttps://facebook.com/ThieuTrungKi3n/
\033[1;97m~ \033[1;92mGithub : \033[1;97mhttps://github.com/ttkienn
\033[1;97m- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"""
    for X in banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        time.sleep(0.0000100)


os.system("clear")
os.system("cls")
banner()

count = 0
count_lock = threading.Lock()


def increment_count():
    global count
    with count_lock:
        count += 1


class FB:
    def __init__(self, cookies):
        self.headers = {
            "cookie": cookies,
            "Host": "d.facebook.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "connection": "keep-alive",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

    def comment(self, reply_id, id_post, c_user, comment):
        session = requests.Session()

        response = session.get("https://d.facebook.com/", headers=self.headers)
        data = response.text

        fb_dtsg = re.search(
            r'<input type="hidden" name="fb_dtsg" value="([^"]+)"', data
        ).group(1)
        jazoest = re.search(
            r'<input type="hidden" name="jazoest" value="([^"]+)"', data
        ).group(1)

        comment_data = {
            "fb_dtsg": fb_dtsg,
            "jazoest": jazoest,
            "comment_text": comment,
        }
        comment_headers = {
            **self.headers,
            "user-agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36 Edg/117.0.0.0",
        }
        response = session.post(
            f"https://d.facebook.com/a/comment.php?parent_comment_id={reply_id}&fs=0&comment_logging&ft_ent_identifier={id_post}&av={c_user}",
            data=comment_data,
            headers=comment_headers,
        )

        if response.status_code == 200:
            increment_count()
            return {"status": True, "data": "Comment thành công!"}
        else:
            return {"status": False, "data": "Comment không thành công!"}


def comment_on_post(cookies, reply_id, post_id, c_user, comment):
    increment_count()
    while True:
        action = FB(cookies)
        result = action.comment(reply_id, post_id, c_user, comment)
        with count_lock:
            current_count = count
            print(
                f"{Fore.GREEN}[ TTK ]{Style.RESET_ALL}: {current_count} | {result['data']} | {comment}"
            )

num_threads = int(input("\033[1;97mNhập số luồng muốn chạy: "))
linkReply = input("\033[1;97mVui lòng nhập link comment bạn cần spam : ")
postID = linkReply.split("ft_ent_identifier=")[1].split("&")[0]
parentCommentID = linkReply.split("ctoken=")[1].split("&")[0].split("_")[1]
cookie_pairs = cookies.split(";")
for pair in cookie_pairs:
    key, value = pair.strip().split("=")
    if key == "c_user":
        c_user_value = value
        break
print(
    "\033[1;97m- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
)
comment_text = ["Thiệu Trung Kiên", "TTK Dz VKL"]
with open(f"emoji.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
threads = []
for i in range(num_threads):
    thread = threading.Thread(
        target=comment_on_post,
        args=(
            cookies,
            parentCommentID,
            postID,
            c_user_value,
            random.choice(comment_text) + " " + random.choice(data),
        ),
    )
    threads.append(thread)
    thread.start()

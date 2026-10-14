"""
In this project, you will build a simple command line interface (CLI) to fetch the recent activity of a GitHub user and display it in the terminal. This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.
 --- Requirements:
 The application should run from the command line, accept the GitHub username as an argument, fetch the user's recent activity using the GitHub API, and display it in the terminal. The user should be able to:

Provide the GitHub username as an argument when running the CLI.

github-activity>username
"""

import requests, json, argparse
from pprint import pprint

USER = ""
DATA_FILE = "data.json"

# Funtion to load data from json file
def load_json_file(json_file):
    try:
        with open(json_file, mode="r", encoding="utf-8") as src_file:
            return json.load(src_file)
    except FileNotFoundError:
        print(f"File {json_file} is not found!")
        return []
    except json.JSONDecodeError:
        print(f"File {json_file} is not in json format.")
        return []

# Function to save json data file
def save_json_file(array, json_file):
    with open(json_file, mode="w", encoding="utf-8") as des_file:
        json.dump(array, des_file, indent=4, ensure_ascii=False)
        print(f"Saved successful file {json_file}.")

# Function get data from API
def get_data_from_API(api_user):
    url = f"https://api.github.com/users/{api_user}/events"
    try:
        response = requests.get(url, timeout=5)
        # Check response status from requests function
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: GitHub API returned status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}!")

def github_Act_CLI():
    parser = argparse.ArgumentParser(description="Fetch recent activity of a GitHub user.")
    parser.add_argument("username", type=str, help="Github username.")
    args = parser.parse_args()
    return args.username

def display_activity(events):
    if not events:
        print(f"No activities recently.")
        return 
    print(f"----- Activities on Github recently. -----")
    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")
        payload = event.get("payload", {})

        #Process events on Github
        if event_type == "PushEvent":
            #Count commits quantity in payload
            commits = payload.get("commit", [])
            commit_count = len(commits) if commits else payload.get("size", 1)
            print(f"- Pushed {commit_count} commits to repo name {repo_name}.")

        elif event_type == "CreateEvent":
            ref_type = payload.get("ref_type") # branch, repository, tag
            ref = payload.get("ref", "")
            if ref_type == "repository":
                print(f"- Created a new repository {repo_name}")
            else:
                print(f"- Created a {ref_type} {ref} in {repo_name}.")

        elif event_type == "IssuesEvent":
            action = payload.get("action")  # opened, closed, reopened...
            print(f"- {action.capitalize()} an issue in {repo_name}")

        elif event_type == "WatchEvent":
            print(f"- Starred {repo_name}")

        elif event_type == "PullRequestEvent":
            action = payload.get("action")
            print(f"- {action.capitalize()} a pull request in {repo_name}")

        else:
            # Các loại sự kiện khác hiển thị dạng tổng quát
            clean_type = event_type.replace("Event", "")
            print(f"- Performed {clean_type} on {repo_name}")


def main():
    print("=== GitHub Activity CLI ===")
    print("Gõ tên username để xem hoạt động, hoặc gõ 'exit' để thoát.\n")

    # A loop to receive a command
    while True:
        try:
            # Tạo dòng nhắc lệnh tùy chỉnh
            user_input = input("github-activity> ").strip()
            
            # Nếu người dùng muốn thoát
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            # Nếu người dùng bấm Enter mà không gõ gì
            if not user_input:
                continue
                
            username = user_input
            print(f"Đang tải dữ liệu của user: {username}...")
            
            data_file = get_data_from_API(username)
            if data_file is not None:
                save_json_file(data_file, DATA_FILE)
                data = load_json_file(DATA_FILE)
                display_activity(data)
                
            print("-" * 40) # Dòng phân cách giữa các lần tra cứu
            
        except KeyboardInterrupt:
            # Xử lý khi người dùng bấm Ctrl + C để thoát an toàn
            print("\nGoodbye!")
            break


if __name__ =="__main__":
    main()
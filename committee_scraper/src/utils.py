import sys
import requests

def extract_list(s: []):
    start = s.find('[')
    end = s.find(']', start + 1)
    if start != -1 and end != -1:
        return s[start + 1:end]
    else:
        return None

def extract_emails(s: []):
    contact_list = s[0]
    for i in range(1, len(s)):
        contact_list += ", " + s[i]
    return contact_list


# Validate the format of an email address
def validate_email(email: str) -> bool:
    accepted_special_characters = "!#$%&'*+-/=?^_`{|}~"
    if not str(email).__contains__("@"):
        return False
    decomposed_email = str(email).split("@")
    local = decomposed_email[0]
    domain = decomposed_email[1]
    for char in local:
        ascii_val = ord(char)
        if char in accepted_special_characters or (48 > ascii_val > 57) and (63 > ascii_val > 90) and (
                97 > ascii_val > 122) and (ascii_val != 126):
            return False
    for char in domain:
        ascii_val = ord(char)
        if (48 > ascii_val > 57) and (63 > ascii_val > 90) and (97 > ascii_val > 122) and (ascii_val != 126):
            return False
    return True

# Validate a URL returns a 200 code
def validate_request(url: str) -> bool:
    try:
        request = requests.get(url)
        return request.status_code == 200
    except Exception as e:
        print(f'{url} : {e.__str__()}')
        return False

# Print progress bar
def print_bar(index: int, total: int) -> None:
    if total == 0:
        return
    n_bar = 50
    progress = index / total
    filled = int(n_bar * progress)
    bar_filled = '█' * filled
    bar_empty = '░' * (n_bar - filled)
    sys.stdout.write('\r')
    sys.stdout.write(
        f"Search Progress: \033[0;32m{bar_filled}\033[0m\033[0;31m{bar_empty}\033[0m {int(100 * progress)}% Complete")
    sys.stdout.flush()

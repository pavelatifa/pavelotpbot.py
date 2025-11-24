import time
import requests
import logging
import json
import os
import re
import asyncio
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TimedOut

if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

BOT_TOKEN = os.getenv('BOT_TOKEN','8254431259:AAFfZLlRbtaAqpbCTHmRHPAKg2phtZtdT4o')
CHAT_IDS = ['-1003087083001',]
USERNAME = os.getenv('PANEL_USERNAME', 'numberpanelotp')
PASSWORD = os.getenv('PANEL_PASSWORD', 'numberpanelotp')

print("\n" + "=" * 60)
print("🤖 TELEGRAM OTP BOT")
print("=" * 60)
print(f"📝 Panel Username: {USERNAME}")
print(f"🔐 Panel Password: {'*' * len(PASSWORD)}")
print(f"🤖 Bot Token: {BOT_TOKEN[:20] if BOT_TOKEN else 'NOT SET'}...")
print(f"📱 Target Channels: {len(CHAT_IDS)} channels")
print("=" * 60 + "\n")
BASE_URL = "http://51.89.99.105/"

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN is not set!")
    print("   Please add BOT_TOKEN to Replit Secrets")
    exit(1)

if USERNAME == 'Agent07':
    print("⚠️  WARNING: Using default credentials. Please update PANEL_USERNAME and PANEL_PASSWORD!")
    print("   Set environment variables in Replit Secrets.")

LOGIN_PAGE_URL = BASE_URL + "/NumberPanel/login"
LOGIN_POST_URL = BASE_URL + "/NumberPanel/signin"
DATA_URL = BASE_URL + "/NumberPanel/client/res/data_smscdr.php"

bot = Bot(token=BOT_TOKEN)
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})
logging.basicConfig(level=logging.INFO, format='%(message)s')

COUNTRY_MAP = {
    '1': '🇺🇸 USA / Canada',
    '7': '🇷🇺 Russia / Kazakhstan',
    '20': '🇪🇬 Egypt',
    '27': '🇿🇦 South Africa',
    '30': '🇬🇷 Greece',
    '31': '🇳🇱 Netherlands',
    '32': '🇧🇪 Belgium',
    '33': '🇫🇷 France',
    '34': '🇪🇸 Spain',
    '36': '🇭🇺 Hungary',
    '39': '🇮🇹 Italy / Vatican City',
    '40': '🇷🇴 Romania',
    '41': '🇨🇭 Switzerland',
    '43': '🇦🇹 Austria',
    '44': '🇬🇧 United Kingdom',
    '45': '🇩🇰 Denmark',
    '46': '🇸🇪 Sweden',
    '47': '🇳🇴 Norway / Svalbard',
    '48': '🇵🇱 Poland',
    '49': '🇩🇪 Germany',
    '51': '🇵🇪 Peru',
    '52': '🇲🇽 Mexico',
    '53': '🇨🇺 Cuba',
    '54': '🇦🇷 Argentina',
    '55': '🇧🇷 Brazil',
    '56': '🇨🇱 Chile',
    '57': '🇨🇴 Colombia',
    '58': '🇻🇪 Venezuela',
    '60': '🇲🇾 Malaysia',
    '61': '🇦🇺 Australia / Christmas Island',
    '62': '🇮🇩 Indonesia',
    '63': '🇵🇭 Philippines',
    '64': '🇳🇿 New Zealand / Pitcairn Islands',
    '65': '🇸🇬 Singapore',
    '66': '🇹🇭 Thailand',
    '81': '🇯🇵 Japan',
    '82': '🇰🇷 South Korea',
    '84': '🇻🇳 Vietnam',
    '86': '🇨🇳 China',
    '90': '🇹🇷 Turkey',
    '91': '🇮🇳 India',
    '92': '🇵🇰 Pakistan',
    '93': '🇦🇫 Afghanistan',
    '94': '🇱🇰 Sri Lanka',
    '95': '🇲🇲 Myanmar',
    '98': '🇮🇷 Iran',
    '211': '🇸🇸 South Sudan',
    '212': '🇲🇦 Morocco / Western Sahara',
    '213': '🇩🇿 Algeria',
    '216': '🇹🇳 Tunisia',
    '218': '🇱🇾 Libya',
    '220': '🇬🇲 Gambia',
    '221': '🇸🇳 Senegal',
    '222': '🇲🇷 Mauritania',
    '223': '🇲🇱 Mali',
    '224': '🇬🇳 Guinea',
    '225': '🇨🇮 Côte d\'Ivoire',
    '226': '🇧🇫 Burkina Faso',
    '227': '🇳🇪 Niger',
    '228': '🇹🇬 Togo',
    '229': '🇧🇯 Benin',
    '230': '🇲🇺 Mauritius',
    '231': '🇱🇷 Liberia',
    '232': '🇸🇱 Sierra Leone',
    '233': '🇬🇭 Ghana',
    '234': '🇳🇬 Nigeria',
    '235': '🇹🇩 Chad',
    '236': '🇨🇫 Central African Republic',
    '237': '🇨🇲 Cameroon',
    '238': '🇨🇻 Cape Verde',
    '239': '🇸🇹 Sao Tome & Principe',
    '240': '🇬🇶 Equatorial Guinea',
    '241': '🇬🇦 Gabon',
    '242': '🇨🇬 Congo',
    '243': '🇨🇩 DR Congo',
    '244': '🇦🇴 Angola',
    '245': '🇬🇼 Guinea-Bissau',
    '246': '🇮🇴 British Indian Ocean Territory',
    '248': '🇸🇨 Seychelles',
    '249': '🇸🇩 Sudan',
    '250': '🇷🇼 Rwanda',
    '251': '🇪🇹 Ethiopia',
    '252': '🇸🇴 Somalia',
    '253': '🇩🇯 Djibouti',
    '254': '🇰🇪 Kenya',
    '255': '🇹🇿 Tanzania',
    '256': '🇺🇬 Uganda',
    '257': '🇧🇮 Burundi',
    '258': '🇲🇿 Mozambique',
    '260': '🇿🇲 Zambia',
    '261': '🇲🇬 Madagascar',
    '262': '🇷🇪 Réunion / Mayotte',
    '263': '🇿🇼 Zimbabwe',
    '264': '🇳🇦 Namibia',
    '265': '🇲🇼 Malawi',
    '266': '🇱🇸 Lesotho',
    '267': '🇧🇼 Botswana',
    '268': '🇸🇿 Eswatini',
    '269': '🇰🇲 Comoros',
    '290': '🇸🇭 Saint Helena / Tristan da Cunha',
    '291': '🇪🇷 Eritrea',
    '297': '🇦🇼 Aruba',
    '298': '🇫🇴 Faroe Islands',
    '299': '🇬🇱 Greenland',
    '350': '🇬🇮 Gibraltar',
    '351': '🇵🇹 Portugal',
    '352': '🇱🇺 Luxembourg',
    '353': '🇮🇪 Ireland',
    '354': '🇮🇸 Iceland',
    '355': '🇦🇱 Albania',
    '356': '🇲🇹 Malta',
    '357': '🇨🇾 Cyprus',
    '358': '🇫🇮 Finland / Åland Islands',
    '359': '🇧🇬 Bulgaria',
    '370': '🇱🇹 Lithuania',
    '371': '🇱🇻 Latvia',
    '372': '🇪🇪 Estonia',
    '373': '🇲🇩 Moldova',
    '374': '🇦🇲 Armenia',
    '375': '🇧🇾 Belarus',
    '376': '🇦🇩 Andorra',
    '377': '🇲🇨 Monaco',
    '378': '🇸🇲 San Marino',
    '379': '🇻🇦 Vatican City',
    '380': '🇺🇦 Ukraine',
    '381': '🇷🇸 Serbia',
    '382': '🇲🇪 Montenegro',
    '383': '🇽🇰 Kosovo',
    '385': '🇭🇷 Croatia',
    '386': '🇸🇮 Slovenia',
    '387': '🇧🇦 Bosnia & Herzegovina',
    '389': '🇲🇰 North Macedonia',
    '420': '🇨🇿 Czech Republic',
    '421': '🇸🇰 Slovakia',
    '423': '🇱🇮 Liechtenstein',
    '500': '🇫🇰 Falkland Islands',
    '501': '🇧🇿 Belize',
    '502': '🇬🇹 Guatemala',
    '503': '🇸🇻 El Salvador',
    '504': '🇭🇳 Honduras',
    '505': '🇳🇮 Nicaragua',
    '506': '🇨🇷 Costa Rica',
    '507': '🇵🇦 Panama',
    '508': '🇵🇲 Saint Pierre and Miquelon',
    '509': '🇭🇹 Haiti',
    '590': '🇬🇵 Guadeloupe / Saint Barthélemy / Saint Martin',
    '591': '🇧🇴 Bolivia',
    '592': '🇬🇾 Guyana',
    '593': '🇪🇨 Ecuador',
    '594': '🇬🇫 French Guiana',
    '595': '🇵🇾 Paraguay',
    '596': '🇲🇶 Martinique',
    '597': '🇸🇷 Suriname',
    '598': '🇺🇾 Uruguay',
    '599': '🇨🇼 Curaçao / Caribbean Netherlands',
    '670': '🇹🇱 Timor-Leste',
    '672': '🇦🇶 Norfolk Island / Australian Antarctica',
    '673': '🇧🇳 Brunei',
    '674': '🇳🇷 Nauru',
    '675': '🇵🇬 Papua New Guinea',
    '676': '🇹🇴 Tonga',
    '677': '🇸🇧 Solomon Islands',
    '678': '🇻🇺 Vanuatu',
    '679': '🇫🇯 Fiji',
    '680': '🇵🇼 Palau',
    '681': '🇼🇫 Wallis and Futuna',
    '682': '🇨🇰 Cook Islands',
    '683': '🇳🇺 Niue',
    '685': '🇼🇸 Samoa',
    '686': '🇰🇮 Kiribati',
    '687': '🇳🇨 New Caledonia',
    '688': '🇹🇻 Tuvalu',
    '689': '🇵🇫 French Polynesia',
    '690': '🇹🇰 Tokelau',
    '691': '🇫🇲 Micronesia',
    '692': '🇲🇭 Marshall Islands',
    '850': '🇰🇵 North Korea',
    '852': '🇭🇰 Hong Kong',
    '853': '🇲🇴 Macau',
    '855': '🇰🇭 Cambodia',
    '856': '🇱🇦 Laos',
    '870': '🇮🇳 Inmarsat (SNAC)',
    '880': '🇧🇩 Bangladesh',
    '886': '🇹🇼 Taiwan',
    '960': '🇲🇻 Maldives',
    '961': '🇱🇧 Lebanon',
    '962': '🇯🇴 Jordan',
    '963': '🇸🇾 Syria',
    '964': '🇮🇶 Iraq',
    '965': '🇰🇼 Kuwait',
    '966': '🇸🇦 Saudi Arabia',
    '967': '🇾🇪 Yemen',
    '968': '🇴🇲 Oman',
    '970': '🇵🇸 Palestine',
    '971': '🇦🇪 UAE',
    '972': '🇮🇱 Israel',
    '973': '🇧🇭 Bahrain',
    '974': '🇶🇦 Qatar',
    '975': '🇧🇹 Bhutan',
    '976': '🇲🇳 Mongolia',
    '977': '🇳🇵 Nepal',
    '992': '🇹🇯 Tajikistan',
    '993': '🇹🇲 Turkmenistan',
    '994': '🇦🇿 Azerbaijan',
    '995': '🇬🇪 Georgia',
    '996': '🇰🇬 Kyrgyzstan',
    '998': '🇺🇿 Uzbekistan'
}


def clean_number(number: str) -> str:
    return re.sub(r'\D', '', number)


def get_country_from_number(number: str) -> str:
    cleaned = clean_number(number)
    for code in sorted(COUNTRY_MAP.keys(), key=lambda x: -len(x)):
        if cleaned.startswith(code):
            return COUNTRY_MAP[code]
    return '🌍 Unknown'


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save_already_sent(already_sent):
    with open("already_sent.json", "w") as f:
        json.dump(list(already_sent), f)


def load_already_sent():
    if os.path.exists("already_sent.json"):
        with open("already_sent.json", "r") as f:
            return set(json.load(f))
    return set()


def login():
    try:
        logging.info("Attempting to login...")

        resp = session.get(LOGIN_PAGE_URL)
        logging.info(f"GET login page status: {resp.status_code}")

        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            logging.error("Captcha not found in login page.")
            return False

        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2
        logging.info(f"Solved captcha: {num1} + {num2} = {captcha_answer}")

        payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "capt": str(captcha_answer)
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_PAGE_URL,
            "Origin": BASE_URL.rstrip('/'),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        resp = session.post(LOGIN_POST_URL, data=payload, headers=headers, allow_redirects=False)
        logging.info(f"POST login status: {resp.status_code}")

        if resp.status_code == 302:
            redirect_location = resp.headers.get('Location', '')
            logging.info(f"Redirect location: {redirect_location}")

            if redirect_location == './':
                redirect_url = BASE_URL + "NumberPanel/"
            elif redirect_location.startswith('/'):
                redirect_url = BASE_URL.rstrip('/') + redirect_location
            else:
                redirect_url = BASE_URL + "NumberPanel/" + redirect_location

            logging.info(f"Following redirect to: {redirect_url}")
            resp = session.get(redirect_url, allow_redirects=True)
            logging.info(f"After redirect - Status: {resp.status_code}, URL: {resp.url}")

            if "/NumberPanel/login" in resp.url.lower():
                logging.error("Login failed - redirected back to login page ❌")
                return False

            if "client" in resp.url.lower() or "dashboard" in resp.text.lower() or "logout" in resp.text.lower():
                logging.info("Login successful ✅")

                try:
                    test_resp = session.get(BASE_URL + "NumberPanel/client/", timeout=5)
                    if test_resp.status_code == 200 and "/login" not in test_resp.url:
                        logging.info("Session verified - dashboard accessible")
                        return True
                except:
                    pass

                return True

        logging.error("Login failed - unexpected response ❌")
        return False

    except Exception as e:
        logging.error(f"Login error: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False


def build_api_url():
    start_date = "2025-04-25"
    end_date = "2026-01-01"
    return (
        f"{DATA_URL}?fdate1={start_date}%2000:00:00&fdate2={end_date}%2023:59:59&"
        "frange=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0&"
        "sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&"
        "mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&"
        "mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&"
        "mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&"
        "mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&"
        "mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&"
        "mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&"
        "mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&"
        "sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1")


def fetch_data():
    url = build_api_url()
    headers = {"X-Requested-With": "XMLHttpRequest"}

    try:
        response = session.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 or "login" in response.text.lower():
            logging.warning("Session expired. Re-logging...")
            if login():
                return fetch_data()
            return None
        logging.error(f"Unexpected status: {response.status_code}")
        return None
    except Exception as e:
        logging.error(f"Fetch error: {e}")
        return None


already_sent = load_already_sent()


def mask_number(number: str) -> str:
    cleaned = clean_number(number)
    for code in sorted(COUNTRY_MAP.keys(), key=lambda x: -len(x)):
        if cleaned.startswith(code):
            country_len = len(code)
            if len(cleaned) > country_len + 3:
                return f"{code}{cleaned[country_len:country_len+3]}°°°°{cleaned[-3:]}"
            else:
                return f"{code}{'°'*(len(cleaned)-country_len-3)}{cleaned[-3:]}"
    return f"{cleaned[:3]}{'°'*(len(cleaned)-6)}{cleaned[-3:]}"


async def send_messages():
    logging.info("🔍 Checking for messages...")
    data = fetch_data()

    if not data or 'aaData' not in data:
        logging.info("No data or invalid response.")
        return

    for row in data['aaData']:
        try:
            date = str(row[0]).strip()
            number = str(row[2]).strip()
            service = str(row[3]).strip()
            message = str(row[4]).strip()

            masked_number = mask_number(number)

            otp_match = re.search(r'(\d{3}-\d{3}|\d{4,6})', message)
            otp = otp_match.group(1) if otp_match else None

            if not otp:
                logging.info(f"No OTP found in: {message}")
                continue

            unique_key = f"{number}|{otp}"
            if unique_key in already_sent:
                continue

            already_sent.add(unique_key)
            save_already_sent(already_sent)

            country = get_country_from_number(number)

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔍 Number Channel", url="https://t.me/NUMBERCHANNELBD")],
                [InlineKeyboardButton("☎️ NUMBER BOT", url="https://t.me/OTPORA_BOT")]
            ])

            caption = (
                f"☣️<b>Pavel OTP</b>☣️\n\n"
                f"🕐 <b>Time:</b> {escape_html(date)}\n"
                f"🌐 <b>Country:</b> {escape_html(country)}\n"
                f"📱 <b>Service:</b> {escape_html(service)}\n"
                f"📞 <b>Number:</b> {escape_html(masked_number)}\n"
                f"🔑 <b>OTP Code:</b> <code>{escape_html(otp)}</code>\n\n"
                f"🔍 <b>Full Message:</b>\n\n"
                f"<pre>{escape_html(message)}</pre>\n\n"
                f"<b>Pavel OTP</b>\n"
                f"☣️<b>Developed by: ●—MR ATIK☣️</b>"
            )

            for chat_id in CHAT_IDS:
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=caption,
                        parse_mode="HTML",
                        disable_web_page_preview=True,
                        reply_markup=keyboard
                    )
                    logging.info(f"✓ Sent to {chat_id}")
                except TimedOut:
                    logging.error(f"⌛ Timeout sending to {chat_id}")
                except Exception as e:
                    logging.error(f"⚠️ Error sending to {chat_id}: {str(e)}")

            logging.info(f"[+] Sent OTP: {otp}")
            await asyncio.sleep(1)

        except Exception as e:
            logging.error(f"Error processing row: {str(e)}")


async def main():
    login_attempts = 0
    max_login_attempts = 3

    while login_attempts < max_login_attempts:
        if login():
            logging.info("✅ Bot is now running and monitoring for OTP messages...")
            break
        login_attempts += 1
        if login_attempts < max_login_attempts:
            logging.warning(f"Login attempt {login_attempts} failed. Retrying in 10 seconds...")
            await asyncio.sleep(10)
        else:
            logging.error("❌ All login attempts failed. Please check your credentials:")
            logging.error(f"   Username: {USERNAME}")
            logging.error(f"   Password: {'*' * len(PASSWORD)}")
            logging.error("\n📝 To fix this:")
            logging.error("   1. Set BOT_TOKEN in Replit Secrets")
            logging.error("   2. Set PANEL_USERNAME and PANEL_PASSWORD in Replit Secrets")
            logging.error("   3. Verify credentials work on http://51.89.99.105/NumberPanel/login")
            return

    while True:
        await send_messages()
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
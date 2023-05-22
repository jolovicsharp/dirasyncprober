import argparse
import asyncio
import aiohttp
import datetime
import pyfiglet


class DirAsyncProber:
    def __init__(self, args):
        self.args = args
        self.semaphore = asyncio.Semaphore(10)

    async def send_request(self, session, url):
        async with self.semaphore:  # Limit number of concurrent requests
            try:
                async with session.request(
                    method=self.args.method,
                    url=url,
                    headers=self.args.headers,
                    cookies=self.args.cookies,
                    allow_redirects=self.args.follow_redirect,
                    ssl=not self.args.no_tls_validation,
                    timeout=self.args.timeout,
                ) as response:
                    try:
                        body = await response.read()
                        content_length = len(body)
                        return response, content_length
                    except Exception as e:
                        print(f"Failed to read response body: {e}")
                        return response, 0
            except aiohttp.ClientError as e:
                print(f"Failed to send request: {e}")
                return None, 0

    async def process_word(self, session, word):
        url = f"{self.args.url}/{word}"
        if self.args.add_slash:
            url += "/"

        response, content_length = await self.send_request(session, url)

        if response is not None:
            if self.args.status_code and response.status != self.args.status_code:
                return  # Skip if status code doesn't match

            if not self.args.no_status:
                print(f"{response.status} - {url}")

            if self.args.expanded:
                print(response.url)

            print(f"Content-Length: {content_length}")

            if self.args.extensions:
                for ext in self.args.extensions.split(","):
                    ext = ext.strip()
                    if response.headers.get("Content-Type", "").endswith(ext):
                        print(f"Found: {url}")

    async def start(self):
        ascii_banner = pyfiglet.figlet_format("DirAsyncProber")
        print(ascii_banner)

        print("===============================================================")
        print("DirAsyncProber v1.0.0")
        print("The Async Directory Prober")
        print("===============================================================")

        start_time = datetime.datetime.now()
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        connector = aiohttp.TCPConnector(ssl=not self.args.no_tls_validation)
        async with aiohttp.ClientSession(connector=connector) as session:
            with open(self.args.wordlist, "r") as wordlist_file:
                tasks = []
                for word in wordlist_file:
                    word = word.strip()
                    tasks.append(self.process_word(session, word))

                await asyncio.gather(*tasks)

        end_time = datetime.datetime.now()
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        print("===============================================================")
        print(f"DirAsyncProber started at: {start_time}")
        print(f"DirAsyncProber finished at: {end_time}")
        print("Directory enumeration completed.")
        print("===============================================================")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Kickstart your directory busting adventure with DirAsyncProber!"
    )
    parser.add_argument(
        "-u", "--url", required=True, help="The target URL that needs a good busting"
    )
    parser.add_argument(
        "-sc",
        "--status-code",
        type=int,
        help="Search for a specific status code",
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        required=True,
        help="The wordlist: your directory busting weapon",
    )
    parser.add_argument(
        "-x",
        "--extensions",
        help="File extensions to hunt for. It's like fishing, but for files.",
    )
    parser.add_argument(
        "-e",
        "--expanded",
        action="store_true",
        help="Expanded mode, prints full URLs for maximum detail",
    )
    parser.add_argument(
        "-f",
        "--add-slash",
        action="store_true",
        help="Adds a / to each request because sometimes it's just necessary",
    )
    parser.add_argument(
        "-r",
        "--follow-redirect",
        action="store_true",
        help="Follows redirects because we don't like dead ends",
    )
    parser.add_argument(
        "-k",
        "--no-tls-validation",
        action="store_true",
        help="Skip TLS certificate verification for those times when you just can't be bothered",
    )
    parser.add_argument(
        "-H",
        "--headers",
        nargs="*",
        help="Specify HTTP headers to tweak your busting spree",
    )
    parser.add_argument(
        "-m",
        "--method",
        default="GET",
        help='Use the following HTTP method (default "GET")',
    )
    parser.add_argument(
        "--timeout", default=10, type=float, help="HTTP Timeout to keep things snappy"
    )
    parser.add_argument(
        "-n",
        "--no-status",
        action="store_true",
        help="Don't print status codes, because who needs those anyway?",
    )
    parser.add_argument("-c", "--cookies", help="Cookies to sweeten your requests")
    parser.add_argument(
        "-a",
        "--useragent",
        default="pybuster/1.0.0",
        help="Set the User-Agent string to strut your stuff",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    dir_async_prober = DirAsyncProber(args)
    asyncio.run(dir_async_prober.start())


if __name__ == "__main__":
    main()

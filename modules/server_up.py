# Trying to make a route that updates the server when a push is made to GitHub
# @app.route('/update_server', methods=['POST'])
#     def webhook():
#         if request.method == 'POST':
#             repo = git.Repo('path/to/git_repo')
#             origin = repo.remotes.origin
# origin.pull()
# return 'Updated PythonAnywhere successfully', 200
#         else:
#             return 'Wrong event type', 400

# load_dotenv()  # This loads the .env file

# # Access your variable
# # GITHUB_SECRET = os.getenv("GITHUB_SECRET")
# GITHUB_WEBHOOK_ROUTE = "/server_update"
# GITHUB_SECRET = bytes(os.getenv("GITHUB_SECRET"), "utf-8")


# @app.route(GITHUB_WEBHOOK_ROUTE, methods=["POST"])
# def github_webhook():
#     # Verify the request signature
#     signature = request.headers.get("X-Hub-Signature")
#     if signature is None:
#         abort(403)

#     sha_name, signature = signature.split("=")
#     if sha_name != "sha1":
#         abort(501)

#     mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha1)
#     if not hmac.compare_digest(mac.hexdigest(), signature):
#         abort(403)

#     # If the signature is valid, pull the latest changes
#     subprocess.call(["git", "pull"])
#     if request.method == "POST":
#         repo = Repo("https://github.com/ChefAharoni/HaaretzMusafim")
#         origin = repo.remotes.origin
#         origin.pull()
#         # Restart the server (this is a placeholder, replace with your server's restart command)
#         os.system("restart server_command")
#         return "Updated and restarted PythonAnywhere successfully", 200
#     # Add any other commands you need to run after pulling changes, such as restarting your server
#     # subprocess.call(['touch', '/var/www/html/myapp.wsgi'])

#     return "Updated PythonAnywhere successfully", 200

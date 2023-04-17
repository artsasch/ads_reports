
app_id = '51617154'
access_rights = 'groups'
get_user_token_url = `https://oauth.vk.com/authorize?client_id=${app_id}&scope=${access_rights}&response_type=token&v=5.131`

window.open(get_user_token_url)
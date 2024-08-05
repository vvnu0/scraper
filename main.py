from insta import get_instagram_profile_info
from linkedin import runSearch

username = "zombie_something"
profile_info = get_instagram_profile_info(username)
print(profile_info)


query = f'"{profile_info["name"]}" "Cornell University" site:linkedin.com/in'
res, links = runSearch(query)

#print(res)
#print(f"Couldn't check the rest, is it one of these? {links}")
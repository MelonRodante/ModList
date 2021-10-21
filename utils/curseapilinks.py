header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
endpoint = 'https://addons-ecs.forgesvc.net/api/v2'

minecraft_versions = endpoint + '/minecraft/version'

pagesize = 50
search_base_query = \
    endpoint + \
    '/addon/search' + \
    '?gameId=432' + \
    '&sectionId=6' + \
    '&sort=2' + \
    '&pageSize=' + str(pagesize)
search_filter_version = '&gameVersion='
search_offset = index = '&index='


'''
https://addons-ecs.forgesvc.net/api/v2/addon/search
?gameId=432
&sectionId=6
&categoryId=0
&sort=2
&gameVersion=1.17
&pageSize=50
&index=0
&searchFilter={searchFilter}
'''
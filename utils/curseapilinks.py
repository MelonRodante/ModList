
class CurseAPI:

    key = '$2a$10$ku3.ncligCgUckN7vKnKyOeqH9y9H/aDca3t.QjPEG./wPaOU7UPu'
    header = {'x-api-key': key, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    gameId = '432'      # Minecraft
    classId = '6'       # Mods

    pageSize = '20'
    sortField = '3'
    sortOrder = 'desc'

    endpoint = 'https://api.curseforge.com/v1'

    minecraft_versions = 'https://www.modpackindex.com/api/v1/minecraft/versions'  # 'https://addons-ecs.forgesvc.net/api/v2/minecraft/version'       # endpoint + '/minecraft/version'
    minecraft_modid = endpoint + '/mods/'

    search_base_query = endpoint + '/mods/search' + '?gameId=' + gameId + '&classId=' + classId + '&sortField=' + sortField + '&sortOrder=' + sortOrder + '&pageSize=' + pageSize

    search_filter_version = '&gameVersion='
    search_offset = index = '&index='


'''
class CurseAPI:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    gameId = '432'
    classId = '6'

    sortField = '2'
    pageSize = 50

    endpoint = 'https://addons-ecs.forgesvc.net/api/v2'

    minecraft_versions = endpoint + '/minecraft/version'
    minecraft_modid = endpoint + '/addon/'

    search_base_query = endpoint + '/addon/search' + '?gameId=' + gameId + '&sectionId=' + classId + '&sort=' + sortField + '&pageSize=' + str(pageSize)
    search_filter_version = '&gameVersion='
    search_offset = index = '&index='
'''

'''
gameId	            query	    integer(int32)	    false	    Filter by game id
classId	            query	    integer(int32)	    false	    Filter by section id (discoverable via Game object)
categoryId	        query	    integer(int32)	    false	    Filter by category id
gameVersion	        query	    string	            false	    Filter by game version string
searchFilter	    query	    string	            false	    Filter by free text search in the mod name and author
sortField	        query	    any	                false	    Filter by ModsSearchSortField enumeration
sortOrder	        query	    any	                false	    'asc' if sort is in ascending order, 'desc' if sort is in descending order
modLoaderType	    query	    any	                false	    Optional - Filter only addons associated to a given modloader (Forge, Fabric ...)
gameVersionTypeId	query	    integer(int32)	    false	    Filter only mods that contain files tagged with versions of the given gameVersionTypeId
index	            query	    integer(int32)	    false	    A zero based index of the first item to include in the response
pageSize	        query	    integer(int32)	    false	    The number of items to include in the response

1=Featured
2=Popularity
3=LastUpdated
4=Name
5=Author
6=TotalDownloads
7=Category
8=GameVersion

0 = Any
1 = Forge
2 = Cauldron
3 = LiteLoader
4 = Fabric
'''
# The script searches for all users with the specified filters in AD. 

## Configuration file
`server` - DNS name or IP address of the domain controller server. 
`user` - user with read access to the AD configuration. 
`password` - the user's password. 
`search_base` - domain name. 
`search_filter` - specify the group in which you want to find users, for example, Domain Administrators. 
`attributes` - specify the criterion by which you search in the group, for example, member.
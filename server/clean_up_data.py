# A really simple script to filter the WhatsApp data so you can use it
# with textgenrnn
#
# Onput = WhatsApp export file with this format:
# [03/02/2016, 10:47:53] example-username: Hallo.
#
# Output =  Messages without timestampt, only sent by the following user:
username = 'example-username'
# You can set your username under WhatsApp > Settings > Edit Profile
# Set this to something unique so it's easier to filter

filtered = ''

with open("input.txt", "r") as input:
    array = []
    i = 0
    for line in input:
        line = line.strip()

        if username in line and 'omitted' not in line:
            message = line.split(username+': ',1)[1]
            filtered += message + '\n'

output = open("output.txt", "w")
output.write(filtered)
output.close()

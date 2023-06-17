from txt_to_list import to_list_single as ttl

f = open('My Spotify Playlist.txt', 'r')
g = open('lil wayne songs.txt', 'w')

songs = ttl(f)
count = 0
for song in songs:
    songBuff = str(song.lower())
    if songBuff[0]=='l' and songBuff[1]=='i' and songBuff[2]=='l' and songBuff[3]==' ' and songBuff[4]=='w':
        g.write(songBuff)
        g.write('\n')
        count+=1
    else:
        pass
print(count)
f.close()
g.close()

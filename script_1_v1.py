
import numpy as np
import matplotlib.pyplot as plt


file_in = open("listen-20131115.log","r")
line = file_in.readline()

listen = []
suspect_art_prov_pairs = np.empty((0,2),int)
line_counter = 0
while line and line_counter < 6000:
    row = [0]*6
    number = ''
    count = 0
    for char in line:
        if char != ',':
            number = number + char
        elif char == ',':
                number = int(number)
                row[count]= number
                number = ''
                count +=1
        row[count] = number[:-2] # this one is for the ip_address. -2 for the /r and /n at the end of the line.

    timestamp = row[0]
    sng_id = row[1]
    user_id = row[2]
    artist_id = row[3]
    provider_id = row[4]
    ip = row[5]

    add_row = True
    for search in range(len(listen)):
        # test to check that an IP address is not listening to several song at the same time.
        if listen[search][5]==ip and listen[search][0]==timestamp and listen[search][1]!=sng_id:
            print(row)
            # suspect_art_prov_pairs = np.append([artist_id, provider_id], axis=0)
            suspect_art_prov_pairs = np.vstack([suspect_art_prov_pairs,[artist_id, provider_id]])
            add_row = False
            break
        # test to check that an IP address is no tbeing used by different users at the same timestamp
        elif listen[search][5]==ip and listen[search][0]==timestamp and listen[search][2]!=user_id:
            print(row)
            # suspect_art_prov_pairs = np.append([artist_id, provider_id], axis=0)
            suspect_art_prov_pairs = np.vstack([suspect_art_prov_pairs,[artist_id, provider_id]])
            # suspect_art_prov_pairs.append([artist_id, provider_id])
            add_row = False
            break
    if add_row:
        listen.append(row)

    ## test to check wether sng_ids always point to the same artist-provider pair.
    # for search in range(len(listen)):
    #     if listen[search][1]==sng_id and(listen[search][3]!=artist_id or listen[search][4]!=provider_id):
    #         print(row)
    #         row = None
    #         break
    ## result of the test: the pair is always correct
    line = file_in.readline()
    line_counter += 1

# let's make an histogram of the suspects to see if some come back very often
artists = plt.figure('Suspected Artists')
plt.hist(suspect_art_prov_pairs[:,0], bins=150)
# ax.annotate(str(count), xy=(x, 0))

providers = plt.figure('Suspected Providers')
plt.hist(suspect_art_prov_pairs[:,1], bins=150)
# ax.annotate(str(count), xy=(x, 0))
# fig = plt.gcf()
plt.show()

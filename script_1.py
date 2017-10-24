
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, current_process, cpu_count
import pickle
import logging

# Initializing the logging
logging.basicConfig(filename="correcting_listening_sessions.log",format='[%(asctime)s.%(msecs)03d] - [%(levelname)s] - [%(name)s:%(lineno)s - %(funcName)s()] - %(message)s', level='DEBUG', datefmt="%d/%m/%y %H:%M:%S")
logger = logging.getLogger()

# importing and extracting the data from the log file.
# creating the pool of lines
lines = []
lines = open("listen-20131115.log", 'r').read().rsplit('\n')
lines = [l for l in lines if l]
logger.info("Number of lines found: "+ str(len(lines)))
# initializin multiprocessing pool
pool_size = cpu_count() * 2
pool = Pool(pool_size)
# creating the rows
from create_listen_array import create_line
try:
    all_lines = pool.map(create_line, lines)
    pool.close() # the tasks are finished
    pool.join() # wrapping current tasks
    # now let's flatten the array
    listen_array = np.empty((0,6))
    for l in all_lines:
        if l:
            listen_array = np.vstack([listen_array, l])
    try:
        pickle.dump(listen_array)
    except:
        logger.warn("unable to dump the listening data array.")
    logger.info("The array with the listening data has been created.")
except Exception as e:
    logger.error("Did not manage to create the array for the listening data. \n",str(e))



# analyzing the data to output authentic listening sessions.
listen_corrected = np.empty((0,6))
suspects = np.empty((0,6))
suspect_art_prov_pairs = np.empty((0,2),int)
# initializin multiprocessing pool
pool_size = cpu_count() * 2
pool = Pool(pool_size)
# analyzing the lines
from analysis import check_line
try:
    pool.map(check_line, listen_array)
    pool.close()
    pool.join()
except Exception as e:
    logger.error("Unable to analyze the lines, error was: \n" + str(e))

    # timestamp = row[0]
    # sng_id = row[1]
    # user_id = row[2]
    # artist_id = row[3]
    # provider_id = row[4]
    # ip = row[5]

#     add_row = True
#     for search in range(len(listening_list)):
#         # test to check that an IP address is not listening to several song at the same time.
#         if listening_list[search][5]==ip and listening_list[search][0]==timestamp and listening_list[search][1]!=sng_id:
#             print(row)
#             # suspect_art_prov_pairs = np.append([artist_id, provider_id], axis=0)
#             suspect_art_prov_pairs = np.vstack([suspect_art_prov_pairs,[artist_id, provider_id]])
#             add_row = False
#             break
#         # test to check that an IP address is no tbeing used by different users at the same timestamp
#         elif listening_list[search][5]==ip and listening_list[search][0]==timestamp and listening_list[search][2]!=user_id:
#             print(row)
#             # suspect_art_prov_pairs = np.append([artist_id, provider_id], axis=0)
#             suspect_art_prov_pairs = np.vstack([suspect_art_prov_pairs,[artist_id, provider_id]])
#             # suspect_art_prov_pairs.append([artist_id, provider_id])
#             add_row = False
#             break
#     if add_row:
#         listening_list.append(row)
#
#     ## test to check wether sng_ids always point to the same artist-provider pair.
#     # for search in range(len(listening_list)):
#     #     if listening_list[search][1]==sng_id and(listening_list[search][3]!=artist_id or listening_list[search][4]!=provider_id):
#     #         print(row)
#     #         row = None
#     #         break
#     ## result of the test: the pair is always correct
#     line = file_in.readline()
#     line_counter += 1
#
# # let's make an histogram of the suspects to see if some come back very often
# artists = plt.figure('Suspected Artists')
# plt.hist(suspect_art_prov_pairs[:,0], bins=150)
# # ax.annotate(str(count), xy=(x, 0))
#
# providers = plt.figure('Suspected Providers')
# plt.hist(suspect_art_prov_pairs[:,1], bins=150)
# # ax.annotate(str(count), xy=(x, 0))
# # fig = plt.gcf()
# plt.show()

import filecmp
import os
import time



def checker():
    if not filecmp.cmp("files/past_details.txt","files/current_details.txt"):
        cur = open("files/current_details.txt")
        cur_arr = cur.readlines()
        cur.close()

        old = open("files/past_details.txt")
        old_arr = old.readlines()
        old.close()

        # find the elements that are extra in the current file and write them to a new file
        new_open = open("files/open_classes.txt", "a")
        for i in range(len(cur_arr)):
            if cur_arr[i] not in old_arr:
                new_open.write(cur_arr[i])
        new_open.close()
        
        # find the elements that are missing in the current file and write them to a new file
        new_closed = open("files/closed_classes.txt", "a")
        for i in range(len(old_arr)):
            if old_arr[i] not in cur_arr:
                new_closed.write(old_arr[i])
        new_closed.close()

        # write the current file to the past file
        os.remove("files/past_details.txt")
        os.system('cp files/current_details.txt files/past_details.txt')

# while True:
checker()
    # time.sleep(30)

import filecmp
import os

def checker():
    if not filecmp.cmp("files/past_details.txt","files/current_details.txt"):
        cur = open("files/current_details.txt","r")
        cur_arr = cur.readlines()
        cur.close()

        old = open("files/past_details.txt","r")
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
        file = open("files/past_details.txt","w")
        file.truncate(0)
        file.close()
        os.system('cp files/current_details.txt files/past_details.txt')
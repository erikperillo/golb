#!/usr/bin/env python3

import subprocess as sp
import os

DEF_CATEGORY = "Random"
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
GLOBALS_FILE = os.path.join(FILE_DIR, "blog/globals.py")
MANAGE_SCRIPT = os.path.join(FILE_DIR, "manage.py")

def bool_input(text, trues=["y", "yes", "1"]):
    ans = input(text)
    return ans.lower() in trues

def main():
    print("Welcome to bolg quick setup.\n"
        "WARNING: this script will flush everything you may have in database.")

    if not bool_input("Proceed? (y/n) "):
        print("Aborting.")
        exit(1)

    print("\nflushing database...")
    sp.run(["python", MANAGE_SCRIPT, "flush"])
    print("done.\n")

    print("Enter superuser information.")
    sp.run(["python", MANAGE_SCRIPT, "createsuperuser"])
    print("done.\n")

    title = input("Enter blog title: ")
    with open(GLOBALS_FILE, "w") as f:
        f.write("blog_title = '%s'" % title)
    print("title '%s' saved to '%s'." % (title, GLOBALS_FILE),
        "You can change it later.\n")

    init_cat = input("Create initial posts category (empty for default '%s') " %\
        DEF_CATEGORY)
    if not init_cat:
        init_cat = DEF_CATEGORY
    with open(GLOBALS_FILE, "a") as f:
        f.write("\ninitial_category = '%s'" % init_cat)
    print("Initial category '%s' saved in '%s'.\n" % (init_cat, GLOBALS_FILE))

    print("Initial setup done!\n"
        "You can change things later in <blog_path>/admin.")

if __name__ == "__main__":
    main()

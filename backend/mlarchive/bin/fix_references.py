#!../../../env/bin/python
"""
Script to locate and fix a specific thread of messages that have bracketed text
in their references header which is causing failure of the threading function 
"""
# Standalone broilerplate -------------------------------------------------------------
from django_setup import do_setup
do_setup()
# -------------------------------------------------------------------------------------
from builtins import input

import argparse
import email
import re
import os
import shutil

from django.conf import settings
from mlarchive.archive.models import Message
from mlarchive.archive.mail import flatten_message

BACKUP_DIR = os.path.join(settings.DATA_ROOT,'backup')

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_references(message):
    """Returns list of entries from References header"""
    reference_re = re.compile(r'(<.*?>)')
    refs = ''.join(message.references.split())      # remove whitespace
    return reference_re.findall(refs)


def main():
    parser = argparse.ArgumentParser(description='Fix references')
    parser.add_argument('-c', '--check', help="check only", action='store_true')
    args = parser.parse_args()
    total = 0
    
    qs = Message.objects.filter(email_list__name='ntp',subject__contains='Proposed REFID changes').order_by('date')
    
    bad_refs = [
        '<Message>',
        '<from>',
        '<"Ulrich>',
        '<Windl">',
        '<Ulrich.Windl@rz.uni-regensburg.de>',
        '<of>',
        '<"Wed,>',
        '<22>',
        '<Jul>',
        '<2015>',
        '<08:20:07>',
        '<+0200.">',
        '<"Mon>',
        '<"Mon,>',
        '<20>',
        '<13:57:02>']

    for message in qs:
        if bad_refs[0] in message.references:
            total = total + 1
            new_refs = []
            old_references = message.references
            for ref in get_references(message):
                if ref in bad_refs:
                    pass
                else:
                    new_refs.append(ref)
            new_references = ' '.join(new_refs)
            print(message.msgid)
            print(old_references)
            print('-----------------')
            print(new_references)
            print('=================')
            eval(input('Press enter to continue'))

            if not args.check:
                print('saving...')
                # update db
                message.references = new_references
                message.save()

                # update message file
                file = message.get_file_path()
                with open(file) as fp:
                    msg = email.message_from_file(fp)
        
                # adjust headers
                msg.add_header('X-References',old_references)
                msg.replace_header('references',new_references)
            
                # save original file
                list_dir = os.path.basename(os.path.dirname(file))
                backup_dir = os.path.join(BACKUP_DIR,list_dir)
                ensure_dir(backup_dir)
                shutil.move(file,backup_dir)
                
                # write new file
                output = flatten_message(msg)
                with open(file,'w') as out:
                    out.write(output)
                os.chmod(file,0o660)
                
    # print stats
    print("Modified messages: {}".format(total))


if __name__ == "__main__":
    main()

import subprocess

import jsons

paydtls = {'action_type': 'pay', "card_number": 65
    , "month": 654, 'year': 54, 'holder': ",mn"
    , 'ccv': +95, 'id': "id"}
proc = subprocess.Popen("python post.py "+jsons.dumps(paydtls), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        shell=True)

proc.communicate()[0]
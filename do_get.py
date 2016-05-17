
import sys
import requests
import simplejson as json


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: python do_get.py <Token> <URL>\n"
        sys.exit(-1)

    # format our auth token for use in the headers
    headers = {'X-Auth-Token': sys.argv[1]}

    res = requests.get(sys.argv[2], headers=headers, verify=False)

    # check for success
    if res.status_code != requests.codes.ok:
        res.raise_for_status()

    # parse the response into JSON
    j = json.loads(res.content)

    #print it nice
    print json.dumps(j, indent=4)

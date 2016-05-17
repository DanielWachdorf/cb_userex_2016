import sys
import requests
import simplejson as json


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "Usage: python do_get.py <Token> <URL> <PostJsonFile>\n"
        sys.exit(-1)

    # format our auth token for use in the headers
    headers = {'X-Auth-Token': sys.argv[1]}

    # read in post JSON data
    data = open(sys.argv[3], 'r').read()

    print "Posting:"
    print "---------"
    print data
    print "---------"

    res = requests.post(sys.argv[2], data=data, headers=headers, verify=False)

    # check for success
    if res.status_code != requests.codes.ok:
        res.raise_for_status()

    # parse the response into JSON
    j = json.loads(res.content)

    #print it nice
    print "Got Reply:"
    print "---------"
    print json.dumps(j, indent=4)
    print "---------"

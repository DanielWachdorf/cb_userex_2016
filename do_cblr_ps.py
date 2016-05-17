import sys
import time
import requests
import simplejson as json


# Require SSL validation
# Set to True if your Cb server uses a real SSL cert
B_VERIFY=False

def establish_session(url, headers, sensor_id):
    '''
    Establish a session.
    Then wait for it to go active.
    Returns the session id of the session

    Note: This has one major shortcoming - it doesn't check
    if a CbLR session is already established for a given sensor
    id
    '''

    print "Starting session for sensor %d" % sensor_id

    postdata = '{"sensor_id" : %s}' % sensor_id
    u = url + '/api/v1/cblr/session'
    res = requests.post(u, data=postdata, headers=headers, verify=B_VERIFY)
    # check for success
    if res.status_code != requests.codes.ok:
        res.raise_for_status()

    # turn the response into JSON
    j = json.loads(res.content)
    while j['status'] != 'active':

        time.sleep(2)

        u = url + '/api/v1/cblr/session/%d' % j['id']
        res = requests.get(u, headers=headers, verify=B_VERIFY)
        # check for success
        if res.status_code != requests.codes.ok:
            res.raise_for_status()

        j = json.loads(res.content)

    print "Established session id %d" % j['id']
    return j['id']

def run_ps(url, headers, session_id):
    '''

    Given a session_id (from an established connection) run the ps command
    '''

    u = url + '/api/v1/cblr/session/%d/command'

    # format the command object
    cmd = {}
    cmd['name'] = 'process list'
    cmd['object'] = ''

    # convert it to JSON
    data = json.dumps(cmd)

    u = url + '/api/v1/cblr/session/%d/command' % (session_id)

    print "Posting command"

    # post the command to the server
    res = requests.post(u, data=data, headers=headers, verify=B_VERIFY)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()

    # parse the command
    j = json.loads(res.content)
    cmd_id = j['id']

    print "Waiting for command id %d to complete" % cmd_id

    u = url + '/api/v1/cblr/session/%d/command/%d' % (session_id, cmd_id)
    res = requests.get(u, params={'wait': 'true'}, headers=headers, verify=B_VERIFY)
    # check for success
    if res.status_code != requests.codes.ok:
        res.raise_for_status()

    j = json.loads(res.content)
    return j


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "Usage: python do_get.py <Token> <URL> <SensorId>\n"
        sys.exit(-1)

    # format our auth token for use in the headers
    headers = {'X-Auth-Token': sys.argv[1]}

    sess_id = establish_session(sys.argv[2], headers, 5)

    cmd_data = run_ps(sys.argv[2], headers, sess_id)

    print json.dumps(cmd_data, indent=4)




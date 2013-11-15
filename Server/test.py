__author__ = 'Alex Qu'
import GateKeeper


class test:
    my_gatekeeper = GateKeeper
    my_gatekeeper.run('kevin chen')

    """    with open('userinfo.pickle', 'rb') as handle:
        reader = pickle.load(handle)
        tmp = reader.has_key(login)
        tmpPass = reader[login]
        handle.close()
        if tmp and tmpPass == passwd:
            print "Logged in"
            return True
        else:
            print "Login failed"
            return False
            """
from utils.ws_utils import WSUtils
import sys

if __name__ == "__main__":
    wsu = WSUtils()
    com = sys.argv[1]
    if com == "list_public":
        wsl = wsu.list_workspaces(public=True)
        for wsid in wsl:
            print(wsid)
    elif com == "list_objects":
        filt = None
        wsid = sys.argv[2]
        upa = False
        lform = '%d\t%s\t%s\t%s\t%d\t%s'
        for arg in sys.argv[3:]:
            if arg == "--upa":
                upa = True
            else:
                filt = arg
        objs = wsu.list_objects(wsid, filter=filt)
        for obj in objs:
            if upa:
                print('%d/%d/%d' % (int(wsid), obj[0], obj[4]))
            else:
                print(lform % (obj[0], obj[1], obj[2],
                               obj[3], obj[4], obj[5]))

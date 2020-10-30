# coding:utf-8

class PrintMain:
    def ReturnPrint(self, layer):

        ip = None
        for iprint in range(len(layer)):
            # print(iprint)
            # print(layer[iprint])
            ip = layer[iprint]

            print("")
            print("レイヤー" + str(iprint))
            # print(ip.DrawSetImg)
            print(ip.Document)
            print(ip.Point)
            print("")

        return ip

    def GetPoint(self, layer, iprint):
        ip = layer[iprint]
        return ip.Point

    #

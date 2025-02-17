import objs

class Stage:
    def getObjs(self):
        return []

class DefaultStage(Stage):
    def getObjs(self):
        return [
            objs.Cube(x, y, z) for x, y, z in [(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (-4, 0, 0)]
        ]

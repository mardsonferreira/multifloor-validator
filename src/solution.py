class Solution:
    def __init__(self, file):
        f = open(file, 'r')
        
        self.num_depts = int(f.readline())

        self.layout = {}
        self.widths = {}
        self.heights = {}
        self.centroides = {}

        _layout = list(map(float, f.readline().split(',')))
        for i in range(self.num_depts):
            self.layout[i] = _layout[i]
        
        _widths = list(map(float, f.readline().split(',')))
        for i in range(self.num_depts):
            self.widths[i] = _widths[i]
        
        _heights = list(map(float, f.readline().split(',')))
        for i in range(self.num_depts):
            self.heights[i] = _heights[i]

        _centroides = []
        for i in range(self.num_depts):
            _centroides.append(tuple(map(float, f.readline().split(','))))
        
        for i in range(self.num_depts):
            self.centroides[i] = _centroides[i]

        f.close()

        self.show()

    def show(self):
        print("###### SOLUTION ######")

        print("###")
        print("# LAYOUT")
        print("###")
        for k, v in self.layout.items():
            print("{0}:{1}".format(k + 1,v))

        print("###")
        print("# CENTRTOIDS")
        print("###")
        for k, v in self.centroides.items():
            print("{0}:{1}".format(k + 1,v))

        print("###")
        print("# WIDTHS")
        print("###")
        for k, v in self.widths.items():
            print("{0}:{1}".format(k + 1,v))
        
        print("###")
        print("# HEIGHTS")
        print("###")
        for k, v in self.heights.items():
            print("{0}:{1}".format(k + 1,v))

        print("###")
        print("# AREAS")
        print("###")
        for i in range(self.num_depts):
            print("{0}:{1}".format(i + 1, self.widths[i] * self.heights[i]))
        
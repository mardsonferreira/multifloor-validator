class Instance:
    def __init__(self, file):
        f = open(file, 'r')
        
        self.num_depts = int(f.readline())
        self.num_floors = int(f.readline())
        self.num_lifts = int(f.readline())
        self.max_width = int(f.readline())
        self.max_height = int(f.readline())
        self.delta = int(f.readline())

        self.aspect_ratios = list(map(float, f.readline().split(',')))

        self.areas = list(map(int, f.readline().split(',')))
        
        self.vertical_costs = []
        for i in range(self.num_depts):
            self.vertical_costs.append(list(map(float, f.readline().split(','))))
        
        self.horizontal_costs = []
        for i in range(self.num_depts):
            self.horizontal_costs.append(list(map(float, f.readline().split(','))))
        
        self.flows = []
        remain_lines = f.readlines()
        for line in remain_lines:
            self.flows.append(list(map(float, line.split(','))))
        
        f.close()
        
        self.show()

    def show(self):
        print("##### INSTANCE ######")
        print('Number of departments: %s' % self.num_depts)
        print('Number of floors: %s' % self.num_floors)
        print('Number of lifts: %s' % self.num_lifts)
        print('Maximum width: %s' % self.max_width)
        print('Maximun height: %s' % self.max_height)
        print('Delta: %s' % self.delta)
        print('Aspect ratios: %s' % self.aspect_ratios)  
        print('Areas: %s' % self.areas)  
        
        print('Vertical Costs Matrix:')
        for cost in self.vertical_costs:
            print(cost)
        
        print('Horizontal Costs Matrix:')
        for cost in self.horizontal_costs:
            print(cost)
        
        print('Flows Matrix:')
        for flow in self.flows:
            print(flow)   

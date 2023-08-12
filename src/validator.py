import numpy as np
import math
from itertools import combinations

epsilon = 1e-05

def is_areas_valid(expected, result):
    invalid_areas = []

    if len(expected) != len(result):
        return False, invalid_areas
    
    clean = True
    for i in range (len(expected)):
        if not math.isclose(expected[i], result[i], abs_tol=epsilon, rel_tol=epsilon):
            invalid_areas.append(i)
            clean = False
    
    return clean, invalid_areas

def is_aspect_ratio_valid(w, h, beta):
    _beta = max([w/h, h/w])

    return round(_beta, 2) - beta <= epsilon

def overlap(coordinate_a, coordinate_b, value_a, value_b):
    aux_1 = round(abs(coordinate_a - coordinate_b), 2)
    aux_2 = round(1/2.0*(value_a + value_b), 2)

    if aux_1 < aux_2 :
        return True
    
    return False

def fit(coordinate, value, max_value):
    if ((coordinate + 0.5*value) - 0.5*max_value > epsilon) or ((coordinate - 0.5*value) + 0.5*max_value < -epsilon):
        return False
    
    return True

class Validator:
    def __init__(self, instance, solution):
        self.instance = instance
        self.layout = solution.layout
        self.centroides = solution.centroides
        self.result_widths = solution.widths
        self.result_heights = solution.heights

        self.vertical_dist = np.zeros((self.instance.num_depts, self.instance.num_depts))
        self.horizontal_dist = np.zeros((self.instance.num_depts, self.instance.num_depts))

    def compute_vertical_cost(self):
        n = self.instance.num_depts

        for i in range(n):
            for j in range(n):
                self.vertical_dist[i][j] = self.instance.delta * abs(self.layout[i] - self.layout[j])
        
        vertical_cost = 0
        for i in range(n):
            for j in range(n):
                vertical_cost += self.instance.vertical_costs[i][j] * self.instance.flows[i][j] * self.vertical_dist[i][j]
        
        return vertical_cost
    
    def compute_horizontal_cost(self):
        n = self.instance.num_depts

        elevetor_coordenates = (7.5, 2.5)

        for i in range(n):
            for j in range(n):
                # if depts are in the same floor
                if self.layout[i] == self.layout[j]:
                    # d_ij = |x_i - x_j| + |y_i - y_j|
                    self.horizontal_dist[i][j] = abs(self.centroides[i][0] - self.centroides[j][0]) + abs(self.centroides[i][1] - self.centroides[j][1])
                else:
                     # d_ie = |x_i - x_e| + |y_i - y_e|
                    d_ie = abs(self.centroides[i][0] - elevetor_coordenates[0]) + abs(self.centroides[i][1] - elevetor_coordenates[1])
                    
                     # d_je = |x_j - x_e| + |y_j - y_e|
                    d_je = abs(self.centroides[j][0] - elevetor_coordenates[0]) + abs(self.centroides[j][1] - elevetor_coordenates[1])

                    self.horizontal_dist[i][j] = d_ie + d_je + self.vertical_dist[i][j]
        
        horizontal_cost = 0
        for i in range(n):
            for j in range(n):
                horizontal_cost += self.instance.horizontal_costs[i][j] * self.instance.flows[i][j] * self.horizontal_dist[i][j]
        

        return horizontal_cost
    
    def validate_area_constraints(self):
        result_areas = [self.result_widths[i] * self.result_heights[i] for i in range(self.instance.num_depts)]

        clean, invalid_areas = is_areas_valid(self.instance.areas, result_areas)

        if not clean:
            print("### AREA ERROR FOUND!")
            for i in invalid_areas:
                print("Area of department {} => {} != {}.".format(i+1, result_areas[i], self.instance.areas[i]))
        
        area_by_floor = {}
        for dept, floor in self.layout.items():
            _area = self.result_widths[dept] * self.result_heights[dept]
            if floor not in area_by_floor:
                area_by_floor[floor] = 0
            area_by_floor[floor] += _area
            
        for area in area_by_floor.values():
            if area  > (self.instance.max_width * self.instance.max_height):
                print("Area error found! The total area of floor {} exceeds the maximum allowed.".format(floor))

        print("### ALL AREAS TESTS PASSED ###")

    def validate_aspect_ratios_constraints(self):
        for dept, floor in self.layout.items():
            _width = self.result_widths[dept]
            _height = self.result_heights[dept]
            _floor = int(floor) - 1
            is_valid = is_aspect_ratio_valid(_width, _height, self.instance.aspect_ratios[_floor])
            
            if not is_valid:
                print("Aspect ratio error found! Department {} => width:{}, height: {}, beta: {}, floor: {}."
                    .format(dept, _width, _height, self.instance.aspect_ratios[_floor], floor))
                return

        print("### ALL ASPECT RATIOS TESTS PASSED ###")

    def validate_overlap_constraints(self):
        _depts_by_floor = {}

        for dept, floor in self.layout.items():
            if floor not in _depts_by_floor:
                _depts_by_floor[floor] = []
            _depts_by_floor[floor].append(dept)
        
        for depts in _depts_by_floor.values():
            pairs = combinations(depts, 2)
            for pair in pairs:
                i, j = pair
                if overlap(self.centroides[i][0], self.centroides[j][0], self.result_widths[i], self.result_widths[j]) and \
                    overlap(self.centroides[i][1], self.centroides[j][1], self.result_heights[i], self.result_heights[j]):
                    print("x1 ", self.centroides[i][0])
                    print("x2 ", self.centroides[j][0])
                    print("w1 ", self.result_widths[i])
                    print("w2", self.result_widths[j])

                    print("dist_x", abs(self.centroides[i][0] - self.centroides[j][0]))
                    print("dist_w", 1/2.0*(self.result_widths[i] + self.result_widths[j]))

                    print("y1", self.centroides[i][1])
                    print("y2", self.centroides[j][1])
                    print("h1", self.result_heights[i])
                    print("h2", self.result_heights[j])

                    print("dist_y", abs(self.centroides[i][1] - self.centroides[j][1]))
                    print("dist_h", 1/2.0*(self.result_heights[i] + self.result_heights[j]))
                    print("Overlaping error found on departments {} and {}!".format(i + 1,j + 1))
                    return
                   

        print("### ALL OVERLLAPING TESTS PASSED ###")


    def validate(self):
        self.validate_area_constraints()
        self.validate_aspect_ratios_constraints()
        self.validate_overlap_constraints()
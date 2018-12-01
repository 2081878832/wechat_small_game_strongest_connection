#!/bin/python
#----coding:utf-8----
import sys
if sys.version_info.major == 2:
   reload(sys)
   sys.setdefaultencoding("utf-8")
   input = raw_input



LEFT = "◀"
RIGHT = "▶"
UP = "▲"
DOWN = "▼"
END = "■"
START = "①"
STRING_EXAMPLE = "←↑→↓⇦⇧⇨⇩▣■□▢▲▶◀▼◉◈═║╚╝╔╗"
OK = 0
NOT_OK = 1
CONTINUE = 2
VALUE_VALID = "■"
VALUE_SPACE = "□"
VALUE_START = "▣"
VALUE_USED = "◈"

IMAGE_MAP = {
    "left_left": "═",
    "left_up": "╚",
    "left_down": "╔",
    "right_up": "╝",
    "right_down": "╗",
    "right_right": "═",
    "up_up": "║",
    "up_left": "╗",
    "up_right": "╔",
    "down_down": "║",
    "down_left": "╝",
    "down_right": "╚",
    "down": DOWN,
    "up": UP,
    "left": LEFT,
    "right": RIGHT,
    "end": END,
}

def copy(x):
    if isinstance(x,list):
        if sys.version_info.major == 2:
            y = []
            for v in x:
                y.append(v)
            return y
        else:
            return x.copy()
    elif isinstance(x,dict):
        return x.copy()
    return x


class ArrayNumbers:
    def __init__(self, input_list,end=None,debug=False):
        self._rows = len(input_list)
        self._cols = len(input_list[0])
        self._array = input_list
        self._debug = debug
        self._start = None
        self._tmp_start = None
        self._tmp_end = end
        self.length = 0
        self.point_list = []
        self.end_list = []
        self.pass_list = []
        self._compute_init()
        if self._tmp_end:
            self.end_list.append(end)

    @property
    def array(self):
        return self._array

    @property
    def start(self):
        return self._start
    
    def copy(self,):
        copy_array = []
        for row in self.array:
            copy_array.append(copy(row))
        return copy_array
    
    def _compute_init(self):
        print("====init start====")
        for x in range(self._rows):
            line = ""
            for y in range(self._cols):
                v = self._array[x][y]
                line += "%s " % v
                if v == VALUE_VALID:
                    self.point_list.append((x, y))
                    self.length += 1
                if v == VALUE_START:
                    self.point_list.append((x, y))
                    self.length += 1
                    self._start = (x, y)
                    self._tmp_start = (x, y)
                    self.pass_list = [(x, y)]
                    self.point_use((x, y))
            print(line)
        print("====init stop====")

    def point_use(self, point):
        self._array[point[0]][point[1]] = VALUE_USED
        self.point_list.remove(point)

    def point_use_start(self, point):
        self.point_use(point)
        self.pass_list.append(point)
        self._tmp_start = point

    def point_use_end(self, point):
        self.point_use(point)
        self.end_list.append(point)
        self._tmp_end = point

    def get_neighbors(self, point):
        neighbors = []
        # left
        if (point[0] - 1) >= 0 and self._array[point[0] - 1][point[1]] == VALUE_VALID:
            neighbors.append(["left", (point[0] - 1, point[1])])
        if (point[0] + 1) < self._rows and self._array[point[0] + 1][point[1]] == VALUE_VALID:
            neighbors.append(["right", (point[0] + 1, point[1])])
        if (point[1] - 1) >= 0 and self._array[point[0]][point[1] - 1] == VALUE_VALID:
            neighbors.append(["up", (point[0], point[1] - 1)])
        if (point[1] + 1) < self._cols and self._array[point[0]][point[1] + 1] == VALUE_VALID:
            neighbors.append(["down", (point[0], point[1] + 1)])
        return neighbors

    @staticmethod
    def is_neighbor(point1, point2):
        if (point1[0] == point2[0] and abs(point1[1] - point2[1]) == 1) or (
                point1[1] == point2[1] and abs(point1[0] - point2[0]) == 1):
            return True
        return False

    def printf(self,):
        for row in self._array:
            print(" ".join(row))

    def result(self, extend=None):
        print("end_list", self.end_list)
        print("pass_list", self.pass_list)
        print("extend", extend)
        if extend:
            self.pass_list += extend
        if self.end_list and len(self.pass_list) < self.length:
            self.end_list.reverse()
            for point in self.end_list:
                if self.pass_list.count(point)==0:
                    self.pass_list.append(point)
        return self.pass_list

    def result_print(self,):
        self.result()
        print(self.pass_list)
        result_array = copy(self._array)
        point_start = self.pass_list[0]
        start_arrow = self.get_arrow_string(point_start, self.pass_list[1])
        result_array[point_start[0]][point_start[1]] = IMAGE_MAP[start_arrow]
        point_end = self.pass_list[-1]
        result_array[point_end[0]][point_end[1]] = IMAGE_MAP["end"]
        print("len:{0},pass_len:{1},pass_list{2}".format(self.length, len(self.pass_list), self.pass_list))
        for i in range(1, len(self.pass_list)-1):
            point0 = self.pass_list[i - 1]
            point1 = self.pass_list[i]
            point2 = self.pass_list[i + 1]
            arrow = "%s_%s" % (self.get_arrow_string(point0, point1), self.get_arrow_string(point1, point2))
            x, y = point1
            result_array[x][y] = IMAGE_MAP.get(arrow, VALUE_SPACE)
        #x, y = self.pass_list[-1]
        #result_array[x][y] = END
        # x, y = self.pass_list[0]
        # result_array[x][y] = START
        print("计算结果")
        for row in result_array:
            print(" ".join(row))

    @staticmethod
    def get_arrow_string(point1, point2):
        if point1[0] + 1 == point2[0]:
            return "down"
        elif point1[0] - 1 == point2[0]:
            return "up"
        elif point1[1] + 1 == point2[1]:
            return "right"
        elif point1[1] - 1 == point2[1]:
            return "left"
        return "end"

    def start_compute(self):
        print("====compute the start====")
        neighbors = self.get_neighbors(self._tmp_start)
        if len(neighbors) == 1:
            neighbor_point = neighbors[0][1]
            print("set the point{0} as new start".format(neighbor_point))
            self.point_use_start(neighbor_point)
            self.start_compute()

    def end_compute(self):
        print("====compute the end=====")
        if self._tmp_end:
            neighbors = self.get_neighbors(self._tmp_end)
            if len(neighbors) == 1:
                neighbor_point = neighbors[0][1]
                print("set the point{0} as new end".format(neighbor_point))
                self.point_use_end(neighbor_point)
                self.end_compute()

    def compute(self):
        print("====compute array:")
        self.printf()
        print("====compute point_list:{0}".format(self.point_list))
        print("====compute pass_list:{0}".format(self.pass_list))
        print("====compute end_list:{0}".format(self.end_list))
        print("==== now the end is :{0}".format(self._tmp_end))
        print("==== now the start is :{0}".format(self._tmp_start))
        self.start_compute()
        self.end_compute()
        print("====compute pass_list2:{0}".format(self.pass_list))
        print("==== now the end2 is :{0}".format(self._tmp_end))
        print("==== now the start2 is :{0}".format(self._tmp_start))
        for point in self.point_list:
            neighbors = self.get_neighbors(point)
            if len(neighbors) == 1:
                print("point:", point)
                neighbor_point = neighbors[0][1]
                print("neighbor_point:", neighbor_point)
                if not self._tmp_end:
                    if not self.is_neighbor(point, self._tmp_start):
                        print("set the point{0} as end,and add it's neighbor{1} to end".format(point,neighbor_point))
                        self.point_use_end(point)
                        self.point_use_end(neighbor_point)
                        return self.compute()
                    else:
                        pass
                elif self.is_neighbor(point, self._tmp_start) and not self.is_neighbor(point, self._tmp_end):
                    print("add the point{0} and it's neighbor{1} to start".format(point,neighbor_point))
                    self.point_use_start(point)
                    self.point_use_start(neighbor_point)
                    return self.compute()
                elif not self.is_neighbor(point, self._tmp_start) and self.is_neighbor(point, self._tmp_end):
                    print("add the point{0} and it's neighbor{1} to end".format(point,neighbor_point))
                    self.point_use_end(point)
                    self.point_use_end(neighbor_point)
                    return self.compute()
                elif self.is_neighbor(point, self._tmp_start) and self.is_neighbor(point, self._tmp_end):
                    pass
                        
                else:
                    return NOT_OK
        if len(self.point_list) == 0:
            if not self._tmp_end:
                return OK
            elif self.is_neighbor(self._tmp_end, self._tmp_start):
                self.pass_list = self.result()
                return OK
            else:
                print("compute failed")
                return NOT_OK
        else:
            return CONTINUE

    def guess(self):
        start = self._tmp_start
        pass_flag = False
        neighbors = self.get_neighbors(start)
        print("guess point:{0} have {1} neighbors:{2}".format(start,len(neighbors),neighbors))
        for neighbor in neighbors:
            print("now the array:")
            self.printf()
            print("now the start:{0}".format(self._tmp_start))
            print("now the end:{0}".format(self._tmp_end))
            temp_array = self.copy()
            neighbor_point = neighbor[1]
            print("guess the next {0} start :{1}".format(neighbor[0],neighbor_point))
            temp_array[neighbor_point[0]][neighbor_point[1]] = VALUE_START
            temp_array_numbers = ArrayNumbers(temp_array,end=self._tmp_end)
            print("guess the array:")
            temp_array_numbers.printf()
            ret = temp_array_numbers.compute()
            if ret == OK:
                print("guess {0} {1} successed".format(start,neighbor[0]))
                self.result(temp_array_numbers.pass_list)
                pass_flag = True
                break
            elif ret == CONTINUE:
                print("guess {0} {1} continue".format(start,neighbor[0]))
                ret1 = temp_array_numbers.guess()
                if ret1 == OK:
                    print("guess {0} {1} successed".format(start,neighbor[0]))
                    self.result(temp_array_numbers.pass_list)
                    pass_flag = True
                    break
                else:
                    print("guess {0} {1} failed".format(start,neighbor[0]))
                    del temp_array_numbers
                    continue
            elif ret == NOT_OK:
                print("guess {0} {1} failed".format(start,neighbor[0]))
                del temp_array_numbers
                continue
        if pass_flag:
            return OK
        else:
            return NOT_OK

    def do_work(self):
        print("开始计算")
        ret = self.compute()
        if ret == OK:
            self.result_print()
        elif ret == NOT_OK:
            print("计算结果：没有结果")
        else:
            ret1 = self.guess()
            if ret1 == OK:
                self.result_print()
            else:
                print("计算结果：没有结果")


def accept_input_string():
    guid_string = """请输入图像（使用数字）
                  数字1 ：代表实心方块(可经过方块)
                  数字0 ：代表空白（不可经过方块）
                  数字2 ：代表起点
                  每次输入一行，按回车结束
                  """
    print(guid_string)
    array = []
    row = 1
    col = 0
    while True:
        prompt = "请输入第%d行,按回车结束:" % row
        line_string = input(prompt)
        if len(line_string) == 0:
            break
        line_list = []
        error_flag = False
        error_msg1 = "输入格式错误,请重新输入！"
        error_msg2 = "输入格数与第一行不同,请重新输入！"
        for letter in line_string:
            try:
                if letter == "":
                    continue
                else:
                    v = int(letter)
                    if v == 0:
                        v = VALUE_SPACE
                    elif v == 1:
                        v = VALUE_VALID
                    elif v == 2:
                        v = VALUE_START
                    else:
                        print(error_msg1)
                        error_flag = True
                        break
                line_list.append(v)
            except:
                print(error_msg1)
                error_flag = True
                break
        if not error_flag:
            if col == 0:
                col = len(line_list)
                array.append(line_list)
                row += 1
            elif len(line_list) == col:
                array.append(line_list)
                row += 1
            else:
                print(error_msg2)
    print("输入完成,输入图形为:")
    for row in array:
        print("".join(row))
    return array


def input_choice():
    guid_string = """请选择操作 a 或者 b：
                             a：开始计算
                             b：退出程序           
                  """
    print(guid_string)
    input_string = input("请选择：")
    if input_string.strip().lower() == "a":
        print("选择了 a：开始计算")
        input_array = accept_input_string()
        a1 = ArrayNumbers(input_array)
        a1.do_work()
        input_choice()
    elif input_string.strip().lower() == "b":
        print("选择了 b：退出程序")
        print("程序退出")
        exit()
    else:
        print("输入错误")
        input_choice()


def test():
    test_array = [
                  [1,1,1,1,1,1],
                  [0,1,1,1,0,1],
                  [1,1,1,1,1,1],
                  [1,1,1,1,1,1],
                  [2,1,1,1,1,1],
                  [0,0,1,1,1,0]
                  ]
    picture_array = []
    for row in test_array:
        new_row = []
        for value in row:
            if value == 1:
                new_row.append(VALUE_VALID)
            elif value == 0:
                new_row.append(VALUE_SPACE)
            else:
                new_row.append(VALUE_START)
        picture_array.append(new_row)
    print("输入图形为：")
    for _row in picture_array:
        print("".join(_row))
    a1 = ArrayNumbers(picture_array)
    a1.do_work()
if __name__ == "__main__":
    input_choice()
#test()


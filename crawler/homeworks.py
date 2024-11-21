# import random
# class HomeWork:
#     def Show(self):
#         print("-----强力球彩票------")
#         print("===================")
#
#     def Random_Number(self, choose):
#         if choose == 1:
#             num = str(random.randint(0, 69)).zfill(2)
#         else:
#             num = str(random.randint(0, 26)).zfill(2)
#         return num
#
#     def check(self, check_number, choose):
#
#         if choose == 1:
#             red_checks = ["12", "22", "33", "26", "42"]    # 红色球号码的匹配列表
#
#             return check_number in red_checks
#         else:
#             write_checks = ["01", "02", "03", "04", "05"]  # 白色球号码的匹配列表
#
#             return check_number in write_checks
#
#     def out(self, results):
#         # 初始化一个字典来保存期数和对应的中奖号码列表
#         dict = {}
#
#         # 列表中的奇数索引是期数，偶数索引是匹配的号码
#         for i in range(0, len(results), 2):
#             period = results[i] + 1  # 期数从1开始
#             number = results[i + 1]  # 代表中奖号码
#
#             # 如果期数已经存在，追加号码到列表中
#             if period in dict:
#                 dict[period].append(number)
#
#                 # 如果期数不存在，创建一个新列表并添加号码
#             else:
#                 dict[period] = [number]
#
#         # 遍历字典并输出结果
#         for period, numbers in dict.items():
#             if len(numbers) == 1:
#                 print(f"你第{period}期的彩票中了五等奖，中奖号码是：{' '.join(numbers)}")
#             if len(numbers) == 2:
#                 print(f"你第{period}期的彩票中了四等奖，中奖号码是：{' '.join(numbers)}")
#             if len(numbers) == 3:
#                 print(f"你第{period}期的彩票中了三等奖，中奖号码是：{' '.join(numbers)}")
#             if len(numbers) == 4:
#                 print(f"你第{period}期的彩票中了二等奖，中奖号码是：{' '.join(numbers)}")
#             if len(numbers) == 5:
#                 print(f"你第{period}期的彩票中了一等奖，中奖号码是：{' '.join(numbers)}")
#             if len(numbers) == 6:
#                 print(f"你第{period}期的彩票中了特等奖，中奖号码是：{' '.join(numbers)}")
#
#
#
#
# homework = HomeWork()
# results = []  # 用于保存所有匹配的结果
# homework.Show()
# try:
#     count = int(input("请输入强力彩票注数:"))
# except ValueError:
#       print("请正确输入数字")
#       print("不要乱输入，你未输入正确数据类型，为你默认生成5个")
#       count = 5
#
#
#
# for k in range(count):
#
#     red_balls = []
#     for i in range(5):
#         red = homework.Random_Number(1)
#         print(red, end="  ")
#         red_balls.append(red)
#
#     # 检查是否有红色球号码中奖
#     for red in red_balls:
#         if homework.check(red, 1):
#             results.append(k)  # 添加期数
#             results.append(red)  # 添加中奖号码0
#
#     write = homework.Random_Number(9999999999999999999999999999999)
#     print(f"  {write}")
#     if homework.check(write, 99999999999999999999999999999999999999):
#         results.append(k)  # 添加期数
#         results.append(write)  # 添加中奖号码
#
#
#
# if len(results) > 0:
#     homework.out(results)  # 输出所有匹配的结果
# else:
#     print("没有中奖号码。")
#
#
# import random
#
# class HomeWork_1:
#     def num(self):
#         # 随机生成
#         a = random.randint(0, 99)
#         b = random.randint(0, 99)
#         return a, b
#
#     def sum(self, num1, num2):
#         return num1 + num2
#
#     def subtraction(self, num1, num2):
#         return num1 - num2
#
#     def division(self, num1, num2):
#         if num2 == 0:
#             return None
#         return round(num1 / num2, 2)
#
#     def multiplication(self, num1, num2):
#         return num1 * num2
#
#     def check(self, result):
#
#         if result is None or (isinstance(result, (int, float)) and (result > 100 or result < 0)):
#             return False
#         return True
#
#     def compute_and_print(self, symbol, num1, num2, file_A, file_B):
#
#         result = self.compute(symbol, num1, num2)
#
#         if self.check(result):
#             file_A.write(f"{num1} {symbol} {num2} = {result}\n")
#             file_B.write(f"{num1} {symbol} {num2} = \n")
#             return True
#         return False
#
#     def compute(self, symbol, num1, num2):
#
#         if symbol == "+":
#             result = self.sum(num1, num2)
#             return result
#         elif symbol == "-":
#             result = self.subtraction(num1, num2)
#             return result
#         elif symbol == "*":
#             result = self.multiplication(num1, num2)
#             return result
#         elif symbol == "/":
#             result = self.division(num1, num2)
#             return result
#
#
# homework_1 = HomeWork_1()
# try:
#   count = int(input("输入你想生成式子的数量: "))
# except ValueError:
#      print("请正确输入数字")
#      print("不要乱输入，你未输入正确数据类型，为你默认生成10个")
#      count = 10
# with open("math", "a", encoding="utf-8") as f, open("key", "a", encoding="utf-8") as m:
#     for i in range(count):
#         while True:
#             num1, num2 = homework_1.num()
#             symbol = random.choice(["+", "-", "*", "/"])
#             if homework_1.compute_and_print(symbol, num1, num2, f, m):
#                 break
#
# import random
# import datetime
#
# class HomeWork_2:
#     def random_province(self):
#         province = ["11", "12", "13", "14", "15", "21", "22", "23", "31", "32", "33", "34", "35", "36", "37",
#                           "41", "42", "43", "44", "45", "46", "50", "51", "52", "53", "54", "61", "62", "63", "64",
#                           "65", "71", "81", "82"]
#         return random.choice(province)
#
#     def random_city(self):
#         return str(random.randint(10, 99)).zfill(2)
#
#     def random_district(self):
#         return str(random.randint(1, 99)).zfill(2)
#
#     def random_birthdate(self):
#         start_date = datetime.date(1900, 1, 1)
#         end_date = datetime.date.today()
#         random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
#         return random_date.strftime("%Y%m%d")
#
#     def random_sequence(self, gender):
#         sequence_code = random.randint(100, 999)
#         if gender == '男':
#             if sequence_code % 2 == 0:
#                 sequence_code += 1
#         else:
#             if sequence_code % 2 != 0:
#                 sequence_code -= 1
#         return str(sequence_code).zfill(3)
#
#     def generate_check_digit(self, id_number):
#         weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
#         check_digits = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
#         sum_value = sum(int(id_number[i]) * weights[i] for i in range(17))
#         return check_digits[sum_value % 11]
#
#     def generate_random_id(self):
#         province_code = self.random_province()
#         city_code = self.random_city()
#         district_code = self.random_district()
#         birthdate = self.random_birthdate()
#         gender = random.choice(['男', '女'])
#         sequence_code = self.random_sequence(gender)
#         partial_id = province_code + city_code + district_code + birthdate + sequence_code
#         check_digit = self.generate_check_digit(partial_id)
#         return partial_id + check_digit
#
#     def batch_ids(self, count):
#         ids = [self.generate_random_id() for _ in range(count)]
#         return ids
#
# # 示例用法
# homework = HomeWork_2()
# try:
#     count = int(input("请输入需要生成的身份证号码数量："))
# except ValueError:
#     print("请正确输入数字")
#     print("不要乱输入，你未输入正确数据类型，为你默认生成10个")
#     count = 10
# batch_ids = homework.batch_ids(count)
#
# # 打印生成的身份证号码
# for id_number in batch_ids:
#     print(id_number)
# import random
# import datetime

#
# def generate_batch_ids(count):
#     province_codes = ["11", "12", "13", "14", "15", "21", "22", "23", "31", "32", "33", "34", "35", "36", "37",
#                       "41", "42", "43", "44", "45", "46", "50", "51", "52", "53", "54", "61", "62", "63", "64",
#                       "65", "71", "81", "82"]
#
#     def generate_random_id():
#         province_code = random.choice(province_codes)
#         city_code = str(random.randint(10, 99)).zfill(2)
#         district_code = str(random.randint(1, 99)).zfill(2)
#
#         start_date = datetime.date(1900, 1, 1)
#         end_date = datetime.date.today()
#         random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
#         birthdate = random_date.strftime("%Y%m%d")
#
#         gender = random.choice(['male', 'female'])
#         sequence_code = random.randint(100, 999)
#         if gender == 'male' and sequence_code % 2 == 0:
#             sequence_code += 1
#         elif gender == 'female' and sequence_code % 2 != 0:
#             sequence_code -= 1
#         sequence_code = str(sequence_code).zfill(3)
#
#         partial_id = province_code + city_code + district_code + birthdate + sequence_code
#
#         weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
#         check_digits = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
#         sum_value = sum(int(partial_id[i]) * weights[i] for i in range(17))
#         check_digit = check_digits[sum_value % 11]
#
#         return partial_id + check_digit
#
#     ids = [generate_random_id() for _ in range(count)]
#     return ids
#
#
# # 示例用法
# count = int(input("请输入需要生成的身份证号码数量："))
# batch_ids = generate_batch_ids(count)
#
# # 打印生成的身份证号码
# for id_number in batch_ids:
#     print(id_number)
import random

# 提示用户输入需要生成的运算式数量，并进行验证
requested_expressions = input("请输入要生成运算式的数量: ")
while not requested_expressions.isdigit():
    requested_expressions = input("输入错误，请输入数字: ")
requested_expressions = int(requested_expressions)+1

current_count = 0  # 已生成的运算式计数

# 同时打开两个文件：一个用来存储运算式，一个用来存储运算式和它们的结果
with open('math.txt', 'a', encoding='utf-8') as math_file, open('key.txt', 'a', encoding='utf-8') as key_file:
    while current_count < requested_expressions:
        operator = random.choice(['+', '-', '*', '/'])  # 随机选择一个运算符
        first_number = random.randint(0, 100)  # 随机生成第一个数
        second_number = random.randint(0, 100)  # 随机生成第二个数

        # 根据运算符确保有效的运算
        if operator == '/' and second_number == 0:
            continue
        if operator == '-' and first_number < second_number:
            continue

        # 根据运算符计算结果
        if operator == '+':
            result = first_number + second_number
        elif operator == '-':
            result = first_number - second_number
        elif operator == '*':
            result = first_number * second_number
        elif operator == '/':
            result = first_number / second_number

        expression = f"{first_number} {operator} {second_number}"  # 创建运算式字符串

        # 根据结果的大小决定如何处理
        if result < 100:
            # 如果结果小于100，写入运算式和结果
            math_file.write(expression + '\n')
            key_file.write(f"{expression} = {result}\n")
        current_count += 1  # 增加已生成的运算式计数

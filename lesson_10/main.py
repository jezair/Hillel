from multiprocessing import get_start_method, set_start_method


set_start_method("fork")
print(get_start_method())

# if __name__ == "__main__":
#     students = {}

#     with Pool(4) as pool:
#         averages = pool.map(calculate_average, students.values())
#         print(averages)

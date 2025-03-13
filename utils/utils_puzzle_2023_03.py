import numpy as np

is_digit = np.vectorize(str.isdigit)

def get_surrounding_indices(np_where_indices: tuple, matrix_shape) -> tuple:
    
    # Get indices
    row_indices, column_indices = np_where_indices
    
    # set offsets for the eight surrounding entries
    row_offsets = np.array([-1, -1, -1, 0, 0, 1, 1, 1])
    col_offsets = np.array([-1, 0, 1, -1, 1, -1, 0, 1])

    # calculate the neighbour entries
    neighbour_rows = row_indices[:, None] + row_offsets
    neighbour_cols = column_indices[:, None] + col_offsets

    # check that we don't check invalid indices
    proper_index_mask = (neighbour_rows >= 0) & (neighbour_rows < matrix_shape[0]) & \
                        (neighbour_cols >= 0) & (neighbour_cols < matrix_shape[1])
    
    # Get the well defined neighbour indices
    neighbour_rows = neighbour_rows[proper_index_mask]
    neighbour_cols = neighbour_cols[proper_index_mask]

    return (neighbour_rows, neighbour_cols)

def get_mask_from_indices(np_where_indices: tuple[np.ndarray, np.ndarray], matrix_shape: tuple[int]) -> np.ndarray:
    mask = np.zeros(matrix_shape, dtype = bool)
    mask[np_where_indices] = True
    return mask

def get_uninterupted_indices_of_numbers(matrix, row, col) -> tuple:
    matrix_shape = matrix.shape
    uninterupted_index_right = set()
    uninterupted_index_left = set()

    if not((0 <= row and row < matrix_shape[0]) and (0 <= col and col < matrix_shape[1])):
        raise IndexError
    
    if not is_digit(matrix[row, col]):
        raise TypeError("the entry for the given row, col pair is not a digit")
    
    next_entry = col
    while is_digit(matrix[row, next_entry]):
        uninterupted_index_right.add(next_entry)
        if next_entry < matrix_shape[1] - 1:
            next_entry += 1
        else:
            break


    previous_entry = col
    while is_digit(matrix[row, previous_entry]):
        uninterupted_index_left.add(previous_entry)
        if previous_entry >= 0 + 1:
            previous_entry -= 1
        else:
            break

    uninterupted_index = tuple(sorted((uninterupted_index_left | uninterupted_index_right)))
    return uninterupted_index

def get_tuple_dict(matrix: np.ndarray, digit_neighbour_indices: tuple):
    tuple_dict = {key: set() for key in digit_neighbour_indices[0]}

    for row, col in zip(digit_neighbour_indices[0], digit_neighbour_indices[1]):
        tuple_dict[row].add(get_uninterupted_indices_of_numbers(matrix, row, col))

    return tuple_dict

def get_number_from_text_array(text_numbers: np.ndarray) -> int:
    number = sum(int(digit) * (10 ** i) for i, digit in enumerate(reversed(text_numbers)))
    return number

def get_valid_list_of_numbers_of_puzzle(matrix: np.ndarray, tuple_dict: dict) -> list:
    valid_list_of_numbers = [get_number_from_text_array(matrix[row, tuple_val]) for row in tuple_dict for tuple_val in tuple_dict[row]]
    return valid_list_of_numbers

def get_sum_of_puzzle(matrix: np.ndarray, tuple_dict: dict) -> int:
    valid_lid_of_numbers = get_valid_list_of_numbers_of_puzzle(matrix, tuple_dict)
    return sum(valid_lid_of_numbers)

def get_sum_of_puzzle_direct(matrix: np.ndarray, tuple_dict: dict):
    val = sum(get_number_from_text_array(matrix[row, tuple_val]) for row in tuple_dict for tuple_val in tuple_dict[row])
    return val

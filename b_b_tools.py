import numpy as np



class Matrix(object):

    column_mapping = []
    row_mapping = []
    matrix = None
    Log = False
    head_estimate = None
    #If you move to node
    left_estimate = None
    left_matrix_state = None
    #If you doesn't move to node
    right_estimate = None
    right_matrix_state = None
    path = []

    def __init__(self,matrix,row_mapping=None,column_mapping=None,head_estimate=None):

        if(row_mapping is None) and (column_mapping is None):
            self.column_mapping = list(range(len(matrix)))
            self.row_mapping = list(range(len(matrix)))
        else:
            self.column_mapping = column_mapping
            self.row_mapping = row_mapping

        if not (head_estimate is None):
            self.head_estimate = head_estimate

        self.matrix = matrix.copy()

    def pos_of_max_penaltie(self):

        zero_elements_indices = np.where(self.matrix == 0)
        zero_penalites = self.count_penalties(zero_elements_indices)

        max_penalties = 0

        for i in range(len(zero_penalites)):
            if (zero_penalites[i] > max_penalties):
                max_penalties = zero_penalites[i]
                number_of_zero_element_with_max_penalty = i

       # self.right_estimate += max_penalties

        return {(zero_elements_indices[0][number_of_zero_element_with_max_penalty],
                zero_elements_indices[1][number_of_zero_element_with_max_penalty]):max_penalties}

    def first_compute(self):
        reduction_constants = self.reduction()
        head_border = np.array(reduction_constants).sum()
        pos_of_max = self.pos_of_max_penaltie()
        for_delete = list(pos_of_max.keys())[0]
        readable_for_delete = (self.row_mapping[for_delete[0]],self.column_mapping[for_delete[1]])
        max_penaltie = list(pos_of_max.values())[0]

        print(readable_for_delete)
        #For negative
        ######################################################3
        negative_matrix = Matrix(self.matrix.copy(),row_mapping=self.row_mapping,column_mapping=self.column_mapping)
        negative_matrix.path.append((for_delete,False))
        negative_estimate = head_border + max_penaltie
        negative_matrix.matrix.A[for_delete[0]][for_delete[1]] = float("Inf")
        reduction_constants = negative_matrix.reduction()
        second_head_border = np.array(reduction_constants).sum()
        negative_estimate += second_head_border
        negative_matrix.head_estimate = negative_estimate
        ##########################################################

        self.deleteRowAndColumn(for_delete[0],for_delete[1])
        left_reduction_constants = self.reduction()
        left_second_head_border = np.array(left_reduction_constants).sum()
        positive_estimate = head_border + left_second_head_border
        left_matrix = Matrix(self.matrix,row_mapping=self.row_mapping,column_mapping=self.column_mapping,head_estimate=positive_estimate)
        left_matrix.path.append((readable_for_delete,True))
        return {"left":left_matrix,"right":negative_matrix}

    def compute2(self):
        print(self.matrix)
        pos_max = self.pos_of_max_penaltie()
        for_delete = list(pos_max.keys())[0]
        readable_for_delete = (self.row_mapping[for_delete[0]],self.column_mapping[for_delete[1]])
        right_border = self.head_estimate+list(pos_max.values())[0]
        right_matrix = Matrix(self.matrix.copy(),self.row_mapping,self.column_mapping,right_border)
        right_matrix.path.append((readable_for_delete,False))



        for each in self.path:
            if not (each[1]):
                continue

            if(each[0][0] == readable_for_delete[1]):
                row_index = self.find_by_value(self.row_mapping,each[0][1])

                column_index = self.find_by_value(self.column_mapping,readable_for_delete[0])

                self.matrix.A[row_index][column_index] = float("inf")

        self.deleteRowAndColumn(for_delete[0], for_delete[1])

        print((self.row_mapping[for_delete[0]],self.column_mapping[for_delete[1]]))

        reduction_constants = self.reduction()

        left_estimate = self.head_estimate+np.array(reduction_constants).sum()
        left_matrix = Matrix(self.matrix,self.row_mapping,self.column_mapping,left_estimate)
        left_matrix.path.append((readable_for_delete,True))

        return{"left":left_matrix,"right":right_matrix}


    def find_by_value(self,array,value):
        for i in range(len(array)):
            if(array[i]==value):
                return i

        return -1

    def compute(self):
        reduction_constants = self.reduction()

        head_border = np.array(reduction_constants).sum()

        if (self.head_estimate is None):
            self.head_estimate = head_border

        self.right_estimate = self.head_estimate
        #In find_row_and_column we compute and assign right estimate also
        for_delete = self.find_row_and_column_number_for_delete()
        # right_matrix_state = self.matrix.copy()
        self.matrix.A[for_delete[0]][for_delete[1]] = float("Inf")
        self.right_matrix_state = self.matrix.copy()
        right_matrix = Matrix(self.right_matrix_state,row_mapping=self.row_mapping,column_mapping=self.column_mapping,head_estimate=self.right_estimate)

        self.deleteRowAndColumn(for_delete[0], for_delete[1])


        second_reduction = self.reduction()
        self.left_estimate =  np.array(second_reduction).sum()+self.head_estimate
        self.left_matrix_state = self.matrix.copy()

        print("-"*15," For delete: ", for_delete[0], " ", for_delete[1]," ","-"*15,)

        if(self.Log):
            print("Left estimate: ",self.left_estimate)
            print("Matrix state: ")
            print(self.left_matrix_state)
            print("-"*35)
            print("Right estimate: ",self.right_estimate)
            print("Matrix state: ")
            print(self.right_matrix_state)

        left_matrix = Matrix(self.left_matrix_state,head_estimate=self.left_estimate,row_mapping=self.row_mapping,column_mapping=self.column_mapping)

        return {"left":left_matrix,"right":right_matrix}

    def reduction(self):
        reduction_constants = []

        for i in range(len(self.matrix)):
            reduction_constant = self.matrix[i].min()
            self.matrix[i] = self.matrix[i] - self.matrix[i].min()

            reduction_constants.append(reduction_constant)

        self.matrix = self.matrix.transpose()

        for i in range(len(self.matrix)):
            reduction_constant = self.matrix[i].min()
            self.matrix[i] = self.matrix[i] - self.matrix[i].min()
            reduction_constants.append(reduction_constant)

        self.matrix = self.matrix.transpose()

        return reduction_constants

    def find_row_and_column_number_for_delete(self):

        zero_elements_indices = np.where(self.matrix == 0)
        zero_penalites = self.count_penalties( zero_elements_indices)

        max_penalties = 0

        for i in range(len(zero_penalites)):
            if (zero_penalites[i] > max_penalties):
                max_penalties = zero_penalites[i]
                number_of_zero_element_with_max_penalty = i

        self.right_estimate += max_penalties

        return (zero_elements_indices[0][number_of_zero_element_with_max_penalty],
                zero_elements_indices[1][number_of_zero_element_with_max_penalty])

    def count_penalties(self, zero_elements_indices):
        zero_penalites = []

        for i in range(len(zero_elements_indices[0])):
            row_index = zero_elements_indices[0][i]
            column_index = zero_elements_indices[1][i]

            self.matrix.A[row_index][column_index] = float("Inf")

            penalty = self.matrix[row_index].min() + self.matrix.transpose()[column_index].min()
            zero_penalites.append(penalty)

            self.matrix.A[row_index][column_index] = 0

        return zero_penalites

    def recomputeIndexesAfterDeleting(self, row_number, column_number):

        if(self.Log):
            print("Column number for delete: " ,column_number)
            print("Row number for delete: ", row_number)

            print("Before:")
            print("Column mapping: ", self.column_mapping)
            print("Row mapping: ", self.row_mapping)
            print("-" * 15)

        c_m = np.array(self.column_mapping)
        r_m = np.array(self.row_mapping)

        c_m = c_m[c_m!=column_number]
        r_m = r_m[r_m!=row_number]

        self.column_mapping = list(c_m)
        self.row_mapping = list(r_m)

        if(self.Log):
            print("After:")
            print("Column mapping: ", self.column_mapping)
            print("Row mapping: ", self.row_mapping)

    def deleteRowAndColumn(self,row_number,column_number):
        self.matrix.A[column_number][row_number] = float("Inf")

        self.matrix = np.delete(self.matrix,row_number,axis=0)
        self.matrix = np.delete(self.matrix,column_number,axis=1)

        self.recomputeIndexesAfterDeleting(row_number,column_number)

        #self.deletePath(column_number,row_number)

        if (self.Log):
            print(self.matrix)

    # #Не читаемый номер строки и столбца
    # def deletePath(self,row_number,column_number):
    #     # row_number_after_delete = -1
    #     # for i in range(len(self.row_mapping)):
    #     #     if (self.row_mapping[i] == row_number):
    #     #         row_number_after_delete = i
    #     #
    #     # column_number_after_delete = -1
    #     # for i in range(len(self.column_mapping)):
    #     #     if (self.column_mapping[i] == column_number):
    #     #         column_number_after_delete = i
    #     #
    #     # if (row_number_after_delete >= 0) and (column_number_after_delete >= 0):
    #     #     self.matrix.A[row_number_after_delete][column_number_after_delete] = float("Inf")
    #     self.matrix.A[row_number][column_number] = float("inf")
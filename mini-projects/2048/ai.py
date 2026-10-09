import random
import math


class NeuralNetwork:

    def __init__(self):
        # Architecture: 16 → 32 → 32 → 4

        self.input_size = 16
        self.hidden1_size = 32
        self.hidden2_size = 32
        self.output_size = 4

        # Weights input to hidden1
        self.weights1 = self.create_weights(self.input_size, self.hidden1_size)

        # hidden1 to hidden2
        self.weights2 = self.create_weights(self.hidden1_size, self.hidden2_size)

        # hidden2 to output
        self.weights3 = self.create_weights(self.hidden2_size, self.output_size)

        # Biases
        self.bias1 = [0] * self.hidden1_size
        self.bias2 = [0] * self.hidden2_size
        self.bias3 = [0] * self.output_size


    def create_weights(self, inputs, outputs):

        weights = []
        for i in range(outputs):
            row = []

            for j in range(inputs):
                row.append(random.uniform(-1, 1))

            weights.append(row)

        return weights


    def relu(self, x):
        return max(0, x)

    def forward(self, inputs):
        if len(inputs) == 4:
            flat_grid = []
            for row in inputs:
                for value in row:
                    flat_grid.append(value)
            inputs = flat_grid
                  
        # -------------------
        # Input → Hidden 1
        # -------------------

        hidden1 = []
        for i in range(self.hidden1_size):
            total = self.bias1[i]

            for j in range(self.input_size):
                total += inputs[j] * self.weights1[i][j]

            hidden1.append(self.relu(total))


        # -------------------
        # Hidden 1 → Hidden 2
        # -------------------

        hidden2 = []
        for i in range(self.hidden2_size):
            total = self.bias2[i]

            for j in range(self.hidden1_size):
                total += hidden1[j] * self.weights2[i][j]
            
            hidden2.append(self.relu(total))

        # -------------------
        # Hidden 2 → Output
        # -------------------

        output = []
        for i in range(self.output_size):
            total = self.bias3[i]

            for j in range(self.hidden2_size):
                total += hidden2[j] * self.weights3[i][j]

            output.append(total)

        return output


    def predict(self, inputs):
        if len(inputs) == 4:
          flat_grid = []
          for row in inputs:
              for value in row:
                  flat_grid.append(value)
          inputs = flat_grid

        output = self.forward(inputs)

        return output.index(max(output))

        # output[0] → UP
        # output[1] → DOWN
        # output[2] → LEFT
        # output[3] → RIGHT




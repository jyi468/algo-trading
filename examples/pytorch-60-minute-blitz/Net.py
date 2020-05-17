import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


# super() builtin returns a proxy object (temporary instance of superclass)
# You can access / call methods of the base class this way
class Net(nn.Module):
    def __init__(self):
        # super parameters super(sub_class, sub_class (instance))
        # This is equivalent to parameterless super() call in Python 3
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernels
        # Conv2d - def __init__(self, in_channels, out_channels, kernel_size, stride=1,
        #              padding=0, dilation=1, groups=1,
        #              bias=True, padding_mode='zeros'):
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # affine operation: y = Wx + b - Affine means preserving parallel relationships
        # nn.Linear - def __init__(self, in_features, out_features, bias=True)
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6x6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        # max_pool2d(kernel_size, stride)
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))  # Feed the convolved x into relu as input
        # If size is square, you can specify single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dims except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
# print(net)
# params = list(net.parameters())
# print(len(params))
# print(params[0].size())  # conv1's .weight

# random 32 x 32 input
input = torch.randn(1, 1, 32, 32)
out = net(input)
print(out)

# zero gradient buffers of all parameters and backprops with random gradients
# Why: https://stackoverflow.com/questions/48001598/why-do-we-need-to-call-zero-grad-in-pytorch
# Need to zero gradients before starting to do backpropagation because torch accumulates the gradients on subsequent
# This is torch's default behavior as it is convenient for RNNs
# Backward passes
# Ideally, on every training loop, you should zero out gradients so that you do paramter update correctly
net.zero_grad()
out.backward(torch.randn(1, 10))

# create optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)


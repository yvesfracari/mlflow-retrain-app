from sklearn.datasets import load_digits
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.transforms import Compose, ToTensor, Normalize
from torch import no_grad, Generator
from flask import current_app
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import joblib
import os


class MNISTModel(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(1, 10, kernel_size=2)
    self.conv2 = nn.Conv2d(10, 20, kernel_size=2)
    self.conv2_drop = nn.Dropout2d()
    self.fc1 = nn.Linear(20, 50)
    self.fc2 = nn.Linear(50, 10)

  def forward(self, x):
    x = F.relu(F.max_pool2d(self.conv1(x), 2))
    x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
    x = x.view(-1, 20)
    x = F.relu(self.fc1(x))
    x = F.dropout(x, training=self.training)
    x = self.fc2(x)
    return F.log_softmax(x)

class MNISTRetrain(object):
  class CustomDataset(Dataset):
    def __init__(self, transform=None):
      data = self.extract_data()
      self._images = data.images
      self._target = data.target
      self.transform = transform

    @staticmethod
    def extract_data():
      return load_digits()

    def __getitem__(self, idx):
      images = self._images[idx]
      targets = self._target[idx]
      if self.transform:
        images = self.transform(images)      
      return images, targets

    def __len__(self):
      return self._target.shape[0]

  def __init__(self, random_seed=0):
    self._dataset = self.CustomDataset(transform=self._preparation())
    self._train_dataset, self._test_dataset = self._train_test_split(self._dataset, random_seed=random_seed)
    self._train_loader = DataLoader(self._train_dataset, shuffle=True)
    self._test_loader = DataLoader(self._test_dataset, shuffle=True)
    self._model = MNISTModel()
    self._optimizer = optim.SGD(self._model.parameters(), lr=0.01)

  def _train_test_split(self, dataset, random_seed=0):
    return random_split(dataset, [1300, 497], generator=Generator().manual_seed(random_seed))

  def _preparation(self):
    preparation_pipeline = list()
    preparation_pipeline.append(ToTensor())
    preparation_pipeline.append(Normalize((0.1307,), (0.3081,)))
    return Compose(preparation_pipeline)

  def train_test(self):
    for epoch in range(5):
      self._train()
    results = self._test()
    return results

  def save_model(self, model_path):
    joblib.dump(self._model, model_path)

  def _train(self):
    self._model.train()
    for batch_idx, (data, target) in enumerate(self._train_loader):
      self._optimizer.zero_grad()
      output = self._model(data.float())
      loss = F.nll_loss(output, target)
      loss.backward()
      self._optimizer.step()  

  def _test(self):
    self._model.eval()
    test_loss = 0
    correct = 0
    with no_grad():
      for data, target in self._test_loader:
        output = self._model(data.float())
        test_loss += F.nll_loss(output, target, size_average=False).item()
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).sum()

    results = dict()
    test_loss /= len(self._test_loader.dataset)
    results['loss'] = test_loss
    results['accuracy'] = float(100 * correct / len(self._test_loader.dataset))
    return results
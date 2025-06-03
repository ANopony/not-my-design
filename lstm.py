import torch.nn as nn

class TimeAwareLSTM(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=64, batch_first=True)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        # x: (batch_size, sequence_length, input_size)
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # 取最后时间步
        return torch.sigmoid(self.fc(out))

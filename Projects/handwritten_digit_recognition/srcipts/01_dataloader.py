from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.ToTensor()
train_dataset = datasets.MNIST(root="../data", train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root="../data", train=False, download=True, transform=transform)


def get_loaders(batch_size=32):
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader

if __name__ == "__main__":
    train_loader, test_loader = get_loaders(batch_size=32)

    images, labels = next(iter(train_loader))

    print("images shape:", images.shape)
    print("labels shape:", labels.shape)

    import matplotlib.pyplot as plt

    for i in range(4):
        plt.subplot(1, 4, i + 1)
        plt.imshow(images[i].squeeze(), cmap="gray")
        plt.title(labels[i].item())
        plt.axis("off")
    plt.show()
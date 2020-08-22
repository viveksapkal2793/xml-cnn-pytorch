import subprocess

import numpy as np
from scipy import io as sio
from sklearn.metrics import average_precision_score
from tqdm import tqdm


def get_num_of_line(path):
    if path is None:
        return None
    else:
        cmd = ["wc", "-l", path]
        output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
        return int(output.decode("utf8").split(" ")[0])


def tqdm_with_num(loader, total):
    bar = "{desc}|{bar}| [{remaining}{postfix}]"
    return tqdm(loader, bar_format=bar, total=total)


def print_num_on_tqdm(loader, num, measure=None, last=False):
    # num = num.item()
    out_str = last and "Epoch" or "Batch"

    if measure is None:
        if num < 10.0:
            out_str = " loss={:.8f}/" + out_str
            loader.set_postfix_str(out_str.format(num))
        else:
            num = 9.9999
            out_str = " loss>{:.8f}/" + out_str
            loader.set_postfix_str(out_str.format(num))
    elif "f1" in measure:
        out_str = (measure[:-3] + "={:.8f}/" + out_str).format(num)
        loader.set_postfix_str(out_str)
    else:
        out_str = ("  " + measure + "={:.8f}/" + out_str).format(num)
        loader.set_postfix_str(out_str)


# 畳み込み後のTensorのサイズを計算
def out_size(l_in, kernel_size, channels, padding=0, dilation=1, stride=1):
    a = l_in + 2 * padding - dilation * (kernel_size - 1) - 1
    b = int(a / stride)
    return (b + 1)*channels


def precision_k(true_mat, score_mat, k):
    rank_mat = np.argsort(score_mat)
    backup = np.copy(score_mat)
    score_mat = np.copy(backup)
    for i in range(rank_mat.shape[0]):
        score_mat[i][rank_mat[i, :-k]] = 0
    score_mat = np.ceil(score_mat)
    mat = np.multiply(score_mat, true_mat)
    num = np.sum(mat, axis=1)
    p = np.mean(num / k).item()
    return p


# def precision_k(target, outputs, k=1):
#     assert target.shape == outputs.shape
#     data = np.array([target, outputs])
#     data = np.reshape(data, (2, 1, target.shape[0])) if len(target.shape) == 1 else data
#     data = np.transpose(data, (1, 2, 0))
#     for i, j in enumerate(data):
#         data[i] = j[j[:, 1].argsort()[::-1], :]
#     data = np.transpose(data, (2, 0, 1))
#     data = data[:, :, :k]
#     return np.mean(data[0])
#     # return average_precision_score(data[0], data[1])

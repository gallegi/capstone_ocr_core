import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_recall_curve
import seaborn as sns


class Evaluator:
    def __init__(self):
        pass

    @staticmethod
    def draw_PR_cureve(y_pred, y_true, iou_min_threshold=0):
        precision_ls, recall_ls, thresholds_ls = precision_recall_curve(y_true,
                                                                        y_pred)  # retieve the precision, recall and corresponding thresholds
        thresholds_ls = np.append(thresholds_ls, 0)  # add the last datapoint to the threshold list

        selected_range = thresholds_ls > iou_min_threshold
        thresholds_ls = thresholds_ls[selected_range]
        precision_ls  = precision_ls[selected_range]
        recall_ls = recall_ls[selected_range]

        plt.plot(thresholds_ls, precision_ls,
                 color=sns.color_palette()[0])  # plot the precision curve as a fuction of the set threshold
        plt.plot(thresholds_ls, recall_ls,
                 color=sns.color_palette()[1])  # plot the Recall curve as a fuction of the set threshold

        Legend = plt.legend(('alpha', 'beta'), frameon=True, loc='best')
        Legend.get_frame().set_edgecolor('k')
        plt.xlabel('IOU Threshold')
        plt.ylabel('Proportion')
        plt.show()

    @staticmethod
    def compute_iou(y_pred, y_true):
        # ytrue, ypred is a flatten vector
        y_pred = y_pred.flatten()
        y_true = y_true.flatten()
        current = confusion_matrix(y_true, y_pred, labels=[0, 1])
        # compute mean iou
        intersection = np.diag(current)
        ground_truth_set = current.sum(axis=1)
        predicted_set = current.sum(axis=0)
        union = ground_truth_set + predicted_set - intersection
        IoU = intersection / union.astype(np.float32)
        return np.mean(IoU)

    # def compute_mean_IOU(self,labels,predicts):

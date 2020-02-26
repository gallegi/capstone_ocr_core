class Box:
    def __init__(self, xmin=None, ymin=None, xmax=None, ymax=None, w=None, h=None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.w = w
        self.h = h
        if self.w is not None:
            self.xmax = self.xmin + w
        if self.h is not None :
            self.ymax = self.ymin + h
        if self.xmax is not None:
            self.w = self.xmax - self.xmin
        if self.ymax is not None:
            self.h = self.ymin - self.ymin



    def get_center(self):
        return (self.xmax - self.xmin) / 2, (self.ymax - self.ymin) / 2

    def compute_overlap(self, box):
        box: Box

        x_left = max(self.xmin, box.xmin)
        y_top = max(self.ymin, box.ymin)
        x_right = min(self.xmax, box.xmax)
        y_bottom = min(self.ymax, box.ymax)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # compute the area of both AABBs
        bb1_area = self.w * self.h
        bb2_area = box.w * box.h

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
        assert iou >= 0.0
        assert iou <= 1.0
        return iou

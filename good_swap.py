import numpy as np
import pandas as pd

class smartTable():
    def __init__(self, path2table):
        base_table = pd.read_csv(path2table)
        base_table.columns = base_table.iloc[1, :]
        self.table = base_table.iloc[2:33, :7]
        self.name_set = set(self.table["תורן מחלקה"])
        self.name_set.update(set(self.table["תורן 3"]))
        self.name2numDict = {i:name for name, i in enumerate(self.name_set)}
        self.num2nameDict = {name:i for name, i in enumerate(self.name_set)}

        col1 = self.table["תורן מחלקה"].values
        col2 = self.table["תורן 3"].values
        worker_at_date = []
        for worker1, worker2 in zip(col1, col2):
            worker_at_date.append([self.name2numDict[worker1], self.name2numDict[worker2]])
        self.column_worker_date = np.array(worker_at_date)
        self.nDays = len(self.column_worker_date)

    def is_legal(self, name, date):
        assert date > 0 and date <= self.nDays
        worker_num = self.name2numDict[name]
        idx = date - 1
        if idx == 0:
            return np.all(self.column_worker_date[:2,:] != worker_num)
        elif idx == self.nDays - 1:  # last row
            return np.all(self.column_worker_date[-2:,:] != worker_num)
        else:
            return np.all(self.column_worker_date[idx-1:idx+2,:] != worker_num)

    def findSwap2(self, name, date2remove):
        worker_num = self.name2numDict[name]
        assert np.any(self.column_worker_date[date2remove-1,:] == worker_num), name + "dosent work on day " + str(date2remove)
        # for name2 in self.name_set:
        #     worker2_num = self.name2numDict[name2]

        for day in range(1,self.nDays + 1):
            if not self.is_legal(name, day):  # name cant work in this day
                continue

            curr_workers = self.column_worker_date[day-1,:]
            curr_workers_names = [self.num2nameDict[curr_worker] for curr_worker in curr_workers]
            for curr_work in curr_workers_names:
                if self.is_legal(curr_work, date2remove):
                    print("found good swap: ", name, "," + str(date2remove) + " " + curr_work + " " + str(day))

if __name__=="__main__":
    s_table = smartTable(r"C:\Users\urigross\Documents\table1.csv")


    s_table.findSwap2('חן', 12)
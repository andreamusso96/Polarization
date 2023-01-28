import os
from config import CODE_PATH
from typing import Dict, List
import pandas as pd


class TerminationReason:
    success = 'success'
    database_locked = 'database_locked'
    time_limit_reached = 'time_limit_reached'


class SlurmOutputReader:
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.sim_id = self.get_sim_id()

    def get_termination_reason(self):
        if not self.simulation_successful():
            counts = self.search_simulation_fail_reason()
        else:
            counts = self.get_counts_dict()
            counts[TerminationReason.success] = 1

        counts['file_name'] = self.file_name
        counts['sim_id'] = self.sim_id
        return counts

    def read_output(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        return lines

    def simulation_successful(self):
        lines = self.read_output()
        error_count = 0
        for line in lines:
            if 'error' in line:
                error_count += 1

        return error_count == 0

    def search_simulation_fail_reason(self) -> Dict[str, int]:
        lines = self.read_output()
        counts = self.get_counts_dict()
        for line in lines:
            if self.check_database_is_locked(line=line):
                counts[TerminationReason.database_locked] += 1
            if self.check_time_limit_reached(line=line):
                counts[TerminationReason.time_limit_reached] += 1

        return counts

    def get_sim_id(self) -> int:
        lines = self.read_output()
        sim_id = None
        for line in lines:
            if 'SIM ID' in line:
                sim_id = int(line.split(' ')[-1])

        return sim_id

    @staticmethod
    def get_counts_dict() -> Dict[str, int]:
        counts = {TerminationReason.success: 0, TerminationReason.database_locked: 0,
                  TerminationReason.time_limit_reached: 0}
        return counts

    @staticmethod
    def check_database_is_locked(line: str) -> bool:
        return 'database is locked' in line

    @staticmethod
    def check_time_limit_reached(line: str) -> bool:
        return 'slurmstepd: error' in line and 'DUE TO TIME LIMIT' in line


class SimulationOutputAnalyser:
    def __init__(self, min_job_id: int):
        self.folder_path = CODE_PATH + '/Slurm/SlurmOutput/'
        self.min_job_id = min_job_id
        self.file_names = self.get_slurm_file_names()

    def get_termination_reasons(self) -> pd.DataFrame:
        termination_reasons = []
        for file_name in self.file_names:
            reader = SlurmOutputReader(file_path=self.folder_path + file_name, file_name=file_name)
            termination_reasons.append(reader.get_termination_reason())

        return pd.DataFrame(termination_reasons)

    def get_slurm_file_names(self) -> List[str]:
        all_file_names = os.listdir(path=self.folder_path)
        slurm_file_names = []
        for file_name in all_file_names:
            if 'slurm' in file_name:
                job_id = int(file_name.split('-')[-1].replace('.out', ''))
                if job_id >= self.min_job_id:
                    slurm_file_names.append(file_name)
        return slurm_file_names

    def print_termination_reasons(self):
        termination_reasons = self.get_termination_reasons()
        for tr in termination_reasons:
            print(tr)


if __name__ == '__main__':
    analyser = SimulationOutputAnalyser(min_job_id=7756509)
    t = analyser.get_termination_reasons()
    print(t.head())

import pandas as pd
from RefineODs import refine_ods
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--file_name', '-fn', help="Name of the OD survey file", required=True)
parser.add_argument('--time', '-t', default="all", help="Start time of the OD Matrix")
parser.add_argument('--mode', '-m', default="all", help="If the state is chosen to be separate, a mode should be specified from ['Vehicle', 'Bus', 'Subway', 'Walk/Bike']")
args = parser.parse_args()


class ProcessODMatrix:
    def __init__(self, already_refined, file_name, time, mode, orig_column='d_orisr', dest_column='d_dessr',
                 time_column='d_hrede', mode_column='d_mode1'):
        self.survey = pd.read_csv(file_name)
        if not already_refined:
            self.survey = refine_ods(self.survey)
        self.orig_column = orig_column
        self.dest_column = dest_column
        self.time_column = time_column
        self.mode_column = mode_column
        self.time = time
        self.mode = mode
        self.get_matrix()

    def make_file(self, info_dict, time, mode="all"):
        result = "$OR,D2\n* From-Time To-Time\n"
        result += str(time) + " " + str(time + 1) + "\n"
        result += "* Factor\n1\n"

        result += "*\t{:9s} {:10s} {:10s}".format("from", "to", "num of trips")
        if mode != "all":
            result += " by " + mode + "\n"
        else:
            result += "\n"
        for (orig, dest), number in info_dict.items():
            a = "taz_" + str(orig)
            b = "taz_" + str(dest)
            c = str(number)
            result += "\t{:10s} {:10s} {:10s}".format(a, b, c) + "\n"
        od_matrix_file_name = "OD_MATRIX_" + str(time) + "-" + str(time + 1)
        if mode != "all":
            od_matrix_file_name += "_" + mode
        if not os.path.exists("OD Matrix"):
            os.makedirs("OD Matrix")
        od_matrix_file = open("OD Matrix/" + od_matrix_file_name + ".od", "w+")
        n = od_matrix_file.write(result)
        od_matrix_file.close()

    def get_matrix_for_time_mode(self):
        time_column, mode_column = self.time_column, self.mode_column
        orig_column, dest_column = self.orig_column, self.dest_column
        time, mode, survey = self.time, self.mode, self.survey
        survey = survey[(survey[time_column] == time) &
                        (survey[mode_column] == mode)]
        survey_grouped = survey.groupby([orig_column, dest_column]).size()
        survey_dict = dict(survey_grouped)
        self.make_file(survey_dict, time, mode)
        
    def get_matrix(self):
        time_column, mode_column = self.time_column, self.mode_column
        orig_column, dest_column = self.orig_column, self.dest_column
        time, mode, survey = self.time, self.mode, self.survey
        print(mode)
        if time != "all":
            survey = survey[(survey[time_column] == time)]
        if mode != "all":
            print(len(survey))
            survey = survey[(survey[mode_column] == mode)]
            print(len(survey))

        if time == "all":
            for time_index in range(0, 25):
                temp_survey = survey[(survey[time_column] == time_index)]
                print("FOR time " + str(time_index) + " " + str(len(temp_survey )))
                survey_grouped = temp_survey .groupby([orig_column, dest_column]).size()
                survey_dict = dict(survey_grouped)
                self.make_file(survey_dict, time_index, mode)
        else:
            survey_grouped = survey.groupby([orig_column, dest_column]).size()
            survey_dict = dict(survey_grouped)
            self.make_file(survey_dict, time, mode)

        
    def get_matrix_for_time(self):
        time_column, mode_column = self.time_column, self.mode_column
        orig_column, dest_column = self.orig_column, self.dest_column
        time, survey = self.time, self.survey
        survey = survey[(survey[time_column] == time)]
        survey_grouped = survey.groupby([orig_column, dest_column]).size()
        survey_dict = dict(survey_grouped)
        self.make_file(survey_dict, time)



if __name__=="__main__":
    SURVEY_FILE_NAME = args.file_name
    TIME = args.time
    TIME = TIME if TIME == "all" else int(TIME)
    MODE = args.mode
    MODE_STATE = "all" if MODE=="all" else "separated"
    TIME_STATE = "all" if TIME=="all" else "separated"
    OK = True
    if MODE not in ["all", "Vehicle", "Bus", "Subway", "Taxi", "Walk", "Bike", "Motorcycle", "Train"]:
        print("Please enter a valid mode of transportation between "+str(["all", "Vehicle", "Bus", "Subway", "Taxi", "Walk", "Bike", "Motorcycle", "Train"]))
        OK = False
    if TIME not in ["all"] + list(range(0, 24)):
        print("Please enter a valid time between 0 and 24 or enter all")
        OK = False


    ORIG_COLUMN_NAME = 'd_orisr'
    DEST_COLUMN_NAME = 'd_dessr'
    TIME_COLUMN_NAME = 'd_hrede'
    MODE_COLUMN_NAME = 'd_mode1'
    if OK :
        process_OD_matrix = ProcessODMatrix(already_refined="refined" in SURVEY_FILE_NAME, file_name=SURVEY_FILE_NAME,
                                            time=TIME, mode=MODE,orig_column=ORIG_COLUMN_NAME, dest_column=DEST_COLUMN_NAME,
                                            time_column=TIME_COLUMN_NAME, mode_column=MODE_COLUMN_NAME)

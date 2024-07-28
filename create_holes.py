
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys
import random
import csv
from decimal import Decimal
import os
from CustomFunctionClass import MakeFilesClass
 
class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI,self).__init__()
		
        loadUi("main_gui.ui",self)

        try:
            makeFilesClass = MakeFilesClass()
            self.pushButton_createFiles.clicked.connect(lambda:makeFilesClass.createFiles(self))
            self.probability_horizontalSlider.valueChanged.connect(lambda:makeFilesClass.myvalueChanged(self))
            self.actionCreate_Holes_In_Datamine.triggered.connect(lambda:makeFilesClass.createDMFiles(self))
        except:
            with open("error.txt", mode='w', newline='') as file:
                file.write('something went wrong')
                file.close()
         
    def generate_grid_collars(self,grid_size, spacing, elevation, origin_x, origin_y):
        """
        Generate drillhole collars on a regular grid with a custom origin.
        
        :param grid_size: Tuple (rows, cols) defining the grid dimensions
        :param spacing: Spacing between drillholes
        :param z_min: Minimum Z value for elevation
        :param z_max: Maximum Z value for elevation
        :param origin_x: X coordinate for the origin
        :param origin_y: Y coordinate for the origin
        :return: List of dictionaries containing collar data
        """
        rows, cols = grid_size
        collars = []
        z=elevation
        for i in range(rows):
            for j in range(cols):
                drillhole_id = f'DH{i*cols + j + 1:04d}'  # Generate drillhole ID e.g., DH0001
                x = origin_x + j * spacing
                y = origin_y + i * spacing
                #z = random.uniform(z_min, z_max)
                
                collar = {
                    'ID': drillhole_id,
                    'X': x,
                    'Y': y,
                    'Z': z
                }
                collars.append(collar)
        
        return collars	
    
    def generate_survey_and_assay_data(self,azimuth,dip,collars, maxHoleLength,sampleInterval, origin_x, background_means, background_stds, high_grade_prob, high_grade_means, high_grade_stds, gradient_factor):
        """
        Generate survey and assay data for each drillhole.
        
        :param collars: List of collar data
        :param num_intervals_min: Minimum number of intervals per drillhole
        :param num_intervals_max: Maximum number of intervals per drillhole
        :param background_means: Dictionary with mean values for background assays
        :param background_stds: Dictionary with standard deviations for background assays
        :param high_grade_prob: Probability of encountering high-grade zones
        :param high_grade_means: Dictionary with mean values for high-grade assays (for log-normal distribution)
        :param high_grade_stds: Dictionary with standard deviations for high-grade assays (for log-normal distribution)
        :param gradient_factor: Factor to apply the mineral trend in the X direction
        :return: Lists of dictionaries containing survey and assay data
        """
        surveys = []
        assays = []
    
        for collar in collars:
            drillhole_id = collar['ID']
            from_depth = 0.0
            num_intervals = maxHoleLength/sampleInterval # random.randint(num_intervals_min, num_intervals_max)
            
            x_position = collar['X']
            
            for _ in range(int(num_intervals)):
                
                to_depth = from_depth + sampleInterval # random.uniform(1, 50)  # Example interval length
                #azimuth = random.uniform(0, 360)  # Azimuth in degrees
                #dip = random.uniform(-90, 90)    # Dip in degrees
                
                # Survey data
                survey = {
                    'ID': drillhole_id,
                    'From': from_depth,
                    'Azimuth': azimuth,
                    'Dip': dip
                }
                surveys.append(survey)
                
                # Assay data
                if random.random() < high_grade_prob:
                    # High-grade zone
                    au_assay = round(random.normalvariate(high_grade_means['Au'], high_grade_stds['Au']), 2)
                    cu_assay = round(random.normalvariate(high_grade_means['Cu'], high_grade_stds['Cu']), 2)
                    ag_assay = round(random.normalvariate(high_grade_means['Ag'], high_grade_stds['Ag']), 2)
                else:
                    # Background values
                    au_assay = round(random.normalvariate(background_means['Au'], background_stds['Au']), 2)
                    cu_assay = round(random.normalvariate(background_means['Cu'], background_stds['Cu']), 2)
                    ag_assay = round(random.normalvariate(background_means['Ag'], background_stds['Ag']), 2)
                
                # Apply gradient factor
               # au_assay += gradient_factor * (x_position - origin_x)
               # cu_assay += gradient_factor * (x_position - origin_x)
               # ag_assay += gradient_factor * (x_position - origin_x)
                
                cu_assay=round(random.uniform(0.01, high_grade_means['Cu']),2) if cu_assay<=0 else cu_assay
                au_assay=au_assay*(-1) if au_assay<0 else au_assay
                ag_assay=ag_assay*(-1) if ag_assay<0 else ag_assay

                assay = {
                    'ID': drillhole_id,
                    'From': from_depth,
                    'To': to_depth,
                    'Au': max(au_assay,0),  # Ensure no negative values
                    'Cu': cu_assay,  # Ensure no negative values
                    'Ag': ag_assay   # Ensure no negative values
                }
                assays.append(assay)
                
                from_depth = to_depth  # Set the start of the next interval to the end of the current one
        
        return surveys, assays

    def write_data_to_csv(self,data, file_name, fieldnames):
        """
        Write the list of data to a CSV file.
        
        :param data: List of dictionaries containing the data
        :param file_name: Name of the CSV file
        :param fieldnames: List of fieldnames for the CSV file
        """
        fileFullName = os.path.join(r"c:\\Database\\CreateHoles", file_name)
        #os.umask(0)
        if not os.path.exists("c:\\Database\\CreateHoles"):
            os.makedirs("c:\\Database\\CreateHoles")

        with open(fileFullName, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
         

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = MainUI()
	ui.show()
	app.exec_()

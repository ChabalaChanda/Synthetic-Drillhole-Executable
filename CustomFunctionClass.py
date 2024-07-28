from decimal import Decimal
import win32com.client
import shutil
import os

class MakeFilesClass():
    def createFiles(self,dta):
    
        grid_size = (int(dta.x_size.text()), int(dta.y_size.text()))  # 20 rows by 20 columns
        spacing = Decimal(dta.spacing.text())  # 20 units spacing between drillholes

        stLength = dta.drilllength.text()

        sampleInterval = float(dta.sample_interval.text())

        print(stLength)
      
        hole_length = int(dta.drilllength.text()) if stLength.find(".")==-1 else float(dta.drilllength.text())
             #drillhole length required

        elevation = Decimal(dta.z_origin.text())

        origin_x = Decimal(dta.x_origin.text())  # Custom X coordinate origin
        origin_y = Decimal(dta.y_origin.text())   # Custom Y coordinate origin

        azimuth = Decimal(dta.azimuth.text())
        dip = Decimal(dta.dip.text())

        gradient_factor = 0.005  # Factor to apply the mineral trend

        # Mean and standard deviation for background assay values (for normal distribution)
        background_means = {dta.element_1.text(): float(Decimal(dta.lg_element_1_mean.text())), 
                            dta.element_2.text(): float(Decimal(dta.lg_element_2_mean.text())), 
                            dta.element_3.text(): float(Decimal(dta.lg_element_3_mean.text()))}
        background_stds  = {dta.element_1.text(): float(Decimal(dta.lg_element_1_std.text())), 
                            dta.element_2.text(): float(Decimal(dta.lg_element_2_std.text())), 
                            dta.element_3.text(): float(Decimal(dta.lg_element_3_std.text()))}

        # Probability of encountering high-grade zones
        high_grade_prob = Decimal(dta.probability_value.text())/100 #0.65  # 10% chance of a high-grade interval

        # Mean and standard deviation for high-grade assay values (for log-normal distribution)
        high_grade_means = {dta.element_1.text(): float(Decimal(dta.hg_element_1_mean.text())), 
                            dta.element_2.text(): float(Decimal(dta.hg_element_2_mean.text())), 
                            dta.element_3.text(): float(Decimal(dta.hg_element_3_mean.text()))}
        
        high_grade_stds = { dta.element_1.text(): float(Decimal(dta.hg_element_1_std.text())), 
                            dta.element_2.text(): float(Decimal(dta.hg_element_2_std.text())), 
                            dta.element_3.text(): float(Decimal(dta.hg_element_3_std.text()))}

        # Generate collars on a grid with custom origin
        collars = dta.generate_grid_collars(grid_size, spacing, elevation, origin_x, origin_y)

        # Generate survey and assay data
        surveys, assays = dta.generate_survey_and_assay_data(azimuth,dip,collars, hole_length,sampleInterval, origin_x, background_means, background_stds, high_grade_prob, high_grade_means, high_grade_stds, gradient_factor)

        # Write data to CSV files
        dta.write_data_to_csv(collars, 'collars.csv', ['ID', 'X', 'Y', 'Z'])
        dta.write_data_to_csv(surveys, 'surveys.csv', ['ID', 'From', 'Azimuth', 'Dip'])
        dta.write_data_to_csv(assays, 'assays.csv', ['ID', 'From', 'To', 'Au', 'Cu', 'Ag'])

        dta.messageArea.setText('CSV files successfully created')
    def myvalueChanged(self,data):
        data.probability_value.setText(str(data.probability_horizontalSlider.value()))
    def createDMFiles(self,data):

        data.messageArea.setText('Connecting to StudioRM')
        oDmApp = win32com.client.Dispatch("Datamine.StudioRM.Application")
        print(oDmApp.version)
        
        fileFullName = os.path.join(r"c:\\Database\\CreateHoles", "create_drillholes.mac")

        if not os.path.exists("c:\\Database\\CreateHoles"):
            os.makedirs("c:\\Database\\CreateHoles")

        with open(fileFullName,"w") as file:
            file.write("!start mkdh\n"+
            "!inpfil &out(collars_txt)\n"+
            "Import collars\n"+
            "BHID A 8 Y \"\"\n"+
            "XCOLLAR N Y -\n"+
            "YCOLLAR N Y -\n"+
            "ZCOLLAR N Y -\n"+
            "-\n"+
            "Y\n"+
            "c:\\Database\\CreateHoles\\collars.csv\n"+

            "!inpfil &out(assays_txt)\n"+
            "Import collars\n"+
            "BHID A 8 Y \"\"\n"+
            "FROM N Y -\n"+
            "TO N Y -\n"+
            "Au N Y -\n"+
            "Cu N Y -\n"+
            "Ag N Y -\n"+
            "-\n"+
            "Y\n"+
            "c:\\Database\\CreateHoles\\assays.csv\n"+

            "!inpfil &out(surveys_txt)\n"+
            "Import collars\n"+
            "BHID A 8 Y \"\"\n"+
            "AT N Y -\n"+
            "BRG N Y -\n"+
            "DIP N Y -\n"+
            "-\n"+
            "Y\n"+
            "c:\\Database\\CreateHoles\\surveys.csv\n"+

            "!holes3d  &COLLAR(collars_txt),\n"+
                    "&SURVEY(surveys_txt),\n"+
                    "&SAMPLE1(assays_txt),\n"+
                    "&OUT(holes),*BHID(BHID),*XCOLLAR(XCOLLAR),*YCOLLAR(YCOLLAR),\n"+
                    "*ZCOLLAR(ZCOLLAR),*FROM(FROM),*TO(TO),*AT(AT),*BRG(BRG),\n"+
                    "*DIP(DIP),*SURVSMTH=1.0,*ENDPOINT=1.0,*DIPMETH=1.0,\n"+
                    "*INCLMISS=0.0,*KEEPNAME=1.0,*PROMPT=1.0\n"+
                    
                    
            "!END \n")
            file.close()
        


        data.messageArea.setText('Importing csv files')
       
       

        dstFile_collars = os.path.join(oDmApp.ActiveProject.Folder, "collars.csv")
        dstFile_surveys = os.path.join(oDmApp.ActiveProject.Folder, "surveys.csv")
        dstFile_assays = os.path.join(oDmApp.ActiveProject.Folder, "assays.csv")
        macro = os.path.join(oDmApp.ActiveProject.Folder, "create_drillholes.mac")

        progCollar = os.path.join("c:\\Database\\CreateHoles","collars.csv")
        progSurvey = os.path.join("c:\\Database\\CreateHoles","surveys.csv")
        progassays = os.path.join("c:\\Database\\CreateHoles","assays.csv")
        progMacro = os.path.join("c:\\Database\\CreateHoles","create_drillholes.mac")

        if os.path.exists(dstFile_collars):
            os.remove(dstFile_collars)
        shutil.copy(progCollar,oDmApp.ActiveProject.Folder)
        data.messageArea.setText('Imported collars') 

        if os.path.exists(dstFile_surveys):
            os.remove(dstFile_surveys)
        shutil.copy(progSurvey,oDmApp.ActiveProject.Folder)
        data.messageArea.setText('Imported surveys')          

        if os.path.exists(dstFile_assays):
            os.remove(dstFile_assays)
        shutil.copy(progassays,oDmApp.ActiveProject.Folder)
        data.messageArea.setText('Imported assays') 

        if os.path.exists(macro):
            os.remove(macro)
        shutil.copy(progMacro,oDmApp.ActiveProject.Folder)

        data.messageArea.setText('Creating holes ..... this can take few seconds or minutes depending on grid size....') 
        oDmApp.ParseCommand("xrun"+
	    " 'create_drillholes.mac'"+
	    " 'mkdh'")

        data.messageArea.setText('Loading drillhole file in StudioRM......') 

        oDmApp.ActiveProject.Data.LoadFile("HOLES.dm")

        data.messageArea.setText('Drillhole file : Holes.dm has been created and loaded in StudioRM! \n@Chanda Chabala email:chabalachanda@yahoo.com')
  
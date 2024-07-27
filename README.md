# Synthetic-Drillhole-Executable
Create collars, surveys and assays files and run automated import and creation of pseudo holes into StudioRM geological software.

![synthetic-gui_2](https://github.com/user-attachments/assets/e33f6a89-bf32-4997-8aa9-26a3182eab80)

1. Clone or download the source code
2. Run the "create_holes.py" file
3. A gui will pop up where drillhole parameters can be adjusted to one's needs.
4. Click "Create Drillhole Files" button on the interface to creaate comma separated value's file (CSV).
5. Go to "File - >  Create Holes In Datamine " to create pseudo holes from the generated csv files, this will automatically run and load the holes into the 3D window.
6. Step 5 will only work when DATAMINE STUDIORM IS OPEN!


![Screenshot 2024-07-27 084858](https://github.com/user-attachments/assets/f0ef99bb-af53-4df6-bcd1-de6bf2588946)

To download an executable and installable version of the app, please follow this link :  https://drive.google.com/file/d/1spDa4eFa5032Qj8GgtvkHMIIHOuA2vYQ/view?usp=sharing

You can watch a demo on this link : https://youtu.be/Vl2_UvIHimE


Detailed Explanation :

The program allows users to input various parameters to model drillhole sampling in a grid pattern. 

Here’s a breakdown of the different sections and components seen in the interface:

Grid Properties:

Grid: The user can enter the dimensions of the grid; in this case, it's set to 20 rows by 20 columns.
Hole Spacing: Defines the spacing between the drillholes, set to 25 units.
Hole Length: Determines how deep each hole will go, which is 100 units here.
Sample Interval: Indicates the frequency of sampling along the drillhole length, at every 1 unit in this example.
Origin Coordinates:

X Origin, Y Origin, Z Origin: These fields allow the user to set the starting coordinates for the grid of drillholes.
Azimuth: The angular measurement relative to the north direction, set to 10 degrees here.
Dip: The angle at which the drillhole deviates from the horizontal plane, set to 90 degrees here.
Data Properties: This section has inputs for defining the elemental composition and grade distribution of the drillhole samples.

Elements: It lists elements like Copper (Cu), Silver (Ag), and Gold (Au). These can all be changed to element of desire and preference.

Low Grade and High Grade: For each element, mean value and standard deviation are specified for low and high-grade ore respectively.

Probability Occurence HG: A slider indicating the probability of occurrence of high grade (HG) ore. It is set at 64%.

Create Drillhole Files: This button generates the csv files (lazy to edit!) and synthetic drillholes are created by accessing " Create Holes In Datamine" under "File" on the menubar,

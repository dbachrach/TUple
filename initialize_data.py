from exam.models import *

def initialize_data():
    problems_data = [('m1', 'How many significant figures are in the  mass 0.05300 kg?', '6', '5', '4', '3', '2', 'c'),
    ('c1', 'The ratio of the number of bismuth atoms to the number of oxygen atoms in Bi<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub> is', '2:1', '2:3', '2:7', '1:6', 'none of the above', 'd'),
    ('m2', 'The best answer for the sum of the masses 4.62g, 58.4322 g and 7.854 g is', '70.9062 g', '70.906 g', '70.91 g', '70.9 g', '71 g', 'c'),
    ('c2', 'How many atoms are in 12 molecules of succinic acid HO<sub>2</sub>CCH<sub>2</sub>CH<sub>2</sub>CO<sub>2</sub>H?', '12', '14', '120', '144', '168', 'e'),
    ('m3', 'The proper conversion of 0.0462 kg is', '4.62 x 10<sup>3</sup> g', '4.62 x 10<sup>2</sup> g', '462 g', '46.2 g', '4.62 g', 'd'),
    ('c3', 'A 25.0 cm<sup>3</sup> sample has a mass of 41.88 g and a molar mass (molecular weight) of 153.33 g/mol. The molar volume (volume of one mole) of the substance is', '6.83 cm<sup>3</sup>/mol', '91.5 cm<sup>3</sup>/mol', '68.3 cm<sup>3</sup>/mol', '915 cm<sup>3</sup>/mol', 'none of the above', 'b'),
    ('m4', 'Which of the following is the largest mass?', '7.5 x 10<sup>7</sup> ng', '2.5 x 10<sup>5</sup> &mu;g', '3.5 x 10<sup>2</sup> mg', '1.5 x 10<sup>-1</sup> g', '6.5 x 10<sup>-6</sup> kg', 'c'),
    ('c4', 'In X<sub>2</sub>O<sub>3</sub>, 65.20% of the mass is due to X. What is the atomic mass (atomic weight) of X? (AM(O) = 16.00 g/mol)', '22.5 g/mol', '30.0 g/mol', '45.0 g/mol', '67.5 g/mol', '90.0 g/mol', 'c'),
    ('c5', 'The distance around an US college track is 4.40 x 10<sup>2</sup> yd. Since 1.00 in = 2.54 cm, find the distance of the track in meters.', '481 m', '402 m', '134 m', '62.4 m', '33.5 m', 'b'),
    ('c6', 'Consider the <i>unbalanced</i> chemical equation,<br>&nbsp; &nbsp; &nbsp; Al(OH)<sub>3</sub> + H<sub>2</sub>CO<sub>3</sub> &rarr; Al<sub>2</sub>(CO<sub>3</sub>)<sub>3</sub> +H<sub>2</sub>O.<br>When balanced with the smallest whole number coefficients, the coefficient of H<sub>2</sub>CO<sub>3</sub> will be', '1', '2', '3', '5', 'none of the above', 'c'),
    ('m5', 'A standard sheet of paper is 8.5 x 11 inches. What is the surface area, in cm<sup>2</sup>, of one side of a sheet of paper?<br>(1.00 in = 2.54 cm)', '2.4 x 10<sup>2</sup> cm<sup>2</sup>', '6.0 x 10<sup>2</sup> cm<sup>2</sup>', '94 cm<sup>2</sup>', '37 cm<sup>2</sup>', '14 cm<sup>2</sup>', 'b'),
    ('c7', 'Consider the following reaction:<br>&nbsp; &nbsp; &nbsp;N<sub>2 (g)</sub> + 3H<sub>2 (g)</sub> &rarr; 2NH<sub>3</sub>(g)<br>How much N<sub>2</sub> would be required to react completely with 1.50 mol of H<sub>2</sub>?<br>(MM(N<sub>2</sub>) = 28.02 g/mol)', '14.0 g', '28.0 g', '42.0 g', '126 g', 'none of the above', 'a'),
    ('m6', 'A cubic block of a pure metal which is 4.0 cm long weighs 1.26 lb. The block is made from which metal? (Note: 1 lb = 453.6 g)', 'Al, <i>d</i> = 2.70 g/cm<sup>3</sup>', 'Cu, <i>d</i> = 8.93 g/cm<sup>3</sup>', 'Pb, <i>d</i> = 11.4 g/cm<sup>3</sup>', 'Ag, <i>d</i> = 10.5 g/cm<sup>3</sup>', 'Au, <i>d</i> = 19.3 g/cm<sup>3</sup>', 'b'),
    ('c8', 'How many atoms are present in 21.1 grams of silicon?<br>(AM(Si) = 28.09 g/mol; <i>N<sub>A</sub></i> = 6.022 x 10<sup>23</sup> mol<sup>-1</sup>)', '3.57 x 10<sup>26</sup> atoms', '4.52 x 10<sup>23</sup> atoms', '1.25 x 10<sup>-24</sup> atom', '8.02 x 10<sup>23</sup> atom', '1.02 x 10<sup>21</sup> atom', 'b'),
    ('m7', 'What is the atmospheric pressure if the weather report lists the "barometric pressure" as 29.97 (inches of Hg), when the temperature is 0 &deg;C?<br>(1.000 in = 2.540 cm; 760 mmHg = 1 atm)', '0.1002 atm', '0.837 atm', '0.935 atm', '1.002 atm', 'none of the above', 'd'),
    ('c9', 'Which of the following chemical samples contain the largest number of atoms?', '1.0 moles of H<sub>2</sub>SO<sub>4</sub>', '2.0 moles of H<sub>3</sub>PO<sub>4</sub>', '3.0 moles of HClO<sub>4</sub>', '4.0 moles of HNO<sub>3</sub>', '5.0 moles of HCl', 'd'),
    ('c10', 'A sample contains copper(I) chloride, CuCl, at a purity of 95.2%. If 2.00 x 10<sup>2</sup> g of the CuCl compound is present, the total mass of the sample must be', '95.2 g', '1.90 x 10<sup>2</sup> g', '2.10 x 10<sup>2</sup> g', '47.2 g', 'none of the above', 'c'),
    ('c11', 'How many hydrogen atoms are present in 3.41 g of NH<sub>3</sub>?<br>(MM(NH<sub>3</sub>) = 17.03 g/mol; <i>N<sub>A</sub></i> = 6.022 x 10<sup>23</sup> mol<sup>-1</sup>)', '2.89 x 10<sup>22</sup>', '1.21 x 10<sup>23</sup>', '2.41 x 10<sup>23</sup>', '3.62 x 10<sup>23</sup>', 'none of the above', 'd'),
    ('c12', 'At 25 &deg;C, 0.55 g of lead iodide (PbI<sub>2</sub>) will dissolve in 1.0 L of water. How much water is needed to dissolve 0.010 g of lead iodide?', '0.18 mL', '1.8 mL', '18 mL', '5.5 mL', '55 mL', 'c'),
    ('p1', 'In which of the following atoms is the number of valence electrons equal to six?', 'Si', 'P', 'S', 'Cl', 'none of the above', 'c'),
    ('m8', '6.00 x 10<sup>2</sup> mL of water at 25 &deg;C (density = 0.997 g/mL) is placed in a container. The water is then cooled to form ice at -10 &deg;C (density = 0.917 g/mL). What is the mass and volume of the ice?', '6.00 x 10<sup>2</sup> g and 652 mL', '598 g and 652 mL', '552 g and 652 mL', '598 g and 600 mL', 'not enought information provided to solve the problem', 'b'),
    ('p2', 'What is the most likely formula for a compound made from the combination of the elements Ca and Cl?', 'CaCl', 'CaCl<sub>2</sub>', 'Ca<sub>2</sub>Cl', 'CaCl<sub>3</sub>', 'Ca<sub>2</sub>Cl<sub>2</sub>', 'b'),
    ('m9', 'A piece of metal weighing 15.442 g is placed in 49.7 cm<sup>3</sup> of ethyl alcohol (<i>d</i> = 0.798 g/cm<sup>3</sup>) in a graduated cylinder. The alcohol level increases to 51.8 cm<sup>3</sup>. The density of the metal is', '9.2 g/cm<sup>3</sup>', '7.4 g/cm<sup>3</sup>', '0.31 g/cm<sup>3</sup>', '0.30 g/cm<sup>3</sup>', '0.14 g/cm<sup>3</sup>', 'b'),
    ('p3', 'Which of the following elements should be most similar to strontium, Sr, in chemical and physical properties?', 'Li', 'At', 'Rb', 'Ba', 'Cs', 'd'),
    ('m10', 'At 25 &deg;C, the density of oxygen in air is 1.31 g/L. What mass of oxygen is in a container whose size is 25 cm by 25 cm by 35 cm?', '17 g', '1.7 x 10<sup>4</sup> g', '2.2 x 10<sup>4</sup> g', '2.9 x 10<sup>4</sup> g', '29 g', 'e'),
    ('p4', 'Give the number of protons and electrons in <sup>79</sup>Se<sup>2-</sup>.', '32 protons and 34 electrons', '32 protons and 36 electrons', '34 protons and 32 electrons', '34 protons and 34 electrons', '34 protons and 36 electrons', 'e'),
    ('m11', 'Bicycles are made from 1 frame and 2 wheels.  Each box of frames contains 5 frames.  Each box of wheels contains 8 wheels.  If a bicycle company orders 3 boxes of frames and 4 boxes of wheels, how many bicycles can they build?', '3', '4', '12', '15', '24', 'd'),
    ('p5', 'Calculate the molar mass (molecular weight) of sulfur dioxide, SO<sub>2</sub>', '24 g/mol', '32 g/mol', '48 g/mol', '64 g/mol', '96 g/mol', 'd'),
    ('m12', 'Apples weigh 0.25 lbs each.  Pears weigh 0.20 lbs each.  Plums weigh 0.10 lbs each. If a box of fruit contains 10 apples, 10 pears, and 20 plums, apples make up _______ % of the total weight.', '25.0%', '33.3%', '34.5%', '38.5%', 'cannot be determined', 'd'),
    ('p6', 'Which of the following compounds has the <i>highest</i> percentage of oxygen by mass?', 'K<sub>2</sub>O<sub>2</sub>', 'KO<sub>2</sub>', 'K<sub>2</sub>C<sub>2</sub>O<sub>4</sub>', 'K<sub>2</sub>CO<sub>3</sub>', 'KHCO<sub>3</sub>', 'e')]

    letters = ['A', 'B', 'C', 'D', 'E']
    correct = ['a', 'b', 'c', 'd', 'e']

    for problem_data, i in zip(problems_data, xrange(len(problems_data))):
        p = Problem()
        p.number = i + 1
        p.text = problem_data[1]
        p.save()
    
        for x in xrange(5):
            a = Answer()
            a.letter = letters[x]
            a.text = problem_data[2 + x]
            if correct[x] == problem_data[7]:
                a.correct = True
            else:
                a.correct = False
            a.problem = p
            a.save()
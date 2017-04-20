'''
Created on Feb 1, 2017
Generate json for research category and research topic

@author: Zhongchao
'''

Topic = {
    'None': ['-----'],
    'Computer Science': [['CS01', 'E-Business'], ['CS02', 'User Adaptive System'], ['CS03', 'Mathematical Computing'], ['CS04', 'Theory of Computing'], ['CS05', 'Algorithm'], ['CS06', 'Computer Network'], ['CS07', 'Quantum Computing'], ['CS08', 'Information System'], ['CS09', 'Security and Privacy'], ['CS10', 'Database Management'], ['CS11', 'Programming Languages'], ['CS12', 'Software Engineering'], ['CS13', 'Formal Methods'], ['CS14', 'Computer System'], ['CS15', 'Distributed Computing'], ['CS16', 'Web Engineering'], ['CS17', 'Human Computer Interface'], ['CS18', 'Artificial Intelligence'], ['CS19', 'Graphics and Visualization'], ['CS20', 'Bioinformatics'], ['CS21', 'Computer Vision'],],
    'Life Science 1': [['LSA01', 'Immunology'], ['LSA02', 'Microbiology'], ['LSA03', 'Cell Structure and Function'], ['LSA04', 'Cellular and Molecular Biology'], ['LSA05', 'Genetics'], ['LSA06', 'Developmental Biology'], ['LSA07', 'Signal Transduction'], ['LSA08', 'Computational Neuroscience'], ['LSA09', 'Biochemistry'], ],   
    'Life Science 2': [['LSB01', 'Plant Biology'], ['LSB02', 'Food Science'], ['LSB03', 'Physiology'], ['LSB06', 'Neuroscience'], ['LSB07', 'Cognitive Science'], ['LSB09', 'Nutritional Science'],],
    }

Category = (
    ('None', '-----'),
    ('Computer Science', 'Computer Science'),
    ('Life Science 1', 'Life Science 1'),
    ('Life Science 2', 'Life Science 2'),
)

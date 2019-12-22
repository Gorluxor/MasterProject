# converting_rs_legal_acts_to_akoma_ntoso

data/akoma_result/ contains all the Akoma Ntoso xml files

data/aktovi_html/ contains all the acts as they were scraped from http://www.pravno-informacioni-sistem.rs/SlGlasnikPortal/fp/news

data/aktoviraw/ contains the all the acts after preprocessing


convert_all.py converts all the files in data/aktovi_html/ and places the resulting xml files in data/akoma_result/


To convert a specific file run convert_html.py as so: convert_html.py <source_path> <destination_path>

The source file needs to have the same name as it appears in data/metadata.csv, otherwise the result will not have any metadata elements
